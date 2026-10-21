#!/usr/bin/env python3
"""Render a 2D User Story Map from JSON to high-DPI PNG using headless browser.

Part of PRD Refiner skill. Provides a zero-friction, parameterized generator
for 2D User Story Maps (Activities on X-axis, Release slices on Y-axis).

The input JSON contract is documented in assets/story-map-schema.md.
"""
from __future__ import annotations

import argparse
from html import escape
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


def find_system_browser() -> Path | None:
    """Discover installed Chrome, Edge, or Chromium executable."""
    env_browser = os.environ.get('CHROME_PATH') or os.environ.get('EDGE_PATH')
    if env_browser and Path(env_browser).is_file():
        return Path(env_browser)

    candidates = [
        Path(r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'),
        Path(r'C:\Program Files\Microsoft\Edge\Application\msedge.exe'),
        Path(r'C:\Program Files\Google\Chrome\Application\chrome.exe'),
        Path(r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'),
        Path.home() / r'AppData\Local\Google\Chrome\Application\chrome.exe',
        Path.home() / r'AppData\Local\Microsoft\Edge\Application\msedge.exe',
        Path('/usr/bin/google-chrome'),
        Path('/usr/bin/chromium-browser'),
        Path('/usr/bin/chromium'),
        Path('/usr/bin/msedge'),
        Path('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'),
        Path('/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge'),
    ]
    for c in candidates:
        if c.is_file():
            return c

    for name in ('msedge', 'google-chrome', 'chrome', 'chromium'):
        found = shutil.which(name)
        if found and Path(found).is_file():
            return Path(found)

    return None


def generate_story_map_html(data: dict) -> tuple[str, int, int]:
    """Generate HTML string and estimated (width, height) from story map JSON."""
    title = data.get('title', '二维用户故事地图')
    badge = data.get('badge', '')
    core_value = data.get('core_value', '')
    role = data.get('role', '')
    activities = data.get('activities', [])
    releases = data.get('releases', [])

    num_activities = max(1, len(activities))
    card_width = 290
    swimlane_header_width = 180
    gap = 16
    padding = 32 * 2
    total_width = swimlane_header_width + (card_width * num_activities) + (gap * num_activities) + padding

    # Resolve activity index lookup
    act_lookup = {}
    for idx, act in enumerate(activities):
        act_lookup[idx] = idx
        if 'id' in act:
            act_lookup[str(act['id']).strip().casefold()] = idx
        if 'name' in act:
            act_lookup[str(act['name']).strip().casefold()] = idx

    # Calculate release row heights
    release_row_heights = []
    release_grids = []

    for rel in releases:
        stories = rel.get('stories', [])
        cols = [[] for _ in range(num_activities)]
        for st in stories:
            raw_act = st.get('activity', 0)
            if isinstance(raw_act, int) and 0 <= raw_act < num_activities:
                col_idx = raw_act
            elif str(raw_act).strip().casefold() in act_lookup:
                col_idx = act_lookup[str(raw_act).strip().casefold()]
            else:
                col_idx = 0
            cols[col_idx].append(st)

        max_in_col = max((len(c) for c in cols), default=1)
        row_h = max(170, 40 + max_in_col * 125)
        release_row_heights.append(row_h)
        release_grids.append((rel, cols))

    # Total estimated window height
    total_height = 130 + 120 + sum(release_row_heights) + (len(releases) * gap) + padding + 40

    html = []
    html.append(f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<title>{escape(title)}</title>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
    background-color: #ffffff;
    color: #1e293b;
    padding: 32px;
    width: {total_width}px;
  }}
  .header {{
    background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
    border: 1px solid #cbd5e1;
    border-radius: 12px;
    padding: 24px 32px;
    margin-bottom: 24px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    box-shadow: 0 4px 20px rgba(15,23,42,0.08);
  }}
  .header h1 {{
    font-size: 26px;
    font-weight: 700;
    color: #0f172a;
    letter-spacing: -0.5px;
    display: flex;
    align-items: center;
    gap: 12px;
  }}
  .header .tag {{
    background: #2563eb;
    color: #ffffff;
    font-size: 13px;
    padding: 4px 10px;
    border-radius: 6px;
    font-weight: 600;
  }}
  .header .meta {{
    color: #475569;
    font-size: 14px;
    display: flex;
    gap: 20px;
  }}
  .meta-item {{ display: flex; align-items: center; gap: 6px; }}

  /* Grid Layout */
  .grid-container {{
    display: grid;
    grid-template-columns: {swimlane_header_width}px repeat({num_activities}, 1fr);
    gap: {gap}px;
  }}

  /* Activity Header Column */
  .activity-corner {{
    background: #f1f5f9;
    border: 1px dashed #94a3b8;
    border-radius: 10px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    padding: 16px;
    color: #475569;
    font-size: 14px;
    font-weight: 600;
    text-align: center;
  }}
  .activity-card {{
    background: linear-gradient(135deg, #1d4ed8 0%, #2563eb 100%);
    border-radius: 10px;
    padding: 16px 18px;
    color: #ffffff;
    box-shadow: 0 4px 12px rgba(37,99,235,0.25);
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    min-height: 96px;
  }}
  .activity-num {{
    font-size: 12px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: #93c5fd;
    margin-bottom: 4px;
  }}
  .activity-title {{
    font-size: 16px;
    font-weight: 700;
    line-height: 1.3;
  }}
  .activity-desc {{
    font-size: 12px;
    color: #dbeafe;
    margin-top: 6px;
  }}

  /* Swimlanes / Releases */
  .swimlane-header {{
    border-radius: 10px;
    padding: 16px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    border-left: 6px solid;
    background: #f8fafc;
    color: #0f172a;
  }}
  .theme-mvp {{ border-color: #f59e0b; }}
  .theme-next {{ border-color: #0284c7; }}
  .theme-future {{ border-color: #64748b; color: #475569; }}

  .swimlane-badge {{
    font-size: 11px;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    margin-bottom: 6px;
  }}
  .badge-mvp {{ color: #b45309; }}
  .badge-next {{ color: #0369a1; }}
  .badge-future {{ color: #64748b; }}

  .swimlane-title {{
    font-size: 15px;
    font-weight: 700;
    line-height: 1.3;
  }}
  .swimlane-desc {{
    font-size: 12px;
    color: #64748b;
    margin-top: 6px;
  }}

  /* Column cells */
  .cell {{
    display: flex;
    flex-direction: column;
    gap: 12px;
    background: rgba(241, 245, 249, 0.8);
    border: 1px solid #e2e8f0;
    border-radius: 10px;
    padding: 12px;
  }}

  /* Story Cards (Sticky Notes) */
  .card {{
    border-radius: 8px;
    padding: 12px 14px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.15);
    border-left: 4px solid;
    position: relative;
  }}
  .card-mvp {{
    background: #fefce8;
    border-color: #eab308;
    color: #713f12;
  }}
  .card-next {{
    background: #f0f9ff;
    border-color: #0284c7;
    color: #0c4a6e;
  }}
  .card-future {{
    background: #f8fafc;
    border-color: #94a3b8;
    color: #334155;
  }}

  .card-header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 6px;
  }}
  .card-id {{
    font-size: 11px;
    font-weight: 700;
    opacity: 0.85;
    letter-spacing: 0.5px;
  }}
  .card-fr {{
    font-size: 10px;
    font-weight: 700;
    padding: 2px 6px;
    border-radius: 4px;
  }}
  .fr-mvp {{ background: #fef08a; color: #854d0e; }}
  .fr-next {{ background: #e0f2fe; color: #0369a1; }}
  .fr-future {{ background: #e2e8f0; color: #475569; }}

  .card-title {{
    font-size: 13.5px;
    font-weight: 700;
    line-height: 1.35;
    margin-bottom: 4px;
  }}
  .card-desc {{
    font-size: 11.5px;
    line-height: 1.4;
    opacity: 0.88;
  }}
  .card-highlight {{
    margin-top: 6px;
    font-size: 11px;
    font-weight: 600;
    display: inline-block;
    padding: 2px 6px;
    border-radius: 4px;
    background: rgba(0,0,0,0.05);
  }}
</style>
</head>
<body>

<div class="header">
  <div>
    <h1>{escape(title)} {f'<span class="tag">{escape(badge)}</span>' if badge else ''}</h1>
  </div>
  <div class="meta">
    {f'<div class="meta-item"><span>📌 核心价值:</span> <strong>{escape(core_value)}</strong></div>' if core_value else ''}
    {f'<div class="meta-item"><span>👥 核心角色:</span> <strong>{escape(role)}</strong></div>' if role else ''}
  </div>
</div>

<div class="grid-container">

  <!-- BACKBONE ACTIVITIES ROW -->
  <div class="activity-corner">
    <div><strong>横向: 用户主干活动</strong></div>
    <div style="font-size: 11px; margin-top: 4px; color: #64748b;">纵向: 阶段发布切片</div>
  </div>
""")

    for idx, act in enumerate(activities):
        aid = escape(act.get('id', f'STAGE {idx+1:02d}'))
        aname = escape(act.get('name', '活动'))
        adesc = escape(act.get('desc', ''))
        html.append(f"""  <div class="activity-card">
    <div class="activity-num">{aid}</div>
    <div class="activity-title">{aname}</div>
    <div class="activity-desc">{adesc}</div>
  </div>""")

    for rel, cols in release_grids:
        theme = rel.get('theme', 'mvp')
        rbadge = escape(rel.get('badge', 'Release'))
        rtitle = escape(rel.get('title', ''))
        rdesc = escape(rel.get('desc', ''))

        html.append(f"""
  <!-- SWIMLANE {rbadge} -->
  <div class="swimlane-header theme-{theme}">
    <div class="swimlane-badge badge-{theme}">{rbadge}</div>
    <div class="swimlane-title">{rtitle}</div>
    <div class="swimlane-desc">{rdesc}</div>
  </div>""")

        for c_stories in cols:
            html.append('  <div class="cell">')
            if not c_stories:
                html.append('    <div style="color: #64748b; font-size: 12px; text-align: center; padding: 20px;">—</div>')
            else:
                for st in c_stories:
                    sid = escape(st.get('id', 'US'))
                    sfr = escape(st.get('fr', ''))
                    stitle = escape(st.get('title', ''))
                    sdesc = escape(st.get('desc', ''))
                    stag = escape(st.get('tag', '')) if st.get('tag') else ''

                    html.append(f"""    <div class="card card-{theme}">
      <div class="card-header">
        <span class="card-id">{sid}</span>
        {f'<span class="card-fr fr-{theme}">{sfr}</span>' if sfr else ''}
      </div>
      <div class="card-title">{stitle}</div>
      <div class="card-desc">{sdesc}</div>
      {f'<div class="card-highlight">{stag}</div>' if stag else ''}
    </div>""")
            html.append('  </div>')

    html.append("""
</div>
</body>
</html>
""")
    return '\n'.join(html), total_width, total_height


def resolve_output(data_file: Path, output: Path | None) -> Path:
    """Default to the same machine-asset directory render_mermaid uses."""
    if output is not None:
        return output
    return data_file.resolve().parent / '.assets' / 'images' / 'story-map.png'


def render_story_map(data_file: Path, output_file: Path | None = None,
                     html_out: Path | None = None,
                     browser_path: Path | None = None,
                     scale: float = 1.5) -> dict:
    """Render story map JSON to PNG image file."""
    if not data_file.is_file():
        return {'passed': False, 'errors': [f'data file not found: {data_file}']}

    try:
        # utf-8-sig tolerates the BOM Windows editors add, matching the other scripts.
        data = json.loads(data_file.read_text(encoding='utf-8-sig'))
    except Exception as exc:
        return {'passed': False, 'errors': [f'invalid JSON format in {data_file}: {exc}']}

    output_file = resolve_output(data_file, output_file)
    html_content, width, height = generate_story_map_html(data)

    browser = browser_path or find_system_browser()
    if not browser:
        fallback_html = html_out or output_file.with_suffix('.html')
        fallback_html.parent.mkdir(parents=True, exist_ok=True)
        fallback_html.write_text(html_content, encoding='utf-8')
        return {
            'passed': False,
            'errors': ['no Chrome/Edge browser found for headless rendering. Saved standalone HTML instead.'],
            'html': str(fallback_html)
        }

    with tempfile.TemporaryDirectory(prefix='story-map-') as temp_dir:
        temp_html = Path(temp_dir) / 'story_map.html'
        temp_html.write_text(html_content, encoding='utf-8')

        output_file.parent.mkdir(parents=True, exist_ok=True)

        cmd = [
            str(browser),
            '--headless',
            '--disable-gpu',
            '--no-sandbox',
            '--disable-dev-shm-usage',
            f'--force-device-scale-factor={scale}',
            f'--screenshot={output_file.resolve()}',
            f'--window-size={width},{height}',
            f'file:///{temp_html.resolve().as_posix()}',
        ]
        try:
            # errors='replace' keeps a non-UTF-8 browser message from raising here,
            # matching render_mermaid.py; the screenshot result is checked separately.
            res = subprocess.run(cmd, capture_output=True, text=True, errors='replace',
                                 timeout=30)
        except Exception as exc:
            return {'passed': False, 'errors': [f'browser invocation failed: {exc}']}

        if res.returncode != 0 or not output_file.is_file():
            return {
                'passed': False,
                'errors': [f'screenshot failed with exit code {res.returncode}: {res.stderr}'],
            }

    if html_out:
        html_out.parent.mkdir(parents=True, exist_ok=True)
        html_out.write_text(html_content, encoding='utf-8')

    return {
        'passed': True,
        'output': str(output_file.resolve()),
        'width': width,
        'height': height,
        'size': output_file.stat().st_size,
        'browser': str(browser),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--data', required=True, type=Path, help='Path to story map JSON input file')
    parser.add_argument('--output', type=Path,
                        help='Target PNG output image file path (default: <data dir>/.assets/images/story-map.png)')
    parser.add_argument('--html', type=Path, help='Optional output HTML debug file path')
    parser.add_argument('--browser', type=Path, help='Path to Chrome or Edge executable')
    parser.add_argument('--scale', type=float, default=1.5, help='Device scale factor (default: 1.5)')
    args = parser.parse_args(argv)
    # A GBK console cannot encode the report verbatim; match the other scripts.
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    res = render_story_map(
        data_file=args.data,
        output_file=args.output,
        html_out=args.html,
        browser_path=args.browser,
        scale=args.scale,
    )
    print(json.dumps(res, ensure_ascii=False, indent=2))
    return 0 if res.get('passed') else 1


if __name__ == '__main__':
    raise SystemExit(main())
