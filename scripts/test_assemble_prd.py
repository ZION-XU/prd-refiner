#!/usr/bin/env python3
"""Unit tests for assemble_prd.py (sharded PRD assembly & Nova-Proto HTML auditing)."""
from pathlib import Path
import tempfile
import unittest

import assemble_prd


class AssemblePrdTests(unittest.TestCase):
    def test_audit_passes_official_and_draft_cad_components(self):
        with tempfile.TemporaryDirectory() as tmp:
            proto = Path(tmp) / 'prototype.html'
            proto.write_text(
                '<cad-dialog title="插入表格">\n'
                '  <cad-input label="行数" value="4"></cad-input>\n'
                '  <cad-linetype-preview status="draft" label="线型实时预览"></cad-linetype-preview>\n'
                '  <cad-button type="primary">确定</cad-button>\n'
                '</cad-dialog>',
                encoding='utf-8',
            )
            report = assemble_prd.audit_prototype_html(proto, fr_id='FR-001')
            self.assertTrue(report['passed'])
            self.assertEqual(report['official_count'], 3)
            self.assertEqual(report['draft_count'], 1)
            self.assertEqual(report['raw_count'], 0)
            self.assertEqual(report['draft_components'][0]['tag'], 'cad-linetype-preview')

    def test_audit_rejects_raw_html_interactive_controls(self):
        with tempfile.TemporaryDirectory() as tmp:
            proto = Path(tmp) / 'prototype.html'
            proto.write_text(
                '<cad-dialog title="测试">\n'
                '  <input type="text" value="bad" />\n'
                '  <button>原生按钮</button>\n'
                '</cad-dialog>',
                encoding='utf-8',
            )
            report = assemble_prd.audit_prototype_html(proto, fr_id='FR-001')
            self.assertFalse(report['passed'])
            self.assertEqual(report['raw_count'], 2)

    def test_assemble_merges_shards_and_writes_missing_components(self):
        with tempfile.TemporaryDirectory() as tmp:
            ws = Path(tmp)
            overview = ws / '00_需求总览.md'
            overview.write_text(
                '# 表格重构 用户需求规格说明书\n\n'
                '## 1. 背景、用户与目标\n\n'
                '## 2. 范围与边界\n\n'
                '## 3. 功能与交互规格\n\n'
                '### 3.1 功能清单\n\n'
                '<!-- FEATURES_INSERT_POINT -->\n\n'
                '## 6. 风险与开放问题\n\n'
                '## 7. 来源与参考资料\n',
                encoding='utf-8',
            )
            f1 = ws / 'features' / 'FR-001_创建表格'
            f2 = ws / 'features' / 'FR-002_视口粘贴'
            f1.mkdir(parents=True)
            f2.mkdir(parents=True)

            (f1 / 'prototype.html').write_text(
                '<cad-dialog title="创建"><cad-custom-grid status="draft" label="网格预览器"></cad-custom-grid></cad-dialog>',
                encoding='utf-8',
            )
            (f1 / 'spec.md').write_text(
                '### 创建表格（FR-001）\n\n![S1](../../.assets/images/fr-001-s1.png)',
                encoding='utf-8',
            )
            (f2 / 'prototype.html').write_text(
                '<cad-dialog title="粘贴"><cad-button>确定</cad-button></cad-dialog>',
                encoding='utf-8',
            )
            (f2 / 'spec.md').write_text(
                '### 视口粘贴（FR-002）\n\n交互卡：未涉及（后台剪贴板解析）',
                encoding='utf-8',
            )

            out = ws / '表格重构.md'
            res = assemble_prd.assemble(ws, output=out)
            self.assertTrue(res['passed'], res['errors'])
            merged = out.read_text(encoding='utf-8')
            self.assertIn('### 创建表格（FR-001）', merged)
            self.assertIn('### 视口粘贴（FR-002）', merged)
            self.assertIn('![S1](.assets/images/fr-001-s1.png)', merged)
            self.assertLess(merged.index('FR-001'), merged.index('FR-002'))

            missing_file = ws / 'Missing_Components.md'
            self.assertTrue(missing_file.is_file())
            self.assertIn('cad-custom-grid', missing_file.read_text(encoding='utf-8'))


if __name__ == '__main__':
    unittest.main()
