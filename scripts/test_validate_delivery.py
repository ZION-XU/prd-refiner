"""Synthetic regressions for the three observed delivery failures; no network writes."""
import json
import re
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from test_validate_links import MARKDOWN, STORAGE
from test_validate_prd import COMPLETE
from validate_delivery import inspect_toc, validate

LAYOUT = (Path(__file__).resolve().parents[1] / 'assets/confluence-toc.xml').read_text(encoding='utf-8')
TOC = re.search(r'<div class="zwFloatingTocRight">[\s\S]*?</div>', LAYOUT)[0]
MD = (COMPLETE.split('## 目录')[0] + '## 1. 背景、用户与目标\n核对直线。\n' + MARKDOWN +
      '\n## 8. 风险与开放问题\n暂无。\n## 9. 来源与参考资料\n本轮合成输入。\n')
CHAPTERS = ('<h2>目录</h2>' + STORAGE +
            '<h2>5. 验收标准</h2><ul><li>混合选择（AC-001）：计数为 2。</li></ul>')
BODY = LAYOUT.replace('{{FRONT_MATTER_STORAGE}}', '<p>合成文档信息</p>').replace('{{BODY_STORAGE}}', CHAPTERS)


class DeliveryTests(unittest.TestCase):
    def test_source_images_checked_in_both_outputs_and_remote_only(self):
        source = self.root / 'source.html'
        source.write_text('<img src="https://example.invalid/prototype.png"/>', encoding='utf-8')
        result = self.check(source=source)
        self.assertFalse(result['passed'])
        self.assertEqual(result['markdown_image_comparison']['output_references'], 0)
        self.assertEqual(result['storage_image_comparison']['output_references'], 0)
        self.assertFalse(validate(self.xml, self.root, remote_only=True, source=source)['passed'])

    def test_markdown_images_lost_during_storage_conversion_are_detected(self):
        self.md.write_text(MD + '\n![prototype](https://example.invalid/a.png)', encoding='utf-8')
        result = self.check(image_policy='external')
        self.assertFalse(result['passed'])
        self.assertEqual(result['format_image_comparison']['source_references'], 1)
        self.assertTrue(any('output has none' in e for e in result['errors']))
        self.xml.write_text(BODY + '<ac:image><ri:attachment ri:filename="a.png"/></ac:image>', encoding='utf-8')
        self.assertTrue(self.check(image_policy='external')['passed'])

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.md = self.root / '需求.md'
        self.xml = self.root / 'submitted.xml'
        self.md.write_text(MD, encoding='utf-8')
        self.xml.write_text(BODY, encoding='utf-8')

    def check(self, **kwargs):
        return validate(self.xml, self.root, **({'markdown': self.md} | kwargs))

    def test_valid_pair_is_static_only_and_read_only(self):
        before = (self.md.read_bytes(), self.xml.read_bytes())
        result = self.check()
        self.assertTrue(result['passed'], result)
        self.assertEqual(result['rendered'], 'unverified')
        self.assertEqual(before, (self.md.read_bytes(), self.xml.read_bytes()))

    def test_location_policy_reaches_markdown_and_storage_checks(self):
        note = '〔直线计数（FR-001）；位置：3. 功能与交互规格〕'
        self.md.write_text(MD.replace('[直线计数（FR-001）](#fr-001)', note), encoding='utf-8')
        self.xml.write_text(BODY + '<p>' + note + '</p>', encoding='utf-8')
        self.assertFalse(self.check()['passed'])
        result = self.check(reference_policy='location')
        self.assertTrue(result['passed'], result)
        self.assertTrue(result['warnings'])
        self.assertEqual(result['rendered'], 'unverified')
        self.xml.write_text(BODY + '<p>' + note.replace('3. 功能与交互规格', '2. 范围与边界') + '</p>', encoding='utf-8')
        self.assertFalse(self.check(reference_policy='location')['passed'])

    def test_converter_heading_slug_does_not_match_short_id(self):
        self.xml.write_text(BODY.replace('>fr-001</ac:parameter>', '>直线计数fr-001</ac:parameter>'), encoding='utf-8')
        result = self.check()
        self.assertFalse(result['passed'])
        self.assertTrue(any('missing or ambiguous anchor: fr-001' in e for e in result['errors']))

    def test_missing_table_rule_anchor_fails(self):
        self.xml.write_text(BODY.replace('>br-001</ac:parameter>', '>规则标题</ac:parameter>'), encoding='utf-8')
        self.assertFalse(self.check()['passed'])

    def test_html_anchor_is_not_a_native_macro(self):
        native = '<ac:structured-macro ac:name="anchor" ac:schema-version="1"><ac:parameter ac:name="">fr-001</ac:parameter></ac:structured-macro>'
        self.xml.write_text(BODY.replace(native, '<a id="fr-001"></a>'), encoding='utf-8')
        self.assertTrue(any('native anchor macro: fr-001' in e for e in self.check()['errors']))

    def test_html_link_is_not_a_native_reference(self):
        native = '<ac:link ac:anchor="fr-001"><ac:plain-text-link-body><![CDATA[直线计数（FR-001）]]></ac:plain-text-link-body></ac:link>'
        self.xml.write_text(BODY.replace(native, '<a href="#fr-001">直线计数（FR-001）</a>'), encoding='utf-8')
        self.assertTrue(any('native ac:link' in e for e in self.check()['errors']))

    def test_code_examples_do_not_change_definition_parity(self):
        self.md.write_text(MD + '\n```markdown\n### 示例（FR-999）\n```\n', encoding='utf-8')
        self.assertTrue(self.check()['passed'])

    def test_confluence_code_and_noformat_macros_fail_delivery(self):
        for name in ('code', 'noformat'):
            with self.subTest(macro=name):
                text = BODY + '<ac:structured-macro ac:name="' + name + '"><ac:plain-text-body><![CDATA[ASCII diagram]]></ac:plain-text-body></ac:structured-macro>'
                self.xml.write_text(text, encoding='utf-8')
                result = self.check()
                self.assertTrue(any('avoid code/noformat' in e for e in result['errors']))

    def test_native_diagram_and_inline_code_remain_allowed(self):
        text = BODY + '<table><tbody><tr><th>用户活动</th></tr><tr><td>选择对象并计数</td></tr></tbody></table><p>命令：<code>COUNT</code></p>'
        self.xml.write_text(text, encoding='utf-8')
        self.assertTrue(self.check()['passed'])

    def test_plain_list_and_standalone_toc_are_not_floating_collapsible(self):
        for replacement in ('<ul><li>范围</li></ul>',
                            '<ac:structured-macro ac:name="toc"><ac:parameter ac:name="minLevel">2</ac:parameter><ac:parameter ac:name="maxLevel">3</ac:parameter></ac:structured-macro>'):
            with self.subTest(replacement=replacement):
                self.xml.write_text(BODY.replace(TOC, replacement), encoding='utf-8')
                self.assertFalse(self.check()['passed'])

    def test_original_inline_and_editor_stripped_versions_both_fail(self):
        for style in ('position: fixed; top: 120px; right: 20px; width: 280px;', 'width: 280px;'):
            with self.subTest(style=style):
                old = TOC.replace('<div class="zwFloatingTocRight">',
                                  '<div class="zwFloatingTocRight" style="' + style + '">') + CHAPTERS
                self.xml.write_text(old, encoding='utf-8')
                self.assertFalse(self.check()['passed'])

    def test_inline_coordinates_are_rejected_even_in_correct_layout(self):
        self.xml.write_text(BODY.replace('<div class="zwFloatingTocRight">',
                                        '<div class="zwFloatingTocRight" style="top: 120px; right: 20px;">'), encoding='utf-8')
        self.assertTrue(any('inline positioning' in e for e in self.check()['errors']))

    def test_floating_group_must_be_in_right_cell(self):
        text = ('<ac:layout><ac:layout-section ac:type="two_right_sidebar">'
                '<ac:layout-cell>' + TOC + '</ac:layout-cell><ac:layout-cell><p>信息</p></ac:layout-cell>'
                '</ac:layout-section><ac:layout-section ac:type="single"><ac:layout-cell>' +
                CHAPTERS + '</ac:layout-cell></ac:layout-section></ac:layout>')
        self.assertTrue(any('right cell' in e for e in inspect_toc(text)))

    def test_main_body_cannot_stay_in_sidebar_layout(self):
        text = BODY.replace('ac:type="single"', 'ac:type="two_right_sidebar"')
        self.assertTrue(any('full-width' in e for e in inspect_toc(text)))
        text = BODY.replace(CHAPTERS, '').replace('合成文档信息', CHAPTERS)
        self.assertTrue(any('document chapters' in e for e in inspect_toc(text)))

    def test_floating_class_on_inner_toc_does_not_float_expand_button(self):
        text = BODY.replace('class="zwFloatingTocRight"', '').replace(
            '<ac:parameter ac:name="minLevel">',
            '<ac:parameter ac:name="class">zwFloatingTocRight</ac:parameter><ac:parameter ac:name="minLevel">')
        self.assertTrue(any('entire expand/toc' in e for e in inspect_toc(text)))

    def test_editor_cursor_paragraphs_do_not_break_native_layout(self):
        text = BODY.replace('<div class="zwFloatingTocRight">',
                            '<div class="zwFloatingTocRight"><p class="auto-cursor-target"><br/></p>')
        self.assertEqual(inspect_toc(text), [])

    def test_unreplaced_front_matter_placeholder_fails(self):
        text = BODY.replace('<p>合成文档信息</p>', '{{FRONT_MATTER_STORAGE}}')
        self.assertTrue(any('placeholders' in e for e in inspect_toc(text)))

    def test_sanitized_expand_and_duplicate_toc_fail(self):
        for text in (BODY.replace('ac:name="expand"', 'ac:name="panel"'), BODY + TOC):
            self.xml.write_text(text, encoding='utf-8')
            self.assertFalse(self.check()['passed'])

    def test_missing_and_empty_local_markdown_fail(self):
        self.assertFalse(self.check(markdown=None)['passed'])
        self.md.unlink()
        self.assertFalse(self.check()['passed'])
        self.md.write_text('', encoding='utf-8')
        self.assertFalse(self.check()['passed'])

    def test_hidden_artifact_is_not_local_delivery(self):
        hidden = self.root / '.artifacts'
        hidden.mkdir()
        artifact = hidden / '需求.md'
        artifact.write_text(MD, encoding='utf-8')
        result = self.check(markdown=artifact, output_dir=hidden)
        self.assertTrue(any('hidden artifact' in e for e in result['errors']))

    def test_explicit_folder_and_remote_only_exceptions(self):
        folder = self.root / '交付'
        folder.mkdir()
        output = folder / '需求.md'
        output.write_text(MD, encoding='utf-8')
        self.assertFalse(self.check(markdown=output)['passed'])
        self.assertTrue(self.check(markdown=output, output_dir=folder)['passed'])
        self.assertTrue(self.check(markdown=None, remote_only=True)['passed'])
        self.assertFalse(self.check(remote_only=True)['passed'])

    def test_explicit_inline_choice_does_not_prove_floating(self):
        self.xml.write_text(TOC.replace('class="zwFloatingTocRight"', '') + CHAPTERS, encoding='utf-8')
        result = self.check(layout='inline')
        self.assertTrue(result['passed'], result)
        self.assertEqual(result['rendered'], 'unverified')

    def test_stale_local_definition_set_fails(self):
        self.md.write_text(MD.replace('AC-001', 'AC-002'), encoding='utf-8')
        result = self.check()
        self.assertTrue(any('definition IDs differ' in e for e in result['errors']))

    def test_local_unlinked_reference_fails_even_with_valid_remote(self):
        self.md.write_text(MD.replace('[直线计数（FR-001）](#fr-001)', '直线计数（FR-001）'), encoding='utf-8')
        self.assertFalse(self.check()['passed'])

    def test_directory_heading_exclusion_and_levels(self):
        self.assertEqual(inspect_toc(BODY), [])
        self.assertTrue(inspect_toc(BODY.replace('^目录$', '')))
        self.assertTrue(inspect_toc(BODY.replace('>2</ac:parameter>', '>9</ac:parameter>')))

    def test_empty_malformed_or_external_entity_storage_fails(self):
        for body in ('', '<h2>', '<!DOCTYPE root SYSTEM "file:///private"><p>x</p>'):
            with self.subTest(body=body):
                self.xml.write_text(body, encoding='utf-8')
                self.assertFalse(self.check()['passed'])

    def test_cli_returns_failure_when_local_file_is_missing(self):
        script = Path(__file__).with_name('validate_delivery.py')
        result = subprocess.run([sys.executable, '-B', str(script), str(self.xml),
                                 '--workspace', str(self.root)], capture_output=True, encoding='utf-8')
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertFalse(json.loads(result.stdout)['passed'])


if __name__ == '__main__':
    unittest.main()
