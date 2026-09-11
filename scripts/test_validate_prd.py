"""Behavioral regression tests; all documents are synthetic, in temporary folders."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from validate_prd import validate


COMPLETE = '''---
status: 初版待核对
---
# 直线计数（合成案例）
## 1. 背景、用户与目标
用户需要核对当前选择集中的直线数量。
## 2. 范围与边界
仅统计直线，不修改对象。
## 3. 功能与交互规格
| 功能 | 内容 |
|---|---|
| FR-001 | 直线计数 |
### FR-001 直线计数
用户点击计数，按 BR-001 显示数量。
## 4. 业务规则与异常处理
| 规则 | 内容 |
|---|---|
| BR-001 | 只统计选择集中的直线；其他对象不计入；没有直线显示 0。 |
## 5. 验收标准
- AC-001：FR-001 / BR-001：选择两条直线和一个圆，点击计数，显示 2；对象不变。
## 8. 风险与开放问题
暂无需要共同判断的事项。
## 9. 核对与版本记录
初版待产品核对；尚未评审。
'''


class ValidatorTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.prd = self.root / '计数初版.md'

    def tearDown(self):
        self.temp.cleanup()

    def run_doc(self, text=COMPLETE, profile='template'):
        self.prd.write_text(text, encoding='utf-8')
        return validate(self.prd, profile)

    def test_complete_output_requires_template_headings(self):
        self.assertTrue(self.run_doc()['passed'])
        for current, historical in [('核对与版本记录', '评审结论与版本记录'),
                                    ('功能与交互规格', '命令与交互规格')]:
            with self.subTest(heading=historical):
                legacy = COMPLETE.replace(current, historical)
                self.assertFalse(self.run_doc(legacy)['passed'])
                self.assertTrue(self.run_doc(legacy, 'existing')['passed'])

    def test_incomplete_draft_saves_with_warnings(self):
        text = '# 计数想法\n目标：核对数量。待确认：对象范围未定，影响计数结果。'
        self.assertTrue(self.run_doc(text, 'draft')['passed'])
        self.assertTrue(self.run_doc(text, 'draft')['warnings'])
        self.assertFalse(self.run_doc(text)['passed'])

    def test_legacy_input_diagnostic_does_not_qualify_output(self):
        text = '# 原格式\n用途：核对选择集。规则：仅计直线；空集为零。'
        result = self.run_doc(text, 'existing')
        self.assertTrue(result['passed'])
        self.assertTrue(result['warnings'])
        before = self.prd.read_bytes()
        self.assertFalse(validate(self.prd, 'template')['passed'])
        self.assertEqual(before, self.prd.read_bytes())

    def test_names_and_unrelated_neighbor_files_are_preserved(self):
        (self.root / 'quality-report.md').write_text('AC-999 为其他项目内容', encoding='utf-8')
        (self.root / 'attachments').mkdir()
        content = COMPLETE + '\n参考 AutoCAD 的说明，未采纳为当前行为。'
        self.run_doc(content)
        before = {p: p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
        self.assertTrue(validate(self.prd)['passed'])
        self.assertEqual(before, {p: p.read_bytes() for p in before})

    def test_open_issue_is_not_template_placeholder(self):
        text = COMPLETE.replace('暂无需要共同判断的事项。', '- DEC-001：显示位置待确认，影响 FR-001 布局。')
        self.assertTrue(self.run_doc(text)['passed'])
        self.assertFalse(self.run_doc(text + '\n{需求名称}')['passed'])

    def test_json_math_html_and_code_examples_are_not_placeholders(self):
        text = COMPLETE + '\n公式 x < y，集合 {a,b}，示例 <kbd>Enter</kbd>。\n```json\n{"FR-999": "{填写}"}\n```\n'
        self.assertTrue(self.run_doc(text)['passed'])

    def test_dangling_and_duplicate_ids(self):
        self.assertFalse(self.run_doc(COMPLETE + '\n参考 BR-999。')['passed'])
        self.assertFalse(self.run_doc(COMPLETE + '\n- BR-001：另一个规则。')['passed'])

    def test_table_and_formatted_definitions(self):
        text = '# 旧稿\n| 功能 | 规则 |\n|---|---|\n| FR-002 | 计数 |\n- **BR-002**：FR-002 只计直线。\n- `AC-002`：BR-002 空集为零。'
        self.assertTrue(self.run_doc(text, 'existing')['passed'])

    def test_template_lists_are_references_not_definitions(self):
        text = COMPLETE.replace('仅统计直线，不修改对象。',
                                '本期包含：\n  - **FR-001** 直线计数')
        text = text.replace('用户点击计数，按 BR-001 显示数量。',
                            '行为规则与边界：\n  - BR-001：计数规则')
        text = text.replace('暂无需要共同判断的事项。',
                            '| DEC-001 | 显示位置待确认 |')
        text += '\n### 9.1 产品侧核对与后续讨论\n1. `DEC-001`：显示位置\n'
        self.assertTrue(self.run_doc(text)['passed'])

    def test_reference_lists_do_not_define_missing_ids(self):
        for section, reference in [
            ('## 2. 范围与边界', '- FR-999 功能'),
            ('## 3. 功能与交互规格', '- BR-999：规则\n- NFR-999：约束'),
            ('## 9. 核对与版本记录', '1. DEC-999：待确认'),
        ]:
            with self.subTest(section=section):
                result = self.run_doc(COMPLETE.replace(section, section + '\n' + reference))
                self.assertTrue(any('IDs referenced but not defined:' in e
                                    for e in result['errors']))

    def test_real_duplicate_definitions_still_fail(self):
        for definition, section in [
            ('### FR-001 另一个功能', '## 3. 功能与交互规格'),
            ('- BR-001：另一个规则', '## 4. 业务规则与异常处理'),
            ('| BR-001 | 另一个数据规则 |', '## 6. 数据、系统变量与接口'),
            ('- AC-001：另一个验收', '## 5. 验收标准'),
        ]:
            with self.subTest(definition=definition):
                result = self.run_doc(COMPLETE + '\n' + section + '\n' + definition)
                self.assertTrue(any('duplicate ID definition:' in e for e in result['errors']))

    def test_image_references_and_percent_encoded_path(self):
        img = self.root / '界 面.png'
        img.write_bytes(b'synthetic existence fixture; not a rendered image')
        text = COMPLETE + '\n![界面](%E7%95%8C%20%E9%9D%A2.png)\n![另图][preview]\n[preview]: <界 面.png>\n'
        self.assertTrue(self.run_doc(text)['passed'])
        img.unlink()
        self.assertFalse(validate(self.prd)['passed'])

    def test_undefined_image_reference_fails_and_remote_is_unverified(self):
        self.assertFalse(self.run_doc(COMPLETE + '\n![x][missing]')['passed'])
        result = self.run_doc(COMPLETE + '\n![x](https://example.invalid/image.png)')
        self.assertTrue(result['passed'])
        self.assertTrue(result['warnings'])

    def test_missing_or_invalid_file_has_controlled_error(self):
        self.assertFalse(validate(self.root / 'missing.md')['passed'])
        self.prd.write_bytes(b'\xff\xfe\xff')
        self.assertFalse(validate(self.prd)['passed'])

    def test_cli_json_exit_and_directory_compatibility(self):
        (self.root / 'prd.md').write_text(COMPLETE, encoding='utf-8')
        script = Path(__file__).with_name('validate_prd.py')
        command = [sys.executable, str(script), str(self.root), '--json']
        result = subprocess.run(command, capture_output=True, encoding='utf-8')
        self.assertEqual(result.returncode, 0)
        self.assertTrue(json.loads(result.stdout)['passed'])
        result = subprocess.run(command + ['--profile', 'invalid'], capture_output=True)
        self.assertEqual(result.returncode, 2)

    def test_unresolved_template_markers_fail(self):
        for marker in ('## 1. 背景、用户与目标【核心】', '## 6. 数据、系统变量与接口【按需】', '### 3.1 功能清单【多功能时填写】'):
            with self.subTest(marker=marker):
                doc = COMPLETE + '\n' + marker + '\n'
                result = self.run_doc(doc)
                self.assertFalse(result['passed'])
                self.assertTrue(any('unresolved template markers:' in e for e in result['errors']))

    def test_numbered_table_definitions_are_recognized(self):
        doc = COMPLETE.replace(
            '| BR-001 | 只统计选择集中的直线；其他对象不计入；没有直线显示 0。 |',
            '| 序号 | 规则 | 内容 |\n|---|---|---|\n| 1 | BR-001 | 只统计选择集中的直线；其他对象不计入；没有直线显示 0。 |\n| 2 | BR-002 | 另一规则 |'
        )
        doc = doc.replace('## 5. 验收标准', '## 5. 验收标准\n- AC-002：FR-001 / BR-002：测试另规则。')
        result = self.run_doc(doc)
        self.assertTrue(result['passed'])

    def test_historical_and_revision_id_references_are_exempt(self):
        # 1. Historical references in Section 9.2 should not trigger undefined error
        doc_with_revision = COMPLETE + '\n### 9.2 版本修订记录\n- v0.2: 废弃 BR-999，更新 FR-001。\n'
        result = self.run_doc(doc_with_revision)
        self.assertTrue(result['passed'])

        # 2. Historical prefix in prose (e.g. 原 BR-888) should not trigger undefined error
        doc_with_old_ref = COMPLETE + '\n本规则由原 BR-888 重构而来。\n'
        result = self.run_doc(doc_with_old_ref)
        self.assertTrue(result['passed'])


if __name__ == '__main__':
    unittest.main()
