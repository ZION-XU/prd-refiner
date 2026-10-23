#!/usr/bin/env python3
"""Fetch a Confluence page or Jira issue and referenced images into a local snapshot.

Automatically discovers Confluence/Jira credentials, URLs, auth schemes (PAT Bearer
or Basic Auth username+token), and custom headers from existing MCP configurations
(JSON, TOML, CLI args, .env) or environment variables across intranet and extranet.

The target workspace must be passed explicitly: the snapshot is a machine asset
of the requirement workspace, never of whatever directory happens to be current.
"""
from __future__ import annotations

import argparse
import base64
from concurrent.futures import ThreadPoolExecutor
import json
import os
from pathlib import Path
import re
import shlex
import ssl
import sys
import tempfile
import urllib.error
import urllib.parse
import urllib.request

from build_snapshot import (
    IMAGE_EXTENSIONS,
    create_snapshot_from_data,
    extract_filename_from_target,
    extract_referenced_filenames,
)


JIRA_KEY_RE = re.compile(r'^[A-Z][A-Z0-9_]{1,19}-\d+$')


def parse_page_id(input_value: str) -> str:
    """Extract numeric page ID from string, URL or tiny link."""
    val = input_value.strip()
    if val.isdigit():
        return val
    parsed = urllib.parse.urlsplit(val)
    query = urllib.parse.parse_qs(parsed.query)
    if 'pageId' in query and query['pageId']:
        return query['pageId'][0]
    m = re.search(r'/pages/(\d+)', parsed.path)
    if m:
        return m.group(1)
    digits = re.findall(r'\b\d{6,12}\b', val)
    if digits:
        return digits[0]
    return val


def parse_jira_issue_key(input_value: str) -> str | None:
    """Extract Jira issue key (e.g. PROJ-123) from key string or browse/API URL."""
    val = input_value.strip()
    if JIRA_KEY_RE.match(val):
        return val
    parsed = urllib.parse.urlsplit(val)
    for pattern in (r'/browse/([A-Z][A-Z0-9_]{1,19}-\d+)',
                    r'/issues/([A-Z][A-Z0-9_]{1,19}-\d+)',
                    r'/rest/api/(?:2|3|latest)/issue/([A-Z][A-Z0-9_]{1,19}-\d+)'):
        m = re.search(pattern, parsed.path)
        if m:
            return m.group(1)
    query = urllib.parse.parse_qs(parsed.query)
    for key in ('selectedIssue', 'issueKey'):
        if key in query and query[key] and JIRA_KEY_RE.match(query[key][0]):
            return query[key][0]
    return None


def read_pat_token(token_str_or_path: str) -> str:
    token_str = token_str_or_path.strip()
    if not token_str:
        return ''
    m = re.match(r'^\{file:(.+)\}$', token_str)
    if m:
        file_path = Path(m.group(1).strip()).expanduser()
        if file_path.is_file():
            return file_path.read_text(encoding='utf-8').strip()
    if token_str.startswith('@') and len(token_str) > 1:
        at_path = Path(token_str[1:].strip()).expanduser()
        if at_path.is_file():
            try:
                return at_path.read_text(encoding='utf-8').strip()
            except OSError:
                pass
    try:
        candidate = Path(token_str).expanduser()
        if candidate.is_file():
            return candidate.read_text(encoding='utf-8').strip()
    except OSError:
        pass
    return token_str


def find_mcp_config_candidates(workspace: Path | None = None) -> list[Path]:
    home = Path.home()
    candidates = [
        home / '.gemini' / 'config' / 'mcp_config.json',
        home / '.gemini' / 'antigravity' / 'mcp_config.json',
        home / '.gemini' / 'antigravity-ide' / 'mcp_config.json',
        home / '.gemini' / 'settings.json',
        home / '.codex' / 'config.toml',
        home / '.config' / 'opencode' / 'opencode.json',
        home / '.codeium' / 'windsurf' / 'mcp_config.json',
        home / '.cursor' / 'mcp.json',
        home / '.claude.json',
        home / '.claude' / 'settings.json',
        home / '.zcode' / 'mcp.json',
        home / '.zcode' / 'v2' / 'mcp.json',
        home / '.vscode' / 'mcp.json',
    ]
    cur = (workspace or Path.cwd()).resolve()
    for _ in range(5):
        candidates.extend([
            cur / '.mcp.json',
            cur / 'mcp_config.json',
            cur / '.cursor' / 'mcp.json',
            cur / '.vscode' / 'mcp.json',
            cur / '.codex' / 'config.toml',
        ])
        if cur.parent == cur:
            break
        cur = cur.parent
    return candidates


def parse_dotenv_file(path: Path) -> dict[str, str]:
    """Parse a simple .env file into a dictionary."""
    env: dict[str, str] = {}
    try:
        lines = path.expanduser().read_text(encoding='utf-8-sig', errors='ignore').splitlines()
    except OSError:
        return env
    for raw in lines:
        line = raw.strip()
        if not line or line.startswith('#'):
            continue
        if line.startswith('export '):
            line = line[7:].strip()
        if '=' not in line:
            continue
        k, v = line.split('=', 1)
        k = k.strip()
        v = v.strip()
        if len(v) >= 2 and v[0] == v[-1] and v[0] in {'"', "'"}:
            v = v[1:-1]
        if k:
            env[k] = v
    return env


_CLI_FLAG_TO_ENV = {
    '--confluence-url': 'CONFLUENCE_URL',
    '--confluence-personal-token': 'CONFLUENCE_PERSONAL_TOKEN',
    '--confluence-token': 'CONFLUENCE_API_TOKEN',
    '--confluence-username': 'CONFLUENCE_USERNAME',
    '--jira-url': 'JIRA_URL',
    '--jira-personal-token': 'JIRA_PERSONAL_TOKEN',
    '--jira-token': 'JIRA_API_TOKEN',
    '--jira-username': 'JIRA_USERNAME',
    '--oauth-access-token': 'OAUTH_ACCESS_TOKEN',
}


def parse_cli_args_to_env(args: list | str | None, base_dir: Path | None = None) -> dict[str, str]:
    """Extract Atlassian MCP CLI options and --env-file from command args."""
    if not args:
        return {}
    if isinstance(args, str):
        try:
            tokens = shlex.split(args, posix=(os.name != 'nt'))
        except ValueError:
            tokens = args.split()
    elif isinstance(args, list):
        tokens = [str(x) for x in args]
    else:
        return {}

    extracted: dict[str, str] = {}
    i = 0
    while i < len(tokens):
        tok = tokens[i]
        if '=' in tok and tok.startswith('--'):
            flag, val = tok.split('=', 1)
        else:
            flag, val = tok, None
        if flag == '--no-confluence-ssl-verify':
            extracted['CONFLUENCE_SSL_VERIFY'] = 'false'
        elif flag == '--confluence-ssl-verify':
            extracted['CONFLUENCE_SSL_VERIFY'] = 'true'
        elif flag == '--no-jira-ssl-verify':
            extracted['JIRA_SSL_VERIFY'] = 'false'
        elif flag == '--jira-ssl-verify':
            extracted['JIRA_SSL_VERIFY'] = 'true'
        elif flag == '--env-file':
            if val is None and i + 1 < len(tokens):
                i += 1
                val = tokens[i]
            if val:
                env_path = Path(val).expanduser()
                if not env_path.is_absolute() and base_dir:
                    env_path = base_dir / env_path
                extracted.update(parse_dotenv_file(env_path))
        elif flag in _CLI_FLAG_TO_ENV:
            if val is None and i + 1 < len(tokens):
                i += 1
                val = tokens[i]
            if val is not None:
                extracted[_CLI_FLAG_TO_ENV[flag]] = val
        i += 1
    return extracted


def _unquote_toml_value(raw: str) -> str:
    val = raw.strip()
    if len(val) >= 2 and val[0] == val[-1] and val[0] in {'"', "'"}:
        inner = val[1:-1]
        if val[0] == '"':
            inner = inner.replace(r'\\', '\\').replace(r'\"', '"')
        return inner
    return val


def parse_toml_mcp_env(text: str, base_dir: Path | None = None) -> list[dict[str, str]]:
    """Extract env dicts from TOML MCP server sections (e.g. ~/.codex/config.toml)."""
    sections: dict[str, dict[str, str]] = {}
    args_by_server: dict[str, list[str]] = {}
    current_server: str | None = None
    in_env = False

    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith('#'):
            continue
        sec_match = re.match(r'^\[([^\]]+)\]\s*$', line)
        if sec_match:
            sec_name = sec_match.group(1).strip()
            m_env = re.match(r'^mcp_servers\.([A-Za-z0-9_\-]+)\.env$', sec_name)
            m_srv = re.match(r'^mcp_servers\.([A-Za-z0-9_\-]+)$', sec_name)
            if m_env:
                current_server = m_env.group(1)
                in_env = True
                sections.setdefault(current_server, {})
            elif m_srv:
                current_server = m_srv.group(1)
                in_env = False
                sections.setdefault(current_server, {})
            else:
                current_server = None
                in_env = False
            continue
        if not current_server or '=' not in line:
            continue
        k, v = line.split('=', 1)
        k = k.strip()
        v = v.strip()
        if in_env:
            sections[current_server][k] = _unquote_toml_value(v)
        elif k == 'args' and v.startswith('[') and v.endswith(']'):
            items = re.findall(r'"(?:\\.|[^"\\])*"|\'[^\']*\'', v)
            args_by_server[current_server] = [_unquote_toml_value(x) for x in items]
        elif k == 'env_file':
            env_path = Path(_unquote_toml_value(v)).expanduser()
            if not env_path.is_absolute() and base_dir:
                env_path = base_dir / env_path
            sections[current_server].update(parse_dotenv_file(env_path))

    results: list[dict[str, str]] = []
    # Prioritize servers named atlassian/confluence/jira
    ordered = sorted(sections.keys(), key=lambda s: (
        0 if any(w in s.casefold() for w in ('atlassian', 'confluence', 'jira')) else 1, s
    ))
    for srv in ordered:
        merged: dict[str, str] = {}
        if srv in args_by_server:
            merged.update(parse_cli_args_to_env(args_by_server[srv], base_dir))
        merged.update(sections[srv])
        if merged:
            results.append(merged)
    return results


def extract_mcp_env_maps(path: Path) -> list[dict[str, str]]:
    """Read a JSON or TOML MCP configuration file and return candidate env maps."""
    try:
        text = path.read_text(encoding='utf-8-sig', errors='ignore')
    except OSError:
        return []
    if path.suffix.casefold() == '.toml':
        return parse_toml_mcp_env(text, path.parent)
    try:
        data = json.loads(text)
    except Exception:
        return []
    if not isinstance(data, dict):
        return []

    server_Maps: list[tuple[str, dict]] = []
    for root_key in ('mcpServers', 'mcp', 'servers'):
        container = data.get(root_key)
        if isinstance(container, dict):
            for name, cfg in container.items():
                if isinstance(cfg, dict):
                    server_Maps.append((name, cfg))
    projects = data.get('projects')
    if isinstance(projects, dict):
        for proj_cfg in projects.values():
            if isinstance(proj_cfg, dict) and isinstance(proj_cfg.get('mcpServers'), dict):
                for name, cfg in proj_cfg['mcpServers'].items():
                    if isinstance(cfg, dict):
                        server_Maps.append((name, cfg))

    server_Maps.sort(key=lambda item: (
        0 if any(w in item[0].casefold() for w in ('atlassian', 'confluence', 'jira')) else 1
    ))

    results: list[dict[str, str]] = []
    for _, cfg in server_Maps:
        merged: dict[str, str] = {}
        env_file = cfg.get('envFile') or cfg.get('env_file')
        if isinstance(env_file, str) and env_file.strip():
            ef_path = Path(env_file.strip()).expanduser()
            if not ef_path.is_absolute():
                ef_path = path.parent / ef_path
            merged.update(parse_dotenv_file(ef_path))
        cmd = cfg.get('command')
        args = cfg.get('args')
        if isinstance(cmd, list):
            merged.update(parse_cli_args_to_env(cmd + (args if isinstance(args, list) else []), path.parent))
        else:
            merged.update(parse_cli_args_to_env(args, path.parent))
        raw_env = cfg.get('env') or cfg.get('environment') or {}
        if isinstance(raw_env, dict):
            for k, v in raw_env.items():
                if v is not None:
                    merged[str(k)] = str(v)
        if merged:
            results.append(merged)
    return results


def parse_custom_headers(raw: str | dict | None) -> dict[str, str]:
    """Parse custom header strings like 'User-Agent=mcp-atlassian/1.0' or 'K: V'."""
    headers: dict[str, str] = {'User-Agent': 'mcp-atlassian/1.0'}
    if not raw:
        return headers
    if isinstance(raw, dict):
        for k, v in raw.items():
            if k and v is not None:
                headers[str(k).strip()] = str(v).strip()
        return headers
    text = str(raw).strip()
    if text.startswith('{') and text.endswith('}'):
        try:
            parsed = json.loads(text)
            if isinstance(parsed, dict):
                return parse_custom_headers(parsed)
        except Exception:
            pass
    for part in re.split(r'[\r\n,;]+', text):
        item = part.strip()
        if not item:
            continue
        if '=' in item and (':' not in item or item.index('=') < item.index(':')):
            k, v = item.split('=', 1)
        elif ':' in item:
            k, v = item.split(':', 1)
        else:
            continue
        if k.strip():
            headers[k.strip()] = v.strip()
    return headers


def _extract_service_config(env: dict[str, str], service: str, default_url: str) -> dict | None:
    prefix = service.upper()  # CONFLUENCE or JIRA
    url = (env.get(f'{prefix}_URL') or env.get(f'{prefix}_BASE_URL')
           or env.get('ATLASSIAN_URL') or '').strip()
    pat_raw = (env.get(f'{prefix}_PERSONAL_TOKEN') or env.get(f'{prefix}_PAT')
               or env.get(f'{prefix}_OAUTH_ACCESS_TOKEN') or env.get('OAUTH_ACCESS_TOKEN') or '').strip()
    api_raw = (env.get(f'{prefix}_API_TOKEN') or env.get(f'{prefix}_TOKEN')
               or env.get(f'{prefix}_PASSWORD') or env.get('ATLASSIAN_API_TOKEN')
               or env.get('ATLASSIAN_TOKEN') or '').strip()
    username = (env.get(f'{prefix}_USERNAME') or env.get(f'{prefix}_USER')
                or env.get('ATLASSIAN_USERNAME') or env.get('ATLASSIAN_EMAIL') or '').strip()
    custom_headers = parse_custom_headers(
        env.get(f'{prefix}_CUSTOM_HEADERS') or env.get('ATLASSIAN_CUSTOM_HEADERS')
    )
    ssl_verify_raw = (env.get(f'{prefix}_SSL_VERIFY') or '').strip().casefold()
    ssl_verify = ssl_verify_raw not in {'false', '0', 'no', 'off'} if ssl_verify_raw else False

    pat = read_pat_token(pat_raw) if pat_raw else ''
    api_token = read_pat_token(api_raw) if api_raw else ''
    token = pat or api_token
    if not token:
        return None
    auth_scheme = 'bearer' if pat else ('basic' if username else 'bearer')
    return {
        'url': (url or default_url).rstrip('/'),
        'token': token,
        'username': username,
        'auth_scheme': auth_scheme,
        'custom_headers': custom_headers,
        'ssl_verify': ssl_verify,
    }


def discover_atlassian_mcp_config(workspace: Path | None = None,
                                  service: str = 'confluence') -> dict:
    """Discover URL, token, username, auth_scheme, and custom_headers for Confluence or Jira."""
    service = service.casefold()
    default_url = 'https://jira.zwcad.com' if service == 'jira' else 'https://confluence.zwcad.com'
    prefix = service.upper()
    env_url = (os.environ.get(f'{prefix}_URL') or default_url).rstrip('/')

    from_env = _extract_service_config(dict(os.environ), service, default_url)
    if from_env:
        from_env['source'] = 'environment variable'
        return from_env

    for candidate in find_mcp_config_candidates(workspace):
        if not candidate.is_file():
            continue
        for env_map in extract_mcp_env_maps(candidate):
            merged = {**os.environ, **env_map}
            extracted = _extract_service_config(merged, service, env_url)
            if extracted:
                extracted['source'] = str(candidate)
                return extracted

    pat_filename = 'jira-PAT.txt' if service == 'jira' else 'confluence-PAT.txt'
    for common_path in [Path.home() / pat_filename]:
        if common_path.is_file():
            try:
                token = common_path.read_text(encoding='utf-8').strip()
                if token:
                    return {
                        'url': env_url,
                        'token': token,
                        'username': '',
                        'auth_scheme': 'bearer',
                        'custom_headers': parse_custom_headers(None),
                        'ssl_verify': False,
                        'source': str(common_path),
                    }
            except OSError:
                pass

    return {
        'url': env_url,
        'token': '',
        'username': '',
        'auth_scheme': 'bearer',
        'custom_headers': parse_custom_headers(None),
        'ssl_verify': False,
        'source': 'none',
    }


def discover_confluence_mcp_config(workspace: Path | None = None) -> tuple[str, str, str]:
    """Return (confluence_url, token, source_description)."""
    cfg = discover_atlassian_mcp_config(workspace, service='confluence')
    return cfg['url'], cfg['token'], cfg['source']


def build_auth_headers(token: str, username: str = '', auth_scheme: str = 'auto',
                       custom_headers: dict[str, str] | None = None) -> list[dict[str, str]]:
    """Build ordered candidate HTTP header dicts supporting Bearer and Basic Auth fallback."""
    base = parse_custom_headers(custom_headers)
    tok = token.strip()
    if not tok:
        return [base]
    if tok.casefold().startswith(('bearer ', 'basic ')):
        return [{**base, 'Authorization': tok}]

    bearer = {**base, 'Authorization': f'Bearer {tok}'}
    if username:
        encoded = base64.b64encode(f'{username}:{tok}'.encode('utf-8')).decode('ascii')
        basic = {**base, 'Authorization': f'Basic {encoded}'}
        if auth_scheme == 'basic':
            return [basic, bearer]
        return [bearer, basic]
    return [bearer]


def create_ssl_context() -> ssl.SSLContext:
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    return ctx


def _request_json(url: str, header_candidates: list[dict[str, str]],
                  ctx: ssl.SSLContext, timeout: int = 15,
                  not_found_msg: str = 'Resource not found (404)',
                  auth_fail_msg: str = 'Confluence PAT authentication failed (401 Unauthorized)') -> dict:
    last_exc: Exception | None = None
    for idx, headers in enumerate(header_candidates):
        req = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(req, context=ctx, timeout=timeout) as resp:
                raw = resp.read().decode('utf-8', errors='replace')
                data = json.loads(raw)
                if isinstance(data, dict):
                    return data
        except urllib.error.HTTPError as exc:
            last_exc = exc
            if exc.code in (401, 403) and idx + 1 < len(header_candidates):
                continue
            if exc.code == 401:
                raise PermissionError(auth_fail_msg) from exc
            if exc.code == 404:
                raise FileNotFoundError(not_found_msg) from exc
            raise RuntimeError(f'HTTP {exc.code} {exc.reason}') from exc
        except json.JSONDecodeError as exc:
            last_exc = exc
            if idx + 1 < len(header_candidates):
                continue
            raise RuntimeError('Server returned non-JSON response (check URL or SSO gateway)') from exc
    if isinstance(last_exc, urllib.error.HTTPError) and last_exc.code in (401, 403):
        raise PermissionError(auth_fail_msg) from last_exc
    raise RuntimeError(f'Request failed: {last_exc}')


def fetch_page_content(base_url: str, page_id: str, pat: str,
                       ctx: ssl.SSLContext, *, username: str = '',
                       auth_scheme: str = 'auto',
                       custom_headers: dict[str, str] | None = None) -> tuple[str, str, str, list[dict]]:
    """Fetch page storage body, version, web URL, and attachment metadata."""
    base = base_url.rstrip('/')
    url = f'{base}/rest/api/content/{page_id}?expand=body.storage,version,space,children.attachment'
    header_candidates = build_auth_headers(pat, username=username,
                                           auth_scheme=auth_scheme,
                                           custom_headers=custom_headers)
    try:
        data = _request_json(
            url,
            header_candidates,
            ctx,
            timeout=15,
            not_found_msg=f'Confluence page {page_id} not found (404)',
            auth_fail_msg='Confluence PAT authentication failed (401 Unauthorized)',
        )
    except FileNotFoundError:
        if not base.endswith('/wiki'):
            alt_base = f'{base}/wiki'
            alt_url = f'{alt_base}/rest/api/content/{page_id}?expand=body.storage,version,space,children.attachment'
            data = _request_json(
                alt_url,
                header_candidates,
                ctx,
                timeout=15,
                not_found_msg=f'Confluence page {page_id} not found (404)',
                auth_fail_msg='Confluence PAT authentication failed (401 Unauthorized)',
            )
            base = alt_base
        else:
            raise
    except RuntimeError as exc:
        if str(exc).startswith('HTTP '):
            raise RuntimeError(f'Failed to fetch page {page_id}: {exc}') from exc
        raise

    content = data.get('body', {}).get('storage', {}).get('value', '')
    version = str(data.get('version', {}).get('number', ''))
    web_url = f'{base}/pages/viewpage.action?pageId={page_id}'
    raw_attachments = (
        data.get('children', {}).get('attachment', {}).get('results')
        or data.get('attachments')
        or []
    )
    attachments: list[dict] = []
    for item in raw_attachments:
        if not isinstance(item, dict):
            continue
        links = item.get('_links') or {}
        dl_path = links.get('download') or item.get('download_url') or ''
        dl_url = f'{base}{dl_path}' if isinstance(dl_path, str) and dl_path.startswith('/') else dl_path
        attachments.append({
            'id': item.get('id'),
            'title': item.get('title', ''),
            'download_url': dl_url or None,
        })
    return content, version, web_url, attachments


def fetch_current_user(base_url: str, pat: str, ctx: ssl.SSLContext, *,
                       username: str = '', auth_scheme: str = 'auto',
                       custom_headers: dict[str, str] | None = None) -> dict:
    """Fetch current user profile (username, displayName) associated with the credentials."""
    base = base_url.rstrip('/')
    header_candidates = build_auth_headers(pat, username=username,
                                           auth_scheme=auth_scheme,
                                           custom_headers=custom_headers)
    for endpoint in (f'{base}/rest/api/user/current', f'{base}/wiki/rest/api/user/current'):
        for headers in header_candidates:
            req = urllib.request.Request(endpoint, headers=headers)
            try:
                with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
                    data = json.loads(resp.read().decode('utf-8'))
                    return {
                        'username': data.get('username') or data.get('accountId', ''),
                        'display_name': data.get('displayName') or data.get('publicName', ''),
                        'user_key': data.get('userKey') or data.get('accountId', ''),
                    }
            except Exception:
                continue
    return {}


def download_attachment_direct(base_url: str, page_id: str, filename: str, pat: str,
                               dest: Path, ctx: ssl.SSLContext, retries: int = 2, *,
                               username: str = '', auth_scheme: str = 'auto',
                               custom_headers: dict[str, str] | None = None,
                               extra_urls: list[str] | None = None) -> bool:
    """Download image directly by filename using Confluence/Jira attachment endpoints."""
    encoded_name = urllib.parse.quote(filename)
    base = base_url.rstrip('/')
    urls: list[str] = []
    if extra_urls:
        urls.extend(u for u in extra_urls if u)
    if page_id:
        urls.extend([
            f'{base}/download/attachments/{page_id}/{encoded_name}?api=v2',
            f'{base}/download/attachments/{page_id}/{encoded_name}',
        ])
    header_candidates = build_auth_headers(pat, username=username,
                                           auth_scheme=auth_scheme,
                                           custom_headers=custom_headers)
    for _ in range(retries + 1):
        for url in urls:
            for headers in header_candidates:
                req = urllib.request.Request(url, headers=headers)
                try:
                    with urllib.request.urlopen(req, context=ctx, timeout=15) as resp:
                        payload = resp.read()
                        if payload and not payload[:512].lstrip().lower().startswith((b'<!doctype html', b'<html')):
                            dest.write_bytes(payload)
                            return True
                except Exception:
                    continue
    return False


def _format_jira_issue_content(issue_key: str, data: dict) -> tuple[str, str, list[dict]]:
    """Convert Jira REST API issue payload into snapshot Markdown/HTML and attachment records."""
    fields = data.get('fields') or {}
    rendered = data.get('renderedFields') or {}
    summary = str(fields.get('summary') or issue_key).strip()
    status = str((fields.get('status') or {}).get('name') or '').strip()
    issue_type = str((fields.get('issuetype') or {}).get('name') or '').strip()
    priority = str((fields.get('priority') or {}).get('name') or '').strip()
    reporter = str((fields.get('reporter') or {}).get('displayName') or '').strip()
    assignee = str((fields.get('assignee') or {}).get('displayName') or '').strip()
    updated = str(fields.get('updated') or data.get('id') or '1').strip()

    description = str(rendered.get('description') or fields.get('description') or '').strip()
    # Convert Jira wiki image syntax !image.png|thumbnail! to Markdown ![image.png](image.png)
    def _replace_wiki_img(m: re.Match) -> str:
        raw_target = m.group(1).split('|', 1)[0].strip()
        fname = extract_filename_from_target(raw_target)
        return f'![{fname}]({fname})' if fname else m.group(0)

    description = re.sub(r'!([^!\n\r]+?\.[A-Za-z0-9]{2,5}(?:\|[^!\n\r]*)?)!', _replace_wiki_img, description)

    raw_attachments = fields.get('attachment') or []
    attachments: list[dict] = []
    image_attachments: list[str] = []
    for item in raw_attachments:
        if not isinstance(item, dict):
            continue
        filename = extract_filename_from_target(str(item.get('filename') or ''))
        dl_url = str(item.get('content') or '').strip()
        if filename:
            attachments.append({
                'id': str(item.get('id') or ''),
                'title': filename,
                'download_url': dl_url or None,
            })
            if Path(filename).suffix.casefold() in IMAGE_EXTENSIONS:
                image_attachments.append(filename)

    lines = [
        f'# [{issue_key}] {summary}',
        '',
        '| 字段 | 内容 |',
        '|---|---|',
        f'| Issue Key | {issue_key} |',
        f'| 类型 | {issue_type or "-"} |',
        f'| 状态 | {status or "-"} |',
        f'| 优先级 | {priority or "-"} |',
        f'| 报告人 | {reporter or "-"} |',
        f'| 经办人 | {assignee or "-"} |',
        '',
        '## 需求描述',
        '',
        description or '（无描述）',
    ]

    comments = ((fields.get('comment') or {}).get('comments')) or []
    if comments:
        lines.extend(['', '## 评论记录', ''])
        for c in comments:
            if not isinstance(c, dict):
                continue
            author = str((c.get('author') or {}).get('displayName') or '未知').strip()
            created = str(c.get('created') or '').strip()
            body = str(c.get('body') or '').strip()
            body = re.sub(r'!([^!\n\r]+?\.[A-Za-z0-9]{2,5}(?:\|[^!\n\r]*)?)!', _replace_wiki_img, body)
            lines.append(f'### {author} ({created})')
            lines.append(body)
            lines.append('')

    content_So_Far = '\n'.join(lines)
    already_referenced = set(extract_referenced_filenames(content_So_Far))
    unreferenced_images = [img for img in image_attachments if img not in already_referenced]
    if unreferenced_images:
        lines.extend(['', '## 附件图片', ''])
        for img in unreferenced_images:
            lines.append(f'![{img}]({img})')

    return '\n'.join(lines) + '\n', updated, attachments


def fetch_jira_snapshot(issue_key: str, workspace: Path,
                        base_url: str | None = None,
                        pat: str | None = None,
                        ctx: ssl.SSLContext | None = None) -> dict:
    """Fetch a Jira issue and its image attachments into an immutable `.assets/` snapshot."""
    cfg = discover_atlassian_mcp_config(workspace, service='jira')
    if not cfg['token'] and not pat:
        # Fallback to shared Confluence/Atlassian MCP credentials if Jira shares SSO/PAT
        shared = discover_atlassian_mcp_config(workspace, service='confluence')
        if shared['token']:
            cfg['token'] = shared['token']
            cfg['username'] = cfg['username'] or shared['username']
            cfg['auth_scheme'] = shared['auth_scheme']
            cfg['source'] = shared['source']

    url = (base_url or cfg['url']).rstrip('/')
    token = (pat or cfg['token']).strip()
    if not token:
        return {
            'passed': False,
            'errors': [
                'No Jira token found. Please configure JIRA_PERSONAL_TOKEN / JIRA_API_TOKEN '
                'in MCP config (atlassian), environment variable, or provide --pat.'
            ],
        }

    ctx = ctx or create_ssl_context()
    header_candidates = build_auth_headers(
        token, username=cfg['username'], auth_scheme=cfg['auth_scheme'],
        custom_headers=cfg['custom_headers'],
    )
    api_url = f'{url}/rest/api/2/issue/{issue_key}?expand=renderedFields'
    try:
        data = _request_json(
            api_url, header_candidates, ctx, timeout=15,
            not_found_msg=f'Jira issue {issue_key} not found (404)',
            auth_fail_msg='Jira authentication failed (401 Unauthorized)',
        )
    except Exception as exc:
        return {'passed': False, 'errors': [f'{type(exc).__name__}: {exc}']}

    content, version, attachments = _format_jira_issue_content(issue_key, data)
    web_url = f'{url}/browse/{issue_key}'
    images = extract_referenced_filenames(content)
    dl_by_name = {item['title']: item.get('download_url') for item in attachments if item.get('title')}
    missing_downloads: list[str] = []

    with tempfile.TemporaryDirectory(prefix='prd-jira-assets-') as temp_dir:
        temp_path = Path(temp_dir)
        cached_files: dict[str, Path] = {}

        for img_name in images:
            dest_file = temp_path / img_name
            dl_url = dl_by_name.get(img_name)
            ok = download_attachment_direct(
                url, '', img_name, token, dest_file, ctx,
                username=cfg['username'], auth_scheme=cfg['auth_scheme'],
                custom_headers=cfg['custom_headers'],
                extra_urls=[dl_url] if dl_url else [],
            )
            if ok:
                cached_files[img_name] = dest_file
            else:
                missing_downloads.append(img_name)

        if missing_downloads:
            return {
                'passed': False,
                'errors': [f'Failed to download images from Jira: {missing_downloads}'],
                'referenced_images': images,
                'missing_images': missing_downloads,
            }

        source_meta = {
            'page_id': issue_key,
            'version': version,
            'url': web_url,
            'kind': 'jira',
        }
        result = create_snapshot_from_data(
            content=content,
            attachments=attachments,
            workspace_dir=workspace,
            cached_files=cached_files,
            source_metadata=source_meta,
        )
        result['pat_source'] = cfg['source']
        return result


def fetch_and_build_snapshot(page_id: str, workspace: Path,
                             base_url: str | None = None,
                             pat: str | None = None,
                             force: bool = False) -> dict:
    workspace = workspace.resolve()
    target_dir = workspace / '.assets'
    marker = target_dir / 'manifest.json'
    if marker.exists():
        if force:
            # Overwrite only the snapshot's own files; never remove the shared
            # `.assets` tree or assets belonging to other artifacts.
            for name in ('manifest.json', 'source.md', 'source.original.txt'):
                (target_dir / name).unlink(missing_ok=True)
        else:
            return {
                'passed': False,
                'errors': [f'snapshot already exists: {marker}. Use --force to overwrite.'],
                'snapshot_dir': str(target_dir),
            }

    jira_key = parse_jira_issue_key(page_id)
    if jira_key:
        return fetch_jira_snapshot(jira_key, workspace, base_url=base_url, pat=pat)

    discovered_url, discovered_pat, src_desc = discover_confluence_mcp_config(workspace)
    extra_cfg = discover_atlassian_mcp_config(workspace, service='confluence')
    url = (base_url or discovered_url).rstrip('/')
    token = (pat or discovered_pat).strip()

    if not token:
        return {
            'passed': False,
            'errors': [
                'No Confluence PAT found. Please configure PAT in MCP config (atlassian), '
                'set CONFLUENCE_PERSONAL_TOKEN env var, or provide --pat-file.'
            ]
        }

    ctx = create_ssl_context()
    username = extra_cfg.get('username', '')
    auth_scheme = extra_cfg.get('auth_scheme', 'auto')
    custom_headers = extra_cfg.get('custom_headers')

    try:
        content, version, web_url, attachments = fetch_page_content(
            url, page_id, token, ctx,
            username=username, auth_scheme=auth_scheme, custom_headers=custom_headers,
        )
    except Exception as exc:
        return {
            'passed': False,
            'errors': [f'{type(exc).__name__}: {exc}'],
        }

    author_info = fetch_current_user(
        url, token, ctx,
        username=username, auth_scheme=auth_scheme, custom_headers=custom_headers,
    )

    images = extract_referenced_filenames(content)
    dl_by_name = {item.get('title', ''): item.get('download_url')
                  for item in attachments if isinstance(item, dict) and item.get('title')}
    missing_downloads = []

    with tempfile.TemporaryDirectory(prefix='prd-snapshot-assets-') as temp_dir:
        temp_path = Path(temp_dir)
        cached_files = {}

        def _download_one(img_name: str) -> tuple[str, bool]:
            dest_file = temp_path / img_name
            dl_url = dl_by_name.get(img_name)
            success = download_attachment_direct(
                url, page_id, img_name, token, dest_file, ctx,
                username=username, auth_scheme=auth_scheme, custom_headers=custom_headers,
                extra_urls=[dl_url] if dl_url else None,
            )
            return img_name, success

        max_workers = min(10, max(1, len(images)))
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            download_results = list(executor.map(_download_one, images))

        for img_name, success in download_results:
            if success:
                cached_files[img_name] = temp_path / img_name
            else:
                missing_downloads.append(img_name)

        if missing_downloads:
            return {
                'passed': False,
                'errors': [f'Failed to download images directly from Confluence: {missing_downloads}'],
                'referenced_images': images,
                'missing_images': missing_downloads,
            }

        source_meta = {
            'page_id': page_id,
            'version': version,
            'url': web_url,
        }
        if author_info and (author_info.get('display_name') or author_info.get('username')):
            source_meta['author'] = author_info

        result = create_snapshot_from_data(
            content=content,
            attachments=attachments,
            workspace_dir=workspace,
            cached_files=cached_files,
            source_metadata=source_meta,
        )
        result['pat_source'] = src_desc
        if author_info:
            result['author'] = author_info
        return result


def main(argv: list[str] | None = None) -> int:
    if hasattr(sys.stdout, 'reconfigure'):
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except Exception:
            pass
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--page-id', required=True,
                        help='Confluence page ID/URL or Jira issue key/URL (e.g. PROJ-123)')
    parser.add_argument('--workspace', required=True, type=Path,
                        help='Requirement workspace root (absolute path); snapshot lands in <workspace>/.assets')
    parser.add_argument('--url', help='Confluence or Jira base URL (overrides MCP config)')
    parser.add_argument('--pat', help='Confluence or Jira PAT / API token (overrides MCP config)')
    parser.add_argument('--pat-file', type=Path, help='File containing PAT / API token')
    parser.add_argument('--force', action='store_true', help='Overwrite existing snapshot if present')
    args = parser.parse_args(argv)

    raw_target = args.page_id.strip()
    jira_key = parse_jira_issue_key(raw_target)
    page_id = jira_key if jira_key else parse_page_id(raw_target)
    pat = args.pat
    if not pat and args.pat_file and args.pat_file.is_file():
        pat = args.pat_file.read_text(encoding='utf-8').strip()

    result = fetch_and_build_snapshot(
        page_id=page_id,
        workspace=args.workspace,
        base_url=args.url,
        pat=pat,
        force=args.force,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result.get('passed') else 1


if __name__ == '__main__':
    raise SystemExit(main())
