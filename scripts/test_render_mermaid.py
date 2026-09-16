"""Unit tests for deterministic Mermaid PNG rendering orchestration."""
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

from render_mermaid import mermaid_asset_stem, mermaid_blocks, process_markdown


PNG = (b'\x89PNG\r\n\x1a\n' + b'\x00\x00\x00\rIHDR' +
       b'\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00' + b'\x00' * 12)


class MermaidRenderTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.markdown = self.root / '需求.md'

    def test_extracts_active_blocks_and_hashes_normalized_source(self):
        source = 'flowchart LR\nA-->B'
        self.markdown.write_text(f'```mermaid\r\n{source}\r\n```\r\n```text\nx\n```',
                                 encoding='utf-8')
        blocks = mermaid_blocks(self.markdown.read_text(encoding='utf-8'))
        self.assertEqual(blocks, [source])
        self.assertRegex(mermaid_asset_stem(source), r'^mermaid-[0-9a-f]{12}$')

    def test_reuses_valid_hash_named_png(self):
        source = 'flowchart LR\nA-->B'
        self.markdown.write_text(f'```mermaid\n{source}\n```', encoding='utf-8')
        target = self.root / 'out'
        target.mkdir()
        (target / f'{mermaid_asset_stem(source)}.png').write_bytes(PNG)
        with patch('render_mermaid.find_renderer') as renderer:
            result = process_markdown(self.markdown, target)
        self.assertEqual(result['status'], 'complete')
        self.assertEqual(result['results'][0]['status'], 'reused')
        renderer.assert_not_called()

    @patch('render_mermaid.find_renderer', return_value=None)
    @patch('render_mermaid.find_browser', return_value='browser')
    def test_missing_renderer_fails_whole_report(self, _browser, _renderer):
        self.markdown.write_text('```mermaid\nflowchart LR\nA-->B\n```', encoding='utf-8')
        result = process_markdown(self.markdown, self.root / 'out')
        self.assertEqual(result['status'], 'failed')
        self.assertEqual(result['results'][0]['status'], 'failed')

    @patch('render_mermaid.find_renderer', return_value=['mmdc'])
    @patch('render_mermaid.find_browser', return_value='browser')
    def test_success_requires_valid_png(self, _browser, _renderer):
        self.markdown.write_text('```mermaid\nflowchart LR\nA-->B\n```', encoding='utf-8')

        def fake_run(command, **_kwargs):
            output = Path(command[command.index('--output') + 1])
            output.write_bytes(PNG)
            return subprocess.CompletedProcess(command, 0, '', '')

        with patch('render_mermaid.subprocess.run', side_effect=fake_run):
            result = process_markdown(self.markdown, self.root / 'out')
        self.assertEqual(result['status'], 'complete')
        self.assertEqual(result['results'][0]['status'], 'rendered')


if __name__ == '__main__':
    unittest.main()
