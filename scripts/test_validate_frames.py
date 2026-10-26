#!/usr/bin/env python3
"""Behavioral tests for the frame-closure checker; all fixtures are synthetic."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from validate_frames import inspect


PRD = '''# 合成需求
## 3. 功能与交互规格

### 直线计数（FR-001）

**交互卡（FR-001）**

| 状态 | 触发／输入 | 可见反馈 | 下一状态 |
|---|---|---|---|
| S1 默认态 | 启动命令 | 命令行提示选择对象 | S2 完成 |
| S2 完成 | 点击计数 | 命令行回显数量 | 结束 |

| 帧 ID | 对应状态 | 画面 | 说明 |
|---|---|---|---|
| FR-001-S1 | S1 | ![FR-001-S1](.assets/images/fr-001-s1.png) | 合成示例 |
'''

FRAME = {'id': 'FR-001-S1', 'fr': 'FR-001', 'state': 'S1 默认态',
         'image': '.assets/images/fr-001-s1.png',
         'source': 'excalidraw:frames', 'version': '0.1', 'captured': '2026-10-24'}


class FrameClosureTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / '.assets' / 'images').mkdir(parents=True)
        (self.root / '.assets' / 'frames').mkdir(parents=True)
        (self.root / '.assets' / 'images' / 'fr-001-s1.png').write_bytes(b'nonempty fixture')
        self.prd = self.root / 'prd.md'
        self.prd.write_text(PRD, encoding='utf-8')

    def write_manifest(self, frames):
        path = self.root / '.assets' / 'frames' / 'manifest.json'
        path.write_text(json.dumps({'requirement': '合成需求', 'frames': frames},
                                   ensure_ascii=False), encoding='utf-8')
        return path

    def test_matching_prd_and_manifest_pass(self):
        self.write_manifest([FRAME])
        result = inspect(self.root)
        self.assertTrue(result['passed'], result)
        self.assertEqual(result['counts']['prd_frames'], 1)
        self.assertEqual(result['counts']['manifest_frames'], 1)

    def test_frames_without_manifest_fail(self):
        result = inspect(self.root)
        self.assertFalse(result['passed'])
        self.assertTrue(any('manifest.json is missing' in e for e in result['errors']))

    def test_orphan_and_unregistered_frames_fail(self):
        self.write_manifest([FRAME, dict(FRAME, id='FR-001-S9', state='S9')])
        result = inspect(self.root)
        self.assertFalse(result['passed'])
        self.assertTrue(any('orphan frame' in e for e in result['errors']))
        self.write_manifest([dict(FRAME, id='FR-002-S1', fr='FR-002')])
        result = inspect(self.root)
        self.assertTrue(any('not in manifest' in e for e in result['errors']))
        self.assertTrue(any('does not define' in e for e in result['errors']))

    def test_missing_empty_and_escaping_images_fail(self):
        self.write_manifest([dict(FRAME, image='.assets/images/missing.png')])
        self.assertTrue(any('not found' in e for e in inspect(self.root)['errors']))
        self.write_manifest([dict(FRAME, image='../outside.png')])
        self.assertTrue(any('leaves the workspace' in e for e in inspect(self.root)['errors']))
        self.write_manifest([dict(FRAME, image=str((self.root / '.assets' / 'images' / 'fr-001-s1.png')))] )
        self.assertTrue(any('workspace-relative' in e for e in inspect(self.root)['errors']))

    def test_manifest_schema_and_duplicates_fail(self):
        self.write_manifest([FRAME, FRAME])
        self.assertTrue(any('duplicate frame id' in e for e in inspect(self.root)['errors']))
        self.write_manifest([dict(FRAME, id='fr-1')])
        self.assertTrue(any('must look like FR-001-S1' in e for e in inspect(self.root)['errors']))
        self.write_manifest([{'id': 'FR-001-S1'}])
        self.assertTrue(any('missing or empty' in e for e in inspect(self.root)['errors']))
        (self.root / '.assets' / 'frames' / 'manifest.json').write_text('[]', encoding='utf-8')
        result = inspect(self.root)
        self.assertFalse(result['passed'])

    def test_document_without_frames_needs_no_manifest(self):
        self.prd.write_text('# 合成需求\n## 3. 功能与交互规格\n- 交互卡：未涉及（纯计算）。\n',
                            encoding='utf-8')
        result = inspect(self.root)
        self.assertTrue(result['passed'], result)
        self.assertTrue(result['warnings'])

    def test_missing_prd_is_a_controlled_failure(self):
        self.prd.unlink()
        result = inspect(self.root)
        self.assertFalse(result['passed'])
        self.assertTrue(any('no PRD found' in e for e in result['errors']))

    def test_cli_json_reports_closure(self):
        self.write_manifest([FRAME])
        script = Path(__file__).with_name('validate_frames.py')
        output = subprocess.run([sys.executable, '-B', str(script), '--workspace', str(self.root), '--json'],
                                capture_output=True, encoding='utf-8')
        self.assertEqual(output.returncode, 0, output.stderr)
        self.assertTrue(json.loads(output.stdout)['passed'])


if __name__ == '__main__':
    unittest.main()
