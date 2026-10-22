#!/usr/bin/env python3
"""Tests for render_story_map_vector.py (pure-Python SVG + browser rasterization)."""
from __future__ import annotations

import json
from pathlib import Path
import struct
import tempfile
import unittest
import xml.etree.ElementTree as ET

import render_story_map_vector as vec
import story_map_to_excalidraw as conv


def sample_data() -> dict:
    return {
        'title': '测试 & <地图>',
        'badge': 'V1',
        'core_value': '一句话价值',
        'role': '主要角色',
        'activities': [
            {'id': 'ACT-1', 'name': '发现', 'desc': '找到入口'},
            {'id': 'ACT-2', 'name': '使用', 'desc': '完成操作'},
        ],
        'releases': [
            {'theme': 'legacy', 'badge': '已交付', 'title': '一期现状', 'desc': '已有能力',
             'stories': [
                 {'id': 'US-1', 'activity': 'ACT-1', 'title': '检索', 'desc': '• 支持关键字',
                  'tag': '[P0]'},
                 {'id': 'US-2', 'activity': 1, 'title': '执行', 'desc': '• 一键执行'},
             ]},
            {'theme': 'mvp', 'badge': 'MVP', 'title': '二期底线', 'desc': '',
             'stories': [
                 {'id': 'US-3', 'activity': 'ACT-1', 'title': '收藏', 'desc': '• 收藏常用项'},
             ]},
        ],
    }


def scene_of(data: dict | None = None, **kwargs) -> dict:
    return conv.build_scene(data or sample_data(), **kwargs)


class SvgTests(unittest.TestCase):
    def setUp(self) -> None:
        self.scene = scene_of()
        self.svg = vec.scene_to_svg(self.scene)
        self.root = ET.fromstring(self.svg)

    def test_svg_is_well_formed_xml(self) -> None:
        self.assertTrue(self.root.tag.endswith('svg'))
        self.assertIn('xmlns="http://www.w3.org/2000/svg"', self.svg)

    def test_canvas_covers_the_scene_bounding_box(self) -> None:
        elements = self.scene['elements']
        expected_w = (max(e['x'] + e['width'] for e in elements)
                      - min(e['x'] for e in elements) + 2 * vec.SVG_PADDING)
        expected_h = (max(e['y'] + e['height'] for e in elements)
                      - min(e['y'] for e in elements) + 2 * vec.SVG_PADDING)
        self.assertAlmostEqual(float(self.root.get('width')), expected_w, delta=1)
        self.assertAlmostEqual(float(self.root.get('height')), expected_h, delta=1)

    def test_every_rectangle_is_drawn(self) -> None:
        rects = self.root.findall('.//{http://www.w3.org/2000/svg}rect')
        expected = [e for e in self.scene['elements'] if e['type'] == 'rectangle']
        self.assertEqual(len(rects) - 1, len(expected))  # one page background

    def test_every_wrapped_text_line_is_drawn(self) -> None:
        texts = self.root.findall('.//{http://www.w3.org/2000/svg}text')
        expected_lines = sum(len(e['text'].split('\n'))
                             for e in self.scene['elements'] if e['type'] == 'text')
        self.assertEqual(len(texts), expected_lines)

    def test_markup_characters_are_escaped_not_dropped(self) -> None:
        joined = ' '.join(t.text or '' for t in self.root.findall('.//{http://www.w3.org/2000/svg}text'))
        self.assertIn('测试 & <地图>', joined)

    def test_emoji_kept_by_default(self) -> None:
        data = sample_data()
        data['releases'][0]['stories'][0]['title'] = '🔵 检索'
        svg = vec.scene_to_svg(scene_of(data))
        self.assertIn('🔵', svg)

    def test_strip_emoji_flag_removes_symbols(self) -> None:
        data = sample_data()
        data['releases'][0]['stories'][0]['title'] = '🔵 检索'
        svg = vec.scene_to_svg(scene_of(data, strip_emoji=True))
        self.assertNotIn('🔵', svg)


class RenderTests(unittest.TestCase):
    def _write_data(self, tmp: str, data: dict | None = None) -> Path:
        path = Path(tmp) / 'map.json'
        path.write_text(json.dumps(data or sample_data(), ensure_ascii=False), encoding='utf-8')
        return path

    def test_svg_output_is_written(self) -> None:
        with tempfile.TemporaryDirectory(prefix='story-map-') as tmp:
            data = self._write_data(tmp)
            out = Path(tmp) / 'map.svg'
            result = vec.render_story_map_vector(data, out, fmt='svg')
            self.assertTrue(result['passed'], result)
            self.assertIn('<svg', out.read_text(encoding='utf-8'))

    def test_missing_browser_is_reported_not_raised(self) -> None:
        with tempfile.TemporaryDirectory(prefix='story-map-') as tmp:
            data = self._write_data(tmp)
            out = Path(tmp) / 'map.png'
            result = vec.render_story_map_vector(
                data, out, fmt='png', browser_path=Path(tmp) / 'no-such-browser.exe', timeout=2)
            self.assertFalse(result['passed'])
            self.assertTrue(result['errors'])

    def test_unsupported_format_rejected(self) -> None:
        result = vec.render_story_map_vector(Path('map.json'), Path('out.bmp'), fmt='bmp')
        self.assertFalse(result['passed'])

    def test_missing_data_file_reports_error(self) -> None:
        result = vec.render_story_map_vector(Path('definitely-missing.json'), Path('out.svg'), fmt='svg')
        self.assertFalse(result['passed'])
        self.assertTrue(result['errors'])

    def test_png_header_parser(self) -> None:
        with tempfile.TemporaryDirectory(prefix='story-map-') as tmp:
            path = Path(tmp) / 'x.png'
            header = b'\x89PNG\r\n\x1a\n' + b'\x00\x00\x00\x0dIHDR' + struct.pack('>II', 120, 80)
            path.write_bytes(header + b'\x00' * 16)
            self.assertEqual(vec._png_size(path), (120, 80))


if __name__ == '__main__':
    unittest.main()
