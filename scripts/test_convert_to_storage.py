#!/usr/bin/env python3
"""Unit tests for convert_to_storage.py."""
import tempfile
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET

from convert_to_storage import (
    convert_markdown_to_storage,
    escape_xml_characters,
    main,
    md_to_storage_fragment,
    sanitize_latex,
)
import validate_delivery


ROOT = Path(__file__).resolve().parents[1]
TOC_TEMPLATE = (ROOT / 'assets/confluence-toc.xml').read_text(encoding='utf-8-sig')


class LatexSanitizationTests(unittest.TestCase):
    def test_replaces_comparison_and_arrow_symbols(self):
        self.assertEqual(sanitize_latex('值应 $\\ge 60$ 且 $\\le 100$'), '值应 ≥ 60 且 ≤ 100')
        self.assertEqual(sanitize_latex('流程：起点 $\\to$ 终点'), '流程：起点 → 终点')
        self.assertEqual(sanitize_latex('误差为 $\\pm 0.5$ 米'), '误差为 ± 0.5 米')
        self.assertEqual(sanitize_latex('当 $A \\neq B$ 时'), '当 A ≠ B 时')

    def test_handles_bare_commands_without_delimiters(self):
        self.assertEqual(sanitize_latex('A \\to B'), 'A → B')
        self.assertEqual(sanitize_latex('x \\ge 10'), 'x ≥ 10')


class XmlEscapingTests(unittest.TestCase):
    def test_escapes_non_html_angle_brackets(self):
        self.assertEqual(escape_xml_characters('选择<全部其他值>项'), '选择&lt;全部其他值&gt;项')
        self.assertEqual(escape_xml_characters('数值 < 10 或 > 50'), '数值 &lt; 10 或 &gt; 50')

    def test_preserves_valid_html_tags(self):
        self.assertEqual(escape_xml_characters('换行<br/>并<strong>加粗</strong>'), '换行<br/>并<strong>加粗</strong>')

    def test_escapes_standalone_ampersands(self):
        self.assertEqual(escape_xml_characters('a=1&b=2&c=3'), 'a=1&amp;b=2&amp;c=3')
        self.assertEqual(escape_xml_characters('已经&amp;转义的不重复转义'), '已经&amp;转义的不重复转义')



class StorageConversionTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.workspace = Path(self.temp_dir.name)

    def test_converts_full_markdown_with_anchors_and_links(self):
        markdown = """# 测试功能规格

## 文件信息

| 字段 | 内容 |
|---|---|
| 版本 | 0.1 |

## 目录
[TOC]

## 1. 功能与规则

### <a id="fr-001"></a> 基础测试（FR-001）

- 阈值设定：$\\ge 60$ 像素
- 跳转：[规则定义（BR-001）](#br-001)

| 规则名称 | 规则说明 |
|---|---|
| <a id="br-001"></a> 规则定义（BR-001） | 状态 $\\to$ 完成 |
"""
        storage = convert_markdown_to_storage(markdown, TOC_TEMPLATE, layout='floating')
        wrapped = f'<root xmlns:ac="urn:ac" xmlns:ri="urn:ri">{storage}</root>'
        root = ET.fromstring(wrapped)
        self.assertIsNotNone(root)

        # Check native anchor macro exists
        anchors = [p.text for p in root.iter('{urn:ac}parameter') if p.get('{urn:ac}name') == '']
        self.assertIn('fr-001', anchors)
        self.assertIn('br-001', anchors)

        # Check native link exists
        links = [l.get('{urn:ac}anchor') for l in root.iter('{urn:ac}link')]
        self.assertIn('br-001', links)

        # Check LaTeX was sanitized
        self.assertNotIn('$\\ge', storage)
        self.assertIn('≥ 60', storage)
        self.assertIn('→ 完成', storage)

    def test_cli_execution(self):
        md_file = self.workspace / 'test.md'
        out_file = self.workspace / 'storage.xml'
        md_file.write_text("""# 标题\n## 目录\n[TOC]\n## 1. 正文\n<a id="fr-001"></a> 实体（FR-001）""", encoding='utf-8')

        ret = main([str(md_file), '--output', str(out_file)])
        self.assertEqual(ret, 0)
        self.assertTrue(out_file.is_file())
        self.assertIn('fr-001', out_file.read_text(encoding='utf-8'))

    def test_strips_leading_h1_title(self):
        markdown = """# 页面大标题

文件密级：公开

## 目录
[TOC]

## 1. 章节标题
正文内容
"""
        storage = convert_markdown_to_storage(markdown, TOC_TEMPLATE, layout='floating')
        self.assertNotIn('<h1>页面大标题</h1>', storage)
        self.assertNotIn('页面大标题', storage)
        self.assertIn('文件密级：公开', storage)
        self.assertIn('<h2>1. 章节标题</h2>', storage)

    def test_ordered_lists_and_escaped_pipes_in_tables(self):
        fragment = md_to_storage_fragment(
            "- 无序项 A\n"
            "1. 第一步\n"
            "2. 第二步\n\n"
            "| 提示流 | 选项说明 |\n"
            "|---|---|\n"
            "| 指定下一点或 `[闭合(C)|放弃(U)]` | 支持输入 \\[闭合\\|放弃] 并显示 *斜体* |\n"
        )
        self.assertIn('<ul>\n<li>无序项 A</li>\n</ul>', fragment)
        self.assertIn('<ol>\n<li>第一步</li>\n<li>第二步</li>\n</ol>', fragment)
        self.assertIn('<td>指定下一点或 <code>[闭合(C)|放弃(U)]</code></td>', fragment)
        self.assertIn('<td>支持输入 \\[闭合|放弃] 并显示 <em>斜体</em></td>', fragment)


if __name__ == '__main__':
    unittest.main()
