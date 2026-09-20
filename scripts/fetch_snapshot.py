#!/usr/bin/env python3
"""Fetch a Confluence page and referenced images directly into a local snapshot.

Automatically discovers Confluence PAT and URL from existing MCP configurations
or environment variables, ensuring zero-token and zero-friction snapshot creation.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
import ssl
import sys
import tempfile
import urllib.error
import urllib.parse
import urllib.request

from build_snapshot import create_snapshot_from_data, extract_referenced_filenames


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


def read_pat_token(token_str_or_path: str) -> str:
    token_str = token_str_or_path.strip()
    m = re.match(r'^\{file:(.+)\}$', token_str)
    if m:
        file_path = Path(m.group(1).strip())
        if file_path.is_file():
            return file_path.read_text(encoding='utf-8').strip()
    if Path(token_str).is_file():
        try:
            return Path(token_str).read_text(encoding='utf-8').strip()
        except OSError:
            pass
    return token_str


def find_mcp_config_candidates(workspace: Path | None = None) -> list[Path]:
    candidates = [
        Path.home() / '.gemini' / 'config' / 'mcp_config.json',
        Path.home() / '.config' / 'opencode' / 'opencode.json',
        Path.home() / '.codeium' / 'windsurf' / 'mcp_config.json',
        Path.home() / '.cursor' / 'mcp.json',
    ]
    cur = (workspace or Path.cwd()).resolve()
    for _ in range(5):
        candidates.extend([cur / '.mcp.json', cur / 'mcp_config.json'])
        if cur.parent == cur:
            break
        cur = cur.parent
    return candidates


def discover_confluence_mcp_config(workspace: Path | None = None) -> tuple[str, str, str]:
    """Return (confluence_url, pat_token, source_description)."""
    env_url = os.environ.get('CONFLUENCE_URL')
    env_token = os.environ.get('CONFLUENCE_PERSONAL_TOKEN') or os.environ.get('CONFLUENCE_PAT')
    if env_token:
        return env_url or 'https://confluence.zwcad.com', read_pat_token(env_token), 'environment variable'

    for p in find_mcp_config_candidates(workspace):
        if not p.is_file():
            continue
        try:
            data = json.loads(p.read_text(encoding='utf-8', errors='ignore'))
            env = (
                data.get('mcpServers', {}).get('atlassian', {}).get('env') or
                data.get('mcp', {}).get('atlassian', {}).get('environment') or
                {}
            )
            raw_url = env.get('CONFLUENCE_URL') or env_url
            raw_token = env.get('CONFLUENCE_PERSONAL_TOKEN') or env.get('CONFLUENCE_PAT')
            if raw_token:
                token = read_pat_token(raw_token)
                if token:
                    return raw_url or 'https://confluence.zwcad.com', token, str(p)
        except Exception:
            continue

    for common_path in [Path('D:/proposal/confluence-PAT.txt'), Path.home() / 'confluence-PAT.txt']:
        if common_path.is_file():
            try:
                token = common_path.read_text(encoding='utf-8').strip()
                if token:
                    return env_url or 'https://confluence.zwcad.com', token, str(common_path)
            except OSError:
                pass

    return env_url or 'https://confluence.zwcad.com', '', 'none'


def create_ssl_context() -> ssl.SSLContext:
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    return ctx


def fetch_page_content(base_url: str, page_id: str, pat: str,
                       ctx: ssl.SSLContext) -> tuple[str, str, str, list[dict]]:
    """Fetch page storage body, version, web URL, and attachment metadata."""
    url = f'{base_url.rstrip("/")}/rest/api/content/{page_id}?expand=body.storage,version,space'
    req = urllib.request.Request(url, headers={'Authorization': f'Bearer {pat}'})
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=15) as resp:
            data = json.loads(resp.read().decode('utf-8'))
    except urllib.error.HTTPError as exc:
        if exc.code == 401:
            raise PermissionError('Confluence PAT authentication failed (401 Unauthorized)') from exc
        if exc.code == 404:
            raise FileNotFoundError(f'Confluence page {page_id} not found (404)') from exc
        raise RuntimeError(f'Failed to fetch page {page_id}: HTTP {exc.code} {exc.reason}') from exc

    content = data.get('body', {}).get('storage', {}).get('value', '')
    version = str(data.get('version', {}).get('number', ''))
    web_url = f'{base_url.rstrip("/")}/pages/viewpage.action?pageId={page_id}'
    attachments = data.get('attachments', [])
    return content, version, web_url, attachments


def fetch_current_user(base_url: str, pat: str, ctx: ssl.SSLContext) -> dict:
    """Fetch current user profile (username, displayName) associated with the PAT."""
    url = f'{base_url.rstrip("/")}/rest/api/user/current'
    req = urllib.request.Request(url, headers={'Authorization': f'Bearer {pat}'})
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            return {
                'username': data.get('username', ''),
                'display_name': data.get('displayName', ''),
                'user_key': data.get('userKey', ''),
            }
    except Exception:
        return {}


def download_attachment_direct(base_url: str, page_id: str, filename: str, pat: str,
                               dest: Path, ctx: ssl.SSLContext) -> bool:
    """Download image directly by filename using Confluence attachment endpoint."""
    encoded_name = urllib.parse.quote(filename)
    urls = [
        f'{base_url.rstrip("/")}/download/attachments/{page_id}/{encoded_name}?api=v2',
        f'{base_url.rstrip("/")}/download/attachments/{page_id}/{encoded_name}',
    ]
    for url in urls:
        req = urllib.request.Request(url, headers={'Authorization': f'Bearer {pat}'})
        try:
            with urllib.request.urlopen(req, context=ctx, timeout=15) as resp:
                dest.write_bytes(resp.read())
                return True
        except Exception:
            continue
    return False


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

    discovered_url, discovered_pat, src_desc = discover_confluence_mcp_config(workspace)
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

    try:
        content, version, web_url, attachments = fetch_page_content(url, page_id, token, ctx)
    except Exception as exc:
        return {
            'passed': False,
            'errors': [f'{type(exc).__name__}: {exc}'],
        }

    author_info = fetch_current_user(url, token, ctx)

    images = extract_referenced_filenames(content)
    missing_downloads = []

    with tempfile.TemporaryDirectory(prefix='prd-snapshot-assets-') as temp_dir:
        temp_path = Path(temp_dir)
        cached_files = {}
        for img in images:
            dest = temp_path / img
            ok = download_attachment_direct(url, page_id, img, token, dest, ctx)
            if ok:
                cached_files[img] = dest
            else:
                missing_downloads.append(img)

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


def main() -> int:
    if hasattr(sys.stdout, 'reconfigure'):
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except Exception:
            pass
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--page-id', required=True, help='Confluence page ID or full page URL')
    parser.add_argument('--workspace', type=Path, default=Path.cwd(), help='Target workspace directory')
    parser.add_argument('--url', help='Confluence base URL (overrides MCP config)')
    parser.add_argument('--pat', help='Confluence PAT (overrides MCP config)')
    parser.add_argument('--pat-file', type=Path, help='File containing Confluence PAT')
    parser.add_argument('--force', action='store_true', help='Overwrite existing snapshot if present')
    args = parser.parse_args()

    page_id = parse_page_id(args.page_id)
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
