#!/usr/bin/env python3
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from fetch_snapshot import (
    parse_page_id,
    read_pat_token,
    discover_confluence_mcp_config,
)


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


if __name__ == '__main__':
    unittest.main()
