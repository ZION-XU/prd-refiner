#!/usr/bin/env python3
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import subprocess
import sys

from fetch_snapshot import (
    parse_page_id,
    read_pat_token,
    discover_confluence_mcp_config,
    fetch_and_build_snapshot,
    fetch_current_user,
    create_ssl_context,
)
from unittest.mock import MagicMock
import json


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


if __name__ == '__main__':
    unittest.main()
