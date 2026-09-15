"""Synthetic regression cases for actual reference failures, without network writes."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from validate_links import inspect, validate


MARKDOWN = '''# 合成需求
## 2. 范围与边界
- [直线计数（FR-001）](#fr-001)：统计所选直线。
## 3. 功能与交互规格
### 3.1 功能清单
| 功能名称（编号） | 结果 |
|---|---|
| [直线计数（FR-001）](#fr-001) | 显示数量 |
<a id="fr-001"></a>
### 3.2 直线计数（FR-001）
用户点击计数显示数量；详见[计数对象范围（BR-001）](#br-001)。
## 4. 业务规则与异常处理
| 规则名称（编号） | 行为 |
|---|---|
| <a id="br-001"></a>计数对象范围（BR-001） | 仅计直线。 |
## 5. 验收标准
- 混合选择（AC-001）：[直线计数（FR-001）](#fr-001)／[计数对象范围（BR-001）](#br-001)：选择两条直线和一个圆，计数为 2。
'''

STORAGE = '''<h2>2. 范围与边界</h2>
<p><ac:link ac:anchor="fr-001"><ac:plain-text-link-body><![CDATA[直线计数（FR-001）]]></ac:plain-text-link-body></ac:link>：统计直线。</p>
<h2>3. 功能与交互规格</h2>
<ac:structured-macro ac:name="anchor" ac:schema-version="1"><ac:parameter ac:name="">fr-001</ac:parameter></ac:structured-macro>
<h3>直线计数（FR-001）</h3>
<p>详见<ac:link ac:anchor="br-001"><ac:link-body><strong>计数对象范围（BR-001）</strong></ac:link-body></ac:link>。</p>
<h2>4. 业务规则与异常处理</h2>
<table><tbody><tr><th>规则</th><th>行为</th></tr>
<tr><td><ac:structured-macro ac:name="anchor"><ac:parameter ac:name="">br-001</ac:parameter></ac:structured-macro>计数对象范围（BR-001）</td><td>仅计直线。</td></tr>
</tbody></table>'''


class ReferenceTests(unittest.TestCase):
    def location_document(self):
        return MARKDOWN.replace('[直线计数（FR-001）](#fr-001)',
                                '〔直线计数（FR-001）；位置：3. 功能与交互规格〕').replace(
                                    '[计数对象范围（BR-001）](#br-001)',
                                    '〔计数对象范围（BR-001）；位置：4. 业务规则与异常处理〕')

    def test_location_fallback_requires_explicit_policy(self):
        text = self.location_document()
        self.assertTrue(any('unlinked reference' in f for f in inspect(text)))
        self.assertEqual(inspect(text, reference_policy='location'), [])

    def test_location_fallback_checks_name_definition_and_heading(self):
        text = self.location_document()
        cases = [
            text.replace('〔直线计数（FR-001）', '〔错误名称（FR-001）'),
            text.replace('位置：3. 功能与交互规格', '位置：2. 范围与边界'),
            text.replace('位置：3. 功能与交互规格', '位置：不存在的章节'),
            text.replace('〔直线计数（FR-001）', '〔直线计数（FR-999）'),
            text + '\n## 3. 功能与交互规格\n同名章。',
            text + '\n### 直线计数（FR-001）\n重复定义。',
        ]
        for candidate in cases:
            with self.subTest(candidate=candidate):
                self.assertTrue(inspect(candidate, reference_policy='location'))

    def test_location_mode_does_not_allow_bare_ids_or_broken_links(self):
        for suffix in ('\n引用 FR-001。', '\n直线计数（FR-001）。',
                       '\n[直线计数（FR-001）](#missing)',
                       '\n〔直线计数（FR-001）〕'):
            with self.subTest(suffix=suffix):
                self.assertTrue(inspect(self.location_document() + suffix, reference_policy='location'))

    def test_location_storage_and_exact_subsection(self):
        text = STORAGE + '<p>〔直线计数（FR-001）；位置：3. 功能与交互规格〕</p>'
        self.assertEqual(inspect(text, 'storage', 'location'), [])
        self.assertEqual(inspect(self.location_document().replace(
            '位置：3. 功能与交互规格', '位置：3.2 直线计数（FR-001）'),
            reference_policy='location'), [])

    def test_location_cli_reports_limitation_and_does_not_modify_document(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'prd.md'
            path.write_text(self.location_document(), encoding='utf-8')
            before = path.read_bytes()
            command = [sys.executable, '-B', str(Path(__file__).with_name('validate_links.py')),
                       str(path), '--reference-policy', 'location', '--json']
            output = subprocess.run(command, capture_output=True, encoding='utf-8')
            self.assertEqual(output.returncode, 0, output.stderr)
            result = json.loads(output.stdout)
            self.assertTrue(result['passed'], result)
            self.assertTrue(result['warnings'])
            self.assertEqual(path.read_bytes(), before)

    def assert_finding(self, text, finding, format='markdown'):
        result = inspect(text, format)
        self.assertTrue(any(finding in message for message in result), result)

    def test_valid_markdown_index_scope_rule_and_acceptance(self):
        self.assertEqual(inspect(MARKDOWN), [])

    def test_scope_sentence_bare_id_is_detected(self):
        text = MARKDOWN.replace('[直线计数（FR-001）](#fr-001)：统计所选直线。',
                                '统计所选直线（FR-001）。')
        self.assert_finding(text, 'unlinked reference: FR-001')

    def test_unlinked_named_index_is_not_another_definition(self):
        text = MARKDOWN.replace('| [直线计数（FR-001）](#fr-001) |', '| 直线计数（FR-001） |')
        self.assert_finding(text, 'unlinked reference: FR-001')
        self.assertFalse(any('duplicate definition' in f for f in inspect(text)))

    def test_old_id_first_heading_is_not_accepted_for_output(self):
        self.assert_finding(MARKDOWN.replace('### 3.2 直线计数（FR-001）', '### 3.2 FR-001 直线计数'),
                            'definition must use name (ID)')

    def test_missing_and_duplicate_anchors(self):
        self.assert_finding(MARKDOWN.replace('<a id="fr-001"></a>', ''), 'missing or ambiguous anchor: fr-001')
        self.assert_finding(MARKDOWN + '\n<a id="fr-001"></a>', 'duplicate anchor: fr-001')

    def test_wrong_definition_and_index_target(self):
        self.assert_finding(MARKDOWN.replace('](#br-001)', '](#fr-001)'),
                            'anchor does not locate definition BR-001')
        text = MARKDOWN.replace('<a id="fr-001"></a>', '')
        text = text.replace('### 3.1 功能清单', '<a id="fr-001"></a>\n### 3.1 功能清单')
        self.assert_finding(text, 'anchor does not locate definition FR-001')

    def test_heading_fallback_for_rule_table(self):
        text = MARKDOWN.replace('](#br-001)', '](#4-业务规则与异常处理)')
        self.assertEqual(inspect(text), [])

    def test_unrelated_section_fallback_fails(self):
        text = MARKDOWN.replace('](#br-001)', '](#2-范围与边界)')
        self.assert_finding(text, 'anchor does not locate definition BR-001')

    def test_function_reference_cannot_fall_back_to_entire_function_chapter(self):
        self.assert_finding(MARKDOWN.replace('](#fr-001)', '](#3-功能与交互规格)'),
                            'anchor does not locate definition FR-001')

    def test_changed_name_requires_updating_reference_labels(self):
        text = MARKDOWN.replace('### 3.2 直线计数（FR-001）', '### 3.2 选择集计数（FR-001）')
        self.assert_finding(text, 'reference name differs from definition: FR-001')
        self.assertEqual(inspect(text.replace('[直线计数（FR-001）]', '[选择集计数（FR-001）]')), [])

    def test_reference_style_links_and_percent_encoded_target(self):
        text = MARKDOWN.replace('[直线计数（FR-001）](#fr-001)', '[直线计数（FR-001）][function]')
        text += '\n[function]: #fr-001\n'
        self.assertEqual(inspect(text), [])
        text = MARKDOWN.replace('[直线计数（FR-001）](#fr-001)', '[直线计数（FR-001)][]')
        text += '\n[直线计数（FR-001)]: #fr-001\n'
        self.assertEqual(inspect(text), [])
        text = MARKDOWN.replace('](#br-001)', '](#4-%E4%B8%9A%E5%8A%A1%E8%A7%84%E5%88%99%E4%B8%8E%E5%BC%82%E5%B8%B8%E5%A4%84%E7%90%86)')
        self.assertEqual(inspect(text), [])

    def test_undefined_reference_label_is_not_success(self):
        self.assert_finding(MARKDOWN.replace('](#br-001)', '][missing]'), 'unsupported reference target')

    def test_bare_or_multiple_ids_in_link_label(self):
        self.assert_finding(MARKDOWN.replace('[直线计数（FR-001）]', '[FR-001]'), 'reference must use one name')
        self.assert_finding(MARKDOWN.replace('[直线计数（FR-001）]', '[FR-001、BR-001]'), 'reference must use one name')

    def test_code_images_history_and_external_source_ids_are_exempt(self):
        text = MARKDOWN + '''
`BR-999` 是代码示例。
```markdown
[错误（BR-999）](#missing)
<a id="fr-001"></a>
```
![FR-999](https://example.invalid/image.png)
原 BR-888 已迁移。
## 版本修订记录
| v1 | 废弃 FR-999，更新 FR-001 |
## 9. 来源与参考资料
| 合成输入（SRC-001） | 外部稿的 FR-999、BR-999 |
'''
        self.assertEqual(inspect(text), [])
        self.assert_finding(text + '\n## 补充\n当前 BR-999。', 'unlinked reference: BR-999')

    def test_front_revision_does_not_hide_later_references(self):
        text = '版本修订记录：\n| v1 | BR-999 |\n\n当前 BR-998。\n' + MARKDOWN
        self.assert_finding(text, 'unlinked reference: BR-998')
        self.assertFalse(any('BR-999' in x for x in inspect(text)))

    def test_external_link_is_not_treated_as_verified_local_target(self):
        self.assert_finding(MARKDOWN.replace('](#fr-001)', '](https://example.invalid/#fr-001)'),
                            'unsupported reference target')

    def test_storage_anchor_macros_and_table_targets(self):
        self.assertEqual(inspect(STORAGE, 'storage'), [])

    def test_storage_missing_target_and_plain_references(self):
        self.assert_finding(STORAGE.replace('>fr-001</ac:parameter>', '>missing</ac:parameter>'),
                            'missing or ambiguous anchor: fr-001', 'storage')
        self.assert_finding(STORAGE + '<p>引用 BR-001。</p>', 'unlinked reference: BR-001', 'storage')

    def test_storage_wrong_anchor_and_external_page_context(self):
        self.assert_finding(STORAGE.replace('ac:anchor="br-001"', 'ac:anchor="fr-001"'),
                            'anchor does not locate definition BR-001', 'storage')
        text = STORAGE.replace('<ac:link ac:anchor="fr-001">',
                               '<ac:link ac:anchor="fr-001"><ri:page ri:content-title="Other"/>')
        self.assert_finding(text, 'unsupported reference target', 'storage')

    def test_storage_does_not_assume_markdown_heading_hash(self):
        self.assert_finding(STORAGE.replace('ac:anchor="br-001"', 'ac:anchor="4-业务规则与异常处理"'),
                            'missing or ambiguous anchor', 'storage')

    def test_storage_code_toc_and_entities(self):
        text = STORAGE + '''<p>测试&nbsp;文本 &amp; 数据。</p>
<ac:structured-macro ac:name="code"><ac:plain-text-body><![CDATA[BR-999]]></ac:plain-text-body></ac:structured-macro>
<ac:structured-macro ac:name="toc"/>'''
        self.assertEqual(inspect(text, 'storage'), [])

    def test_anchor_uses_unnamed_parameter_not_rendering_metadata(self):
        text = STORAGE.replace('<ac:parameter ac:name="">fr-001',
                               '<ac:parameter ac:name="atlassian-macro-output-type">INLINE</ac:parameter><ac:parameter ac:name="">fr-001')
        self.assertEqual(inspect(text, 'storage'), [])

    def test_commented_links_and_anchors_are_not_active_content(self):
        text = MARKDOWN + '\n<!-- [错误（BR-999）](#missing)\n<a id="fr-001"></a> -->'
        self.assertEqual(inspect(text), [])

    def test_profiles_cli_read_only_and_controlled_parse_error(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'prd.md'
            path.write_text(MARKDOWN + '\n引用 BR-001。', encoding='utf-8')
            before = path.read_bytes()
            self.assertFalse(validate(path)['passed'])
            for profile in ('draft', 'existing'):
                result = validate(path, profile=profile)
                self.assertTrue(result['passed'])
                self.assertTrue(result['warnings'])
            command = [sys.executable, '-B', str(Path(__file__).with_name('validate_links.py')), str(path), '--json']
            output = subprocess.run(command, capture_output=True, encoding='utf-8')
            self.assertEqual(output.returncode, 1)
            self.assertFalse(json.loads(output.stdout)['passed'])
            self.assertEqual(path.read_bytes(), before)
            path.write_text('<h2>broken', encoding='utf-8')
            self.assertFalse(validate(path, 'storage')['passed'])
            path.write_text('<!DOCTYPE x><h2>test</h2>', encoding='utf-8')
            self.assertFalse(validate(path, 'storage')['passed'])
            self.assertFalse(validate(path.parent / 'absent.md')['passed'])


if __name__ == '__main__':
    unittest.main()
