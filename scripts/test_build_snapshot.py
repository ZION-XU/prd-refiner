#!/usr/bin/env python3
import base64
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from build_snapshot import (
    create_snapshot_from_data,
    extract_filename_from_target,
    extract_referenced_filenames,
    rewrite_image_paths_to_local,
)


PNG = base64.b64decode(
    'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII=')


class SnapshotTests(unittest.TestCase):
    def test_extracts_supported_forms_and_ignores_fenced_examples(self):
        text = '''
![Remote](https://example.invalid/a.png?version=1)
<img src="b.jpg">
<ac:image><ri:attachment ri:filename="c.png"/></ac:image>
```markdown
![example](not-source.png)
```
'''
        self.assertEqual(extract_referenced_filenames(text), ['a.png', 'b.jpg', 'c.png'])

    def test_encoded_path_is_rejected_and_cannot_escape_assets(self):
        target = 'https://example.invalid/%2E%2E%2Fescape.png'
        self.assertEqual(extract_filename_from_target(target), '')
        with tempfile.TemporaryDirectory() as tmp:
            result = create_snapshot_from_data(
                f'![x]({target})', [], Path(tmp),
                source_metadata={'page_id': '123', 'version': '7'})
            self.assertFalse(result['passed'])
            self.assertEqual(result['unsafe_images'][0]['target'], target)

    def test_rewrites_markdown_html_and_attachment_macro(self):
        text = ('![a](https://example.invalid/a.png) '
                '<img src="https://example.invalid/b.jpg"> '
                '<ac:image><ri:attachment ri:filename="c.png"/></ac:image>')
        rewritten, count = rewrite_image_paths_to_local(
            text, './images', {'a.png', 'b.jpg', 'c.png'})
        self.assertEqual(count, 3)
        self.assertIn('![a](./images/a.png)', rewritten)
        self.assertIn('src="./images/b.jpg"', rewritten)
        self.assertIn('![c.png](./images/c.png)', rewritten)

    def test_rewrite_preserves_comments_and_fenced_examples(self):
        text = ('![active](a.png)\n'
                '<!-- ![comment](a.png) -->\n'
                '```markdown\n![example](a.png)\n```\n')
        rewritten, count = rewrite_image_paths_to_local(text, './images', {'a.png'})
        self.assertEqual(count, 1)
        self.assertIn('![active](./images/a.png)', rewritten)
        self.assertIn('<!-- ![comment](a.png) -->', rewritten)
        self.assertIn('```markdown\n![example](a.png)\n```', rewritten)

    def test_confluence_url_image_is_downloaded_and_rewritten(self):
        text = '<ac:image><ri:url ri:value="https://example.invalid/prototype.png"/></ac:image>'
        self.assertEqual(extract_referenced_filenames(text), ['prototype.png'])
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            image = root / 'prototype.png'
            image.write_bytes(PNG)
            result = create_snapshot_from_data(
                text, [], root, {'prototype.png': image},
                source_metadata={'page_id': '123', 'version': '7'})
            self.assertTrue(result['passed'], result)
            source = Path(result['snapshot_file']).read_text(encoding='utf-8')
            self.assertIn('![prototype.png](./images/prototype.png)', source)

    def test_unknown_confluence_image_macro_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = create_snapshot_from_data(
                '<ac:image><ri:shortcut ri:value="x"/></ac:image>', [], Path(tmp),
                source_metadata={'page_id': '123', 'version': '7'})
            self.assertFalse(result['passed'])
            self.assertTrue(result['unsafe_images'])

    def test_unclosed_confluence_image_macro_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = create_snapshot_from_data(
                '<ac:image><ri:attachment ri:filename="x.png"/>', [], Path(tmp),
                source_metadata={'page_id': '123', 'version': '7'})
            self.assertFalse(result['passed'])
            self.assertTrue(result['unsafe_images'])

    def test_same_name_from_different_pages_fails_closed(self):
        text = ('<ac:image><ri:attachment ri:filename="same.png">'
                '<ri:page ri:content-title="Page A"/></ri:attachment></ac:image>'
                '<ac:image><ri:attachment ri:filename="same.png">'
                '<ri:page ri:content-title="Page B"/></ri:attachment></ac:image>')
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            image = root / 'same.png'
            image.write_bytes(PNG)
            result = create_snapshot_from_data(
                text, [], root, {'same.png': image},
                source_metadata={'page_id': '123', 'version': '7'})
            self.assertFalse(result['passed'])
            self.assertEqual(len(result['ambiguous_images'][0]['sources']), 2)

    def test_missing_or_invalid_image_fails_without_snapshot(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            metadata = {'page_id': '123', 'version': '7'}
            missing = create_snapshot_from_data(
                '![x](missing.png)', [], root, source_metadata=metadata)
            self.assertFalse(missing['passed'])
            self.assertFalse((root / '.assets' / 'manifest.json').exists())
            bad = root / 'bad.png'
            bad.write_text('<html>login</html>', encoding='utf-8')
            invalid = create_snapshot_from_data(
                '![x](bad.png)', [], root, {'bad.png': bad}, source_metadata=metadata)
            self.assertFalse(invalid['passed'])
            self.assertTrue(invalid['invalid_images'])

    def test_complete_snapshot_is_immutable_and_has_manifest(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            image = root / 'screen.png'
            image.write_bytes(PNG)
            result = create_snapshot_from_data(
                '![界面](https://example.invalid/screen.png)',
                [{'title': 'screen.png', 'id': 'att-1'}], root,
                {'screen.png': image},
                source_metadata={'page_id': '123', 'version': '7'})
            self.assertTrue(result['passed'], result)
            snapshot = root / '.assets'
            manifest = json.loads((snapshot / 'manifest.json').read_text(encoding='utf-8'))
            self.assertEqual(manifest['status'], 'complete')
            self.assertEqual(manifest['source']['version'], '7')
            self.assertEqual(manifest['images'][0]['attachment_id'], 'att-1')
            self.assertEqual(len(manifest['images'][0]['sha256']), 64)
            self.assertIn('./images/screen.png', (snapshot / 'source.md').read_text(encoding='utf-8'))
            again = create_snapshot_from_data('', [], root)
            self.assertFalse(again['passed'])

    def test_cli_returns_failure_for_incomplete_snapshot(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / 'source.md'
            source.write_text('![x](missing.png)', encoding='utf-8')
            command = [sys.executable, '-B', str(Path(__file__).with_name('build_snapshot.py')),
                       '--source-file', str(source), '--workspace', str(root),
                       '--page-id', '123', '--page-version', '7']
            result = subprocess.run(command, capture_output=True, encoding='utf-8')
            self.assertEqual(result.returncode, 1, result.stdout)
            self.assertFalse(json.loads(result.stdout)['passed'])


if __name__ == '__main__':
    unittest.main()
