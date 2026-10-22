#!/usr/bin/env python3
"""Layout invariants for story_map_to_excalidraw.py.

The converter's job is to make overlap impossible by computing geometry from
text metrics, so these tests assert the scene is self-consistent rather than
matching exact pixel values.
"""
from __future__ import annotations

import itertools
import json
from pathlib import Path
import tempfile
import unittest

import story_map_to_excalidraw as conv


def sample_data() -> dict:
    return {
        'title': '测试故事地图',
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
                 {'id': 'US-1', 'activity': 'ACT-1', 'title': '检索', 'desc': '• 支持关键字\n• 支持过滤',
                  'tag': '[P0]'},
                 {'id': 'US-2', 'activity': 1, 'title': '执行', 'desc': '• 一键执行', 'fr': 'FR-002'},
             ]},
            {'theme': 'mvp', 'badge': 'MVP', 'title': '二期底线', 'desc': '',
             'stories': [
                 {'id': 'US-3', 'activity': 'ACT-1', 'title': '收藏', 'desc': '• 收藏常用项\n• 排序'},
             ]},
        ],
    }


class SceneTests(unittest.TestCase):
    def setUp(self) -> None:
        self.scene = conv.build_scene(sample_data())
        self.elements = self.scene['elements']
        self.by_id = {e['id']: e for e in self.elements}

    def test_scene_envelope(self) -> None:
        self.assertEqual(self.scene['type'], 'excalidraw')
        self.assertEqual(self.scene['version'], 2)
        self.assertEqual(self.scene['files'], {})
        self.assertTrue(self.elements)

    def test_element_ids_are_unique(self) -> None:
        self.assertEqual(len(self.by_id), len(self.elements))

    def test_every_container_has_matching_bound_text(self) -> None:
        for element in self.elements:
            if element['type'] != 'rectangle':
                continue
            for bound in element.get('boundElements') or []:
                text = self.by_id.get(bound['id'])
                self.assertIsNotNone(text, f"missing bound text {bound['id']}")
                self.assertEqual(text['containerId'], element['id'])

    def test_text_stays_inside_its_container(self) -> None:
        for element in self.elements:
            if element['type'] != 'rectangle' or not element.get('boundElements'):
                continue
            text = self.by_id[element['boundElements'][0]['id']]
            self.assertGreaterEqual(text['x'], element['x'] - 0.5)
            self.assertGreaterEqual(text['y'], element['y'] - 0.5)
            self.assertLessEqual(text['x'] + text['width'], element['x'] + element['width'] + 0.5)
            self.assertLessEqual(text['y'] + text['height'], element['y'] + element['height'] + 0.5)

    def test_no_labelled_boxes_overlap(self) -> None:
        boxes = [e for e in self.elements if e['type'] == 'rectangle' and e.get('boundElements')]
        for a, b in itertools.combinations(boxes, 2):
            overlap_w = min(a['x'] + a['width'], b['x'] + b['width']) - max(a['x'], b['x'])
            overlap_h = min(a['y'] + a['height'], b['y'] + b['height']) - max(a['y'], b['y'])
            with self.subTest(pair=(a['id'], b['id'])):
                self.assertFalse(overlap_w > 1 and overlap_h > 1,
                                 f"{a['id']} overlaps {b['id']}")

    def test_every_story_becomes_a_card(self) -> None:
        expected = sum(len(r['stories']) for r in sample_data()['releases'])
        cards = [e for e in self.elements
                 if e['type'] == 'rectangle' and e['id'].startswith('lane-') and '-card-' in e['id']]
        self.assertEqual(len(cards), expected)

    def test_long_text_is_pre_wrapped(self) -> None:
        long_story = {'id': 'US-9', 'activity': 0,
                      'title': '很长的标题' * 12, 'desc': '很长的说明' * 20}
        data = sample_data()
        data['releases'][0]['stories'].append(long_story)
        scene = conv.build_scene(data)
        card = next(e for e in scene['elements']
                    if e['type'] == 'rectangle' and '-card-' in e['id'] and 'US-9' in e['id'])
        text = next(e for e in scene['elements'] if e.get('containerId') == card['id'])
        self.assertIn('\n', text['text'], 'wrapped text must keep its line breaks')
        self.assertEqual(text['originalText'], text['originalText'].strip())

    def test_layout_is_deterministic(self) -> None:
        first = conv.build_scene(sample_data())
        second = conv.build_scene(sample_data())
        self.assertEqual(json.dumps(first, sort_keys=True), json.dumps(second, sort_keys=True))

    def test_unknown_theme_falls_back(self) -> None:
        data = sample_data()
        data['releases'][0]['theme'] = 'no-such-theme'
        scene = conv.build_scene(data)
        self.assertEqual(len(scene['elements']), len(self.elements))

    def test_missing_activities_rejected(self) -> None:
        with self.assertRaises(ValueError):
            conv.build_scene({'releases': []})


class EmojiTests(unittest.TestCase):
    def _data(self) -> dict:
        data = sample_data()
        data['releases'][0]['stories'][0].update(
            {'title': '🟢 已交付能力', 'desc': '• 支持关键 🔴 告警\n• 保留 → 箭头'})
        return data

    def _card_texts(self, scene: dict) -> list[str]:
        return [e['text'] for e in scene['elements']
                if e['type'] == 'text' and e.get('containerId')]

    def test_emoji_kept_by_default(self) -> None:
        joined = '\n'.join(self._card_texts(conv.build_scene(self._data())))
        for glyph in ('🟢', '🔴'):
            self.assertIn(glyph, joined)
        self.assertIn('已交付能力', joined)

    def test_arrows_and_brackets_survive(self) -> None:
        joined = '\n'.join(self._card_texts(conv.build_scene(self._data())))
        self.assertIn('→', joined)
        self.assertIn('[P0]', joined)

    def test_strip_emoji_flag_removes_symbols(self) -> None:
        joined = '\n'.join(self._card_texts(conv.build_scene(self._data(), strip_emoji=True)))
        for glyph in ('🟢', '🔴'):
            self.assertNotIn(glyph, joined)
        self.assertIn('已交付能力', joined)

    def test_strip_emoji_collapses_the_gap_it_leaves(self) -> None:
        self.assertEqual(conv.strip_emoji('• 支持关键 🔴 告警'), '• 支持关键 告警')
        self.assertEqual(conv.strip_emoji('🟢 已交付'), '已交付')


class FileTests(unittest.TestCase):
    def test_round_trip_writes_valid_json(self) -> None:
        with tempfile.TemporaryDirectory(prefix='story-map-') as tmp:
            data_file = Path(tmp) / 'map.json'
            data_file.write_text(json.dumps(sample_data(), ensure_ascii=False), encoding='utf-8')
            out_file = Path(tmp) / 'map.excalidraw'
            result = conv.render_story_map_to_excalidraw(data_file, out_file)
            self.assertTrue(result['passed'], result)
            scene = json.loads(out_file.read_text(encoding='utf-8'))
            self.assertEqual(scene['type'], 'excalidraw')
            self.assertNotIn('_meta', scene)
            self.assertEqual(len(scene['elements']), result['elements'])

    def test_missing_data_file_reports_error(self) -> None:
        result = conv.render_story_map_to_excalidraw(Path('definitely-missing.json'))
        self.assertFalse(result['passed'])
        self.assertTrue(result['errors'])


if __name__ == '__main__':
    unittest.main()
