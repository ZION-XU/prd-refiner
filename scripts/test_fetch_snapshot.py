#!/usr/bin/env python3
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import subprocess
import sys

from fetch_snapshot import (
    build_auth_headers,
    create_ssl_context,
    discover_atlassian_mcp_config,
    discover_confluence_mcp_config,
    extract_mcp_env_maps,
    fetch_and_build_snapshot,
    fetch_current_user,
    fetch_page_content,
    parse_custom_headers,
    parse_jira_issue_key,
    parse_page_id,
    read_pat_token,
)
from unittest.mock import MagicMock
import json
import urllib.error


class FetchSnapshotTests(unittest.TestCase):
    def test_parse_page_id(self):
        self.assertEqual(parse_page_id('272269546'), '272269546')
        self.assertEqual(parse_page_id('https://confluence.zwcad.com/pages/viewpage.action?pageId=272269546'), '272269546')
        self.assertEqual(parse_page_id('https://confluence.zwcad.com/pages/272269546/My+Title'), '272269546')
        self.assertEqual(parse_page_id('https://example.com/wiki/spaces/GEO/pages/123456789'), '123456789')

    def test_read_pat_token_file_directive(self):
        with tempfile.NamedTemporaryFile('w', encoding='utf-8', delete=False) as f:
            f.write('secret_pat_123\n')
            temp_name = f.name
        try:
            token = read_pat_token(f'{temp_name}')
            self.assertEqual(token, 'secret_pat_123')
            token2 = read_pat_token(f'{{file:{temp_name}}}')
            self.assertEqual(token2, 'secret_pat_123')
        finally:
            Path(temp_name).unlink(missing_ok=True)

    def test_discover_confluence_mcp_config_env(self):
        with patch.dict('os.environ', {'CONFLUENCE_PERSONAL_TOKEN': 'mock_token', 'CONFLUENCE_URL': 'https://mock.com'}):
            url, token, src = discover_confluence_mcp_config()
            self.assertEqual(url, 'https://mock.com')
            self.assertEqual(token, 'mock_token')
            self.assertEqual(src, 'environment variable')

    @patch('urllib.request.urlopen')
    def test_fetch_current_user_success(self, mock_urlopen):
        mock_resp = MagicMock()
        mock_resp.read.return_value = json.dumps({
            'username': 'xuzhou',
            'displayName': '徐舟',
            'userKey': 'key_123'
        }).encode('utf-8')
        mock_urlopen.return_value.__enter__.return_value = mock_resp

        user = fetch_current_user('https://mock.confluence.com', 'fake_pat', create_ssl_context())
        self.assertEqual(user['username'], 'xuzhou')
        self.assertEqual(user['display_name'], '徐舟')
        self.assertEqual(user['user_key'], 'key_123')

    @patch('urllib.request.urlopen')
    def test_fetch_current_user_error(self, mock_urlopen):
        mock_urlopen.side_effect = Exception('Network error')
        user = fetch_current_user('https://mock.confluence.com', 'fake_pat', create_ssl_context())
        self.assertEqual(user, {})

    def test_force_overwrites_snapshot_files_only(self):
        # `.assets/` is shared and flat: forcing a fresh snapshot must not delete
        # Storage bodies, rendered diagrams or any other machine asset.
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            assets = root / '.assets'
            (assets / 'images').mkdir(parents=True)
            for name in ('manifest.json', 'source.md', 'source.original.txt'):
                (assets / name).write_text('stale', encoding='utf-8')
            storage = assets / 'page.storage.html'
            storage.write_text('submitted body', encoding='utf-8')
            rendered = assets / 'images' / 'mermaid-abc123.png'
            rendered.write_bytes(b'\x89PNG\r\n\x1a\n')

            with patch('fetch_snapshot.discover_confluence_mcp_config',
                       return_value=('https://mock.invalid', '', 'none')):
                result = fetch_and_build_snapshot('123', root, force=True)

            self.assertFalse(result['passed'])  # no PAT configured in this test
            self.assertFalse((assets / 'manifest.json').exists())
            self.assertFalse((assets / 'source.md').exists())
            self.assertTrue(storage.is_file())
            self.assertTrue(rendered.is_file())

    def test_cli_refuses_to_infer_the_workspace(self):
        # Omitting --workspace used to fall back to the current directory, which
        # would drop the snapshot into the skill checkout instead of the
        # requirement workspace.
        with tempfile.TemporaryDirectory() as tmp:
            command = [sys.executable, '-B', str(Path(__file__).with_name('fetch_snapshot.py')),
                       '--page-id', '272269546']
            result = subprocess.run(command, capture_output=True, encoding='utf-8', cwd=tmp)
            self.assertEqual(result.returncode, 2)
            self.assertIn('--workspace', result.stderr)
            self.assertFalse((Path(tmp) / '.assets').exists())

    def test_parse_jira_issue_key(self):
        self.assertEqual(parse_jira_issue_key('ZWCAD-12345'), 'ZWCAD-12345')
        self.assertEqual(parse_jira_issue_key('https://jira.zwcad.com/browse/ZWCAD-12345'), 'ZWCAD-12345')
        self.assertEqual(parse_jira_issue_key('https://jira.example.com/projects/CAD/issues/CAD-99?filter=all'), 'CAD-99')
        self.assertIsNone(parse_jira_issue_key('272269546'))
        self.assertIsNone(parse_jira_issue_key('https://confluence.zwcad.com/pages/viewpage.action?pageId=272269546'))

    def test_extract_mcp_env_from_toml_and_cli_args(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            toml_path = root / 'config.toml'
            toml_path.write_text(
                '[mcp_servers.atlassian]\n'
                'command = "mcp-atlassian"\n'
                'args = ["--confluence-url", "https://intranet.example.com", "--no-confluence-ssl-verify"]\n'
                '[mcp_servers.atlassian.env]\n'
                'CONFLUENCE_USERNAME = "alice"\n'
                'CONFLUENCE_API_TOKEN = "basic_tok_999"\n'
                'CONFLUENCE_CUSTOM_HEADERS = "User-Agent=mcp-atlassian/1.0, X-Gateway=intranet"\n',
                encoding='utf-8',
            )
            maps = extract_mcp_env_maps(toml_path)
            self.assertEqual(len(maps), 1)
            self.assertEqual(maps[0]['CONFLUENCE_URL'], 'https://intranet.example.com')
            self.assertEqual(maps[0]['CONFLUENCE_USERNAME'], 'alice')
            self.assertEqual(maps[0]['CONFLUENCE_API_TOKEN'], 'basic_tok_999')
            headers = parse_custom_headers(maps[0]['CONFLUENCE_CUSTOM_HEADERS'])
            self.assertEqual(headers['User-Agent'], 'mcp-atlassian/1.0')
            self.assertEqual(headers['X-Gateway'], 'intranet')

    def test_auth_headers_fallback_from_bearer_to_basic_on_401(self):
        candidates = build_auth_headers('my_secret', username='xuzhou', auth_scheme='bearer')
        self.assertEqual(len(candidates), 2)
        self.assertTrue(candidates[0]['Authorization'].startswith('Bearer '))
        self.assertTrue(candidates[1]['Authorization'].startswith('Basic '))

        # Simulate 401 on Bearer and 200 OK on Basic Auth fallback
        ok_resp = MagicMock()
        ok_resp.read.return_value = json.dumps({
            'body': {'storage': {'value': '<p>Body</p>'}},
            'version': {'number': 3},
            'children': {'attachment': {'results': [
                {'id': 'att-1', 'title': 'demo.png', '_links': {'download': '/download/attachments/10/demo.png'}}
            ]}},
        }).encode('utf-8')
        cm = MagicMock()
        cm.__enter__.return_value = ok_resp
        err_401 = urllib.error.HTTPError('https://mock/api', 401, 'Unauthorized', {}, None)

        with patch('urllib.request.urlopen', side_effect=[err_401, cm]) as mock_open:
            content, version, web_url, attachments = fetch_page_content(
                'https://mock.confluence.com', '10', 'my_secret', create_ssl_context(),
                username='xuzhou', auth_scheme='bearer',
            )
            self.assertEqual(mock_open.call_count, 2)
            self.assertEqual(content, '<p>Body</p>')
            self.assertEqual(version, '3')
            self.assertEqual(len(attachments), 1)
            self.assertEqual(attachments[0]['id'], 'att-1')
            self.assertEqual(attachments[0]['download_url'], 'https://mock.confluence.com/download/attachments/10/demo.png')

    def test_jira_issue_snapshot_via_mcp_config(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            issue_payload = {
                'id': '10050',
                'fields': {
                    'summary': '支持动态块夹点拉伸',
                    'updated': '2026-10-23T15:00:00.000+0800',
                    'status': {'name': '处理中'},
                    'issuetype': {'name': 'Story'},
                    'priority': {'name': 'P1'},
                    'reporter': {'displayName': '张三'},
                    'assignee': {'displayName': '李四'},
                    'description': '请参考截图 !grip.png|thumbnail!',
                    'attachment': [
                        {'id': '901', 'filename': 'grip.png', 'content': 'https://jira.mock/secure/attachment/901/grip.png'}
                    ],
                },
            }
            png_bytes = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR' + b'\x00' * 24

            def fake_urlopen(req, context=None, timeout=15):
                resp = MagicMock()
                if '/rest/api/2/issue/ZWCAD-888' in req.full_url:
                    resp.read.return_value = json.dumps(issue_payload).encode('utf-8')
                else:
                    resp.read.return_value = png_bytes
                cm = MagicMock()
                cm.__enter__.return_value = resp
                return cm

            with patch.dict('os.environ', {'JIRA_URL': 'https://jira.mock', 'JIRA_PERSONAL_TOKEN': 'jira_tok'}), \
                 patch('urllib.request.urlopen', side_effect=fake_urlopen):
                result = fetch_and_build_snapshot('https://jira.mock/browse/ZWCAD-888', root)

            self.assertTrue(result['passed'], result)
            source_md = (root / '.assets' / 'source.md').read_text(encoding='utf-8')
            self.assertIn('[ZWCAD-888] 支持动态块夹点拉伸', source_md)
            self.assertIn('![grip.png](./images/grip.png)', source_md)
            self.assertTrue((root / '.assets' / 'images' / 'grip.png').is_file())


if __name__ == '__main__':
    unittest.main()
