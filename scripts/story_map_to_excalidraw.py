#!/usr/bin/env python3
"""Render a 2D user story map JSON into an editable .excalidraw scene file.

Part of PRD Refiner skill. Layout is computed here, not by the model: card
heights come from estimated text metrics, so containers never need to grow
after the fact and cards cannot overlap. The output is a plain Excalidraw
scene file that opens in excalidraw.com or the desktop app — no local canvas
service required.

The input JSON contract is documented in assets/story-map-schema.md.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import sys

# ---- geometry -------------------------------------------------------------

PAGE = 50
TITLE_H = 70
ROW_GAP = 20
CARD_W = 280
COL_GAP = 24
LANE_HEADER_W = 230
LANE_PAD = 20
CARD_GAP_Y = 12
LANE_GAP = 30
TEXT_PAD = 10
LINE_HEIGHT = 1.25
FIXED_UPDATED = 1_700_000_000_000  # deterministic output

FONT_TITLE = 22
FONT_META = 14
FONT_ACTIVITY = 15
FONT_LANE = 13
FONT_CARD = 14

INK = '#1e293b'
ACTIVITY_BG = '#dbeafe'
ACTIVITY_STROKE = '#1d4ed8'
ACTIVITY_INK = '#1e3a8a'

# theme -> colours; unknown themes fall back to ``future``.
THEMES = {
    'legacy': {
        'card_bg': '#f1f3f5', 'card_stroke': '#868e96',
        'lane_bg': '#fafafa', 'lane_stroke': '#dee2e6',
        'head_bg': '#e9ecef', 'head_stroke': '#495057',
    },
    'mvp': {
        'card_bg': '#fefce8', 'card_stroke': '#eab308',
        'lane_bg': '#fffdf5', 'lane_stroke': '#fde68a',
        'head_bg': '#fef3c7', 'head_stroke': '#d97706',
    },
    'next': {
        'card_bg': '#f0f9ff', 'card_stroke': '#0284c7',
        'lane_bg': '#f8fdff', 'lane_stroke': '#bae6fd',
        'head_bg': '#e0f2fe', 'head_stroke': '#0369a1',
    },
    'future': {
        'card_bg': '#f8fafc', 'card_stroke': '#94a3b8',
        'lane_bg': '#fbfcfe', 'lane_stroke': '#e2e8f0',
        'head_bg': '#e2e8f0', 'head_stroke': '#475569',
    },
}
THEME_KEYS = tuple(THEMES)

_B62 = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'


def _index(n: int) -> str:
    """Fixed-width fractional index: lexicographic order matches numeric order."""
    digits = []
    value = n
    for _ in range(4):
        digits.append(_B62[value % len(_B62)])
        value //= len(_B62)
    return 'a' + ''.join(reversed(digits))


def _seed(text: str) -> int:
    digest = hashlib.sha1(text.encode('utf-8')).digest()
    return (int.from_bytes(digest[:4], 'big') % 2_147_483_646) + 1


# Emoji and pictographs render differently across machines (and slow some
# rasterizers down badly), so they are stripped from diagram text by default.
_EMOJI_RANGES = ((0x1F000, 0x1FAFF), (0x2600, 0x27BF), (0x2B00, 0x2BFF),
                 (0xFE0F, 0xFE0F), (0x200D, 0x200D))


def strip_emoji(text: str) -> str:
    kept = [ch for ch in text
            if not any(lo <= ord(ch) <= hi for lo, hi in _EMOJI_RANGES)]
    return re.sub(r'[ \t]{2,}', ' ', ''.join(kept)).strip()


# Alias so kwargs named ``strip_emoji`` do not shadow the callable.
_remove_emoji = strip_emoji


def char_width(ch: str) -> float:
    """Estimated advance width in em, deliberately erring wide to avoid under-measuring."""
    code = ord(ch)
    if code < 128:
        return 0.62
    if 0x3000 <= code <= 0x303F or 0x4E00 <= code <= 0x9FFF or 0xFF00 <= code <= 0xFFEF:
        return 1.03
    if 0x1F000 <= code <= 0x1FAFF or 0x2600 <= code <= 0x27BF:
        return 1.08
    return 1.06


def wrap_text(text: str, max_width: float, font_size: float) -> list[str]:
    lines: list[str] = []
    for para in text.split('\n'):
        if not para:
            lines.append('')
            continue
        current = ''
        width = 0.0
        for ch in para:
            advance = char_width(ch) * font_size
            if current and width + advance > max_width:
                lines.append(current)
                current, width = '', 0.0
            current += ch
            width += advance
        lines.append(current)
    return lines


def text_height(text: str, max_width: float, font_size: float) -> float:
    return len(wrap_text(text, max_width, font_size)) * font_size * LINE_HEIGHT + TEXT_PAD


def box_height(width: float, content: str, font_size: float, minimum: float = 0.0) -> float:
    """Height a container needs so its pre-wrapped text fits without growing."""
    return max(minimum, text_height(content, width - 2 * TEXT_PAD - 2, font_size) + 2 * TEXT_PAD)


class SceneBuilder:
    def __init__(self) -> None:
        self.elements: list[dict] = []
        self._seq = 0

    def _next_index(self) -> str:
        self._seq += 1
        return _index(self._seq)

    def add_rect(self, eid: str, x: float, y: float, width: float, height: float,
                 fill: str, stroke: str, *, dashed: bool = False, stroke_width: float = 2,
                 text_id: str | None = None, seed_key: str | None = None) -> dict:
        element = {
            'id': eid,
            'type': 'rectangle',
            'x': round(x, 2),
            'y': round(y, 2),
            'width': round(width, 2),
            'height': round(height, 2),
            'angle': 0,
            'backgroundColor': fill,
            'boundElements': [{'id': text_id, 'type': 'text'}] if text_id else [],
            'fillStyle': 'solid',
            'frameId': None,
            'groupIds': [],
            'index': self._next_index(),
            'isDeleted': False,
            'link': None,
            'locked': False,
            'opacity': 100,
            'roughness': 0,
            'roundness': {'type': 3},
            'seed': _seed(seed_key or eid),
            'strokeColor': stroke,
            'strokeStyle': 'dashed' if dashed else 'solid',
            'strokeWidth': stroke_width,
            'updated': FIXED_UPDATED,
            'version': 1,
            'versionNonce': _seed((seed_key or eid) + ':nonce'),
        }
        self.elements.append(element)
        return element

    def add_text(self, tid: str, x: float, y: float, width: float, height: float,
                 wrapped: str, original: str, font_size: float, color: str, *,
                 container_id: str | None = None, align: str = 'center',
                 valign: str = 'middle', seed_key: str | None = None) -> dict:
        element = {
            'id': tid,
            'type': 'text',
            'x': round(x, 2),
            'y': round(y, 2),
            'width': round(width, 2),
            'height': round(height, 2),
            'angle': 0,
            'autoResize': True,
            'backgroundColor': 'transparent',
            'boundElements': [],
            'containerId': container_id,
            'fillStyle': 'solid',
            'fontFamily': 2,
            'fontSize': font_size,
            'frameId': None,
            'groupIds': [],
            'index': self._next_index(),
            'isDeleted': False,
            'lineHeight': LINE_HEIGHT,
            'link': None,
            'locked': False,
            'opacity': 100,
            'originalText': original,
            'roughness': 1,
            'roundness': None,
            'seed': _seed((seed_key or tid) + ':text'),
            'strokeColor': color,
            'strokeStyle': 'solid',
            'strokeWidth': 1,
            'text': wrapped,
            'textAlign': align,
            'updated': FIXED_UPDATED,
            'version': 1,
            'versionNonce': _seed((seed_key or tid) + ':text-nonce'),
            'verticalAlign': valign,
        }
        self.elements.append(element)
        return element


def _labelled_box(builder: SceneBuilder, box_id: str, x: float, y: float,
                  width: float, height: float, content: str, font_size: float,
                  fill: str, stroke: str, ink: str, *, dashed: bool = False,
                  align: str = 'center') -> float:
    """Draw a rectangle plus its bound text; return the rectangle bottom edge.

    The text is pre-wrapped here and stored wrapped (Excalidraw honours the
    stored line breaks instead of re-flowing on open), so the container never
    has to grow after the fact.
    """
    text_id = f'{box_id}-text'
    inner_w = width - 2 * TEXT_PAD
    lines = wrap_text(content, inner_w - 2, font_size)
    text_h = len(lines) * font_size * LINE_HEIGHT + TEXT_PAD
    builder.add_rect(box_id, x, y, width, height, fill, stroke, dashed=dashed, text_id=text_id)
    builder.add_text(text_id, x + TEXT_PAD, y + max(0.0, (height - text_h) / 2), inner_w, text_h,
                     '\n'.join(lines), content, font_size, ink,
                     container_id=box_id, align=align)
    return y + height


def _story_text(story: dict, clean=lambda value: value) -> str:
    story_id = clean(str(story.get('id') or '').strip())
    title = clean(str(story.get('title') or '').strip())
    head = ' '.join(part for part in (story_id, title) if part)
    parts = [head] if head else []
    tag = clean(str(story.get('tag') or '').strip())
    if tag:
        parts.append(tag)
    desc = clean(str(story.get('desc') or '').strip())
    if desc:
        parts.append(desc)
    fr = clean(str(story.get('fr') or '').strip())
    if fr and fr not in desc:
        parts.append(f'关联 {fr}')
    return '\n'.join(parts)


def _activity_index(story: dict, activities: list[dict]) -> int:
    raw = story.get('activity', 0)
    if isinstance(raw, int) and 0 <= raw < len(activities):
        return raw
    lookup: dict[str, int] = {}
    for i, act in enumerate(activities):
        for field in ('id', 'name'):
            value = str(act.get(field) or '').strip().casefold()
            if value:
                lookup[value] = i
    return lookup.get(str(raw).strip().casefold(), 0)


def build_scene(data: dict, *, strip_emoji: bool = False) -> dict:
    """Build an Excalidraw scene dict from story-map JSON data."""
    activities = data.get('activities') or []
    releases = data.get('releases') or []
    if not activities:
        raise ValueError('activities is required and must not be empty')

    def clean(value: str) -> str:
        return _remove_emoji(value) if strip_emoji else value

    builder = SceneBuilder()
    title = clean(str(data.get('title') or '二维用户故事地图'))
    badge = clean(str(data.get('badge') or '').strip())

    n_cols = len(activities)
    inner_w = LANE_HEADER_W + COL_GAP + n_cols * CARD_W + (n_cols - 1) * COL_GAP
    lane_w = inner_w + 2 * LANE_PAD
    col_x = [PAGE + LANE_PAD + LANE_HEADER_W + COL_GAP + i * (CARD_W + COL_GAP)
             for i in range(n_cols)]

    # ---- title banner ----
    heading = f'{title}  {badge}'.strip()
    band_h = box_height(lane_w, heading, FONT_TITLE, TITLE_H)
    y = PAGE
    _labelled_box(builder, 'title', PAGE, y, lane_w, band_h, heading, FONT_TITLE,
                  '#e7f5ff', '#1864ab', INK)
    y += band_h + ROW_GAP

    # ---- meta row (core value / role) ----
    meta_items = [(label, clean(str(data.get(key) or '').strip()))
                  for key, label in (('core_value', '核心价值'), ('role', '核心角色'))]
    meta_items = [(label, value) for label, value in meta_items if value]
    if meta_items:
        meta_gap = 20
        meta_w = (lane_w - meta_gap * (len(meta_items) - 1)) / len(meta_items)
        meta_h = max(box_height(meta_w, f'{label}：{value}', FONT_META)
                     for label, value in meta_items)
        for i, (label, value) in enumerate(meta_items):
            _labelled_box(builder, f'meta-{i + 1}', PAGE + i * (meta_w + meta_gap), y,
                          meta_w, meta_h, f'{label}：{value}', FONT_META,
                          '#f8f9fa', '#1971c2', INK)
        y += meta_h + ROW_GAP

    # ---- backbone activity row ----
    corner_w = LANE_HEADER_W
    activity_contents = []
    for i, act in enumerate(activities):
        head = ' '.join(clean(str(part).strip()) for part in
                        (act.get('id') or f'ACT-{i + 1:02d}', act.get('name') or '')
                        if str(part).strip())
        desc = clean(str(act.get('desc') or '').strip())
        activity_contents.append(head + (f'\n{desc}' if desc else ''))
    act_h = max(72, box_height(CARD_W, '活动', FONT_ACTIVITY),
                *(box_height(CARD_W, content, FONT_ACTIVITY) for content in activity_contents))
    _labelled_box(builder, 'backbone-corner', PAGE + LANE_PAD, y, corner_w, act_h,
                  '用户主干活动 →\n版本切片 ↓', FONT_LANE, '#e9ecef', '#343a40', INK)
    for i, content in enumerate(activity_contents):
        _labelled_box(builder, f'act-{i + 1:02d}', col_x[i], y, CARD_W, act_h,
                      content, FONT_ACTIVITY, ACTIVITY_BG, ACTIVITY_STROKE, ACTIVITY_INK)
    y += act_h + LANE_GAP

    # ---- swimlanes ----
    for r_i, release in enumerate(releases):
        theme_key = str(release.get('theme') or 'mvp').strip().casefold()
        theme = THEMES.get(theme_key, THEMES['future'])
        release_badge = clean(str(release.get('badge') or 'Release').strip())
        release_title = clean(str(release.get('title') or '').strip())
        release_desc = clean(str(release.get('desc') or '').strip())

        columns: list[list[dict]] = [[] for _ in activities]
        for story in release.get('stories') or []:
            columns[_activity_index(story, activities)].append(story)

        # card heights first: lane height depends on the tallest column
        card_boxes: list[list[dict]] = []
        for column in columns:
            boxes = []
            for story in column:
                content = _story_text(story, clean)
                height = box_height(CARD_W, content, FONT_CARD, 70.0)
                boxes.append({'story': story, 'content': content, 'height': height})
            card_boxes.append(boxes)

        head_content = '\n'.join(part for part in (release_title, release_badge, release_desc) if part)
        head_h = box_height(LANE_HEADER_W, head_content, FONT_LANE)
        column_h = max((sum(b['height'] for b in boxes) + CARD_GAP_Y * max(0, len(boxes) - 1)
                        for boxes in card_boxes), default=0)
        lane_h = max(column_h, head_h) + 2 * LANE_PAD

        lane_id = f'lane-{r_i + 1:02d}'
        builder.add_rect(lane_id, PAGE, y, lane_w, lane_h, theme['lane_bg'],
                         theme['lane_stroke'], dashed=True, stroke_width=1.5)
        _labelled_box(builder, f'{lane_id}-head', PAGE + LANE_PAD, y + LANE_PAD,
                      LANE_HEADER_W, lane_h - 2 * LANE_PAD, head_content, FONT_LANE,
                      theme['head_bg'], theme['head_stroke'], INK, align='left')

        for c_i, boxes in enumerate(card_boxes):
            card_y = y + LANE_PAD
            for s_j, box in enumerate(boxes):
                story = box['story']
                story_id = str(story.get('id') or f'story-{r_i + 1}-{c_i + 1}-{s_j + 1}')
                safe_id = ''.join(ch if ch.isalnum() or ch in '-_' else '-' for ch in story_id).strip('-')
                card_id = f'{lane_id}-card-{c_i + 1:02d}-{s_j + 1:02d}-{safe_id}'
                _labelled_box(builder, card_id, col_x[c_i], card_y, CARD_W, box['height'],
                              box['content'], FONT_CARD, theme['card_bg'],
                              theme['card_stroke'], INK)
                card_y += box['height'] + CARD_GAP_Y

        y += lane_h + LANE_GAP

    width = lane_w
    height = y - LANE_GAP + PAGE
    return {
        'type': 'excalidraw',
        'version': 2,
        'source': 'https://github.com/prd-refiner',
        'elements': builder.elements,
        'appState': {'viewBackgroundColor': '#ffffff', 'gridSize': None},
        'files': {},
        '_meta': {'width': round(width), 'height': round(height)},
    }


def render_story_map_to_excalidraw(data_file: Path, output_file: Path | None = None,
                                   *, strip_emoji: bool = False) -> dict:
    if not data_file.is_file():
        return {'passed': False, 'errors': [f'data file not found: {data_file}']}
    try:
        data = json.loads(data_file.read_text(encoding='utf-8-sig'))
    except Exception as exc:
        return {'passed': False, 'errors': [f'invalid JSON format in {data_file}: {exc}']}
    try:
        scene = build_scene(data, strip_emoji=strip_emoji)
    except ValueError as exc:
        return {'passed': False, 'errors': [str(exc)]}

    if output_file is None:
        output_file = data_file.resolve().parent / '.assets' / 'story-map.excalidraw'
    output_file.parent.mkdir(parents=True, exist_ok=True)
    body = {key: value for key, value in scene.items() if key != '_meta'}
    output_file.write_text(json.dumps(body, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return {
        'passed': True,
        'output': str(output_file.resolve()),
        'elements': len(body['elements']),
        'width': scene['_meta']['width'],
        'height': scene['_meta']['height'],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--data', required=True, type=Path, help='Story map JSON input file')
    parser.add_argument('--output', type=Path,
                        help='Output .excalidraw file (default: <data dir>/.assets/story-map.excalidraw)')
    parser.add_argument('--strip-emoji', action='store_true',
                        help='Remove emoji/symbols (default: keep them; browsers render them fine)')
    args = parser.parse_args(argv)
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    result = render_story_map_to_excalidraw(args.data, args.output, strip_emoji=args.strip_emoji)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result.get('passed') else 1


if __name__ == '__main__':
    raise SystemExit(main())
