#!/usr/bin/env python3
"""Render a 2D user story map to SVG or PNG without external renderers.

Reuses the scene layout from ``story_map_to_excalidraw`` so the picture and the
editable ``.excalidraw`` file share one geometry. SVG is serialized here in pure
Python; PNG is rasterized by a headless browser through canvas ``drawImage`` +
``toBlob`` (the same browser rasterization excalidraw.com itself uses) — not a
page screenshot, so nothing gets clipped and ``--scale`` controls resolution.

The input JSON contract is documented in assets/story-map-schema.md.
"""
from __future__ import annotations

import argparse
from html import escape
import http.server
import json
import os
from pathlib import Path
import shutil
import socketserver
import struct
import subprocess
import sys
import tempfile
import threading
import time

from story_map_to_excalidraw import build_scene

SVG_PADDING = 10
SVG_FONT = "'Microsoft YaHei', 'PingFang SC', 'Segoe UI', sans-serif"
SVG_RADIUS = 8
DEFAULT_TIMEOUT = 60


def find_system_browser() -> Path | None:
    """Discover an installed Chrome, Edge, or Chromium executable."""
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
    for candidate in candidates:
        if candidate.is_file():
            return candidate

    for name in ('msedge', 'google-chrome', 'chrome', 'chromium'):
        found = shutil.which(name)
        if found and Path(found).is_file():
            return Path(found)
    return None


def _text_lines(element: dict) -> list[str]:
    return element.get('text', '').split('\n')


def _baseline_y(element: dict, index: int) -> float:
    font_size = element['fontSize']
    line_height = font_size * element.get('lineHeight', 1.25)
    lines = _text_lines(element)
    block = len(lines) * line_height
    top = element['y'] + max(0.0, (element['height'] - block) / 2)
    return top + index * line_height + font_size * 0.82


def scene_to_svg(scene: dict) -> str:
    """Serialize a scene built by build_scene() to a standalone SVG document."""
    elements = [e for e in scene.get('elements', []) if not e.get('isDeleted')]
    if not elements:
        raise ValueError('scene has no elements')
    min_x = min(e['x'] for e in elements) - SVG_PADDING
    min_y = min(e['y'] for e in elements) - SVG_PADDING
    max_x = max(e['x'] + e['width'] for e in elements) + SVG_PADDING
    max_y = max(e['y'] + e['height'] for e in elements) + SVG_PADDING
    width = max_x - min_x
    height = max_y - min_y

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width:.0f}" height="{height:.0f}" '
        f'viewBox="0 0 {width:.0f} {height:.0f}">',
        f'<rect x="0" y="0" width="{width:.0f}" height="{height:.0f}" fill="#ffffff"/>',
        f'<g transform="translate({-min_x:.2f} {-min_y:.2f})">',
    ]
    for element in elements:
        x, y = element['x'], element['y']
        w, h = element['width'], element['height']
        if element['type'] == 'rectangle':
            dash = ' stroke-dasharray="8 6"' if element.get('strokeStyle') == 'dashed' else ''
            parts.append(
                f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" '
                f'rx="{SVG_RADIUS}" fill="{element.get("backgroundColor", "none")}" '
                f'stroke="{element.get("strokeColor", "none")}" '
                f'stroke-width="{element.get("strokeWidth", 1)}"{dash}/>'
            )
        elif element['type'] == 'text':
            anchor = 'middle' if element.get('textAlign') == 'center' else 'start'
            text_x = x + (w / 2 if anchor == 'middle' else 0)
            color = element.get('strokeColor', '#1e293b')
            font_size = element['fontSize']
            for index, line in enumerate(_text_lines(element)):
                if not line:
                    continue
                parts.append(
                    f'<text x="{text_x:.2f}" y="{_baseline_y(element, index):.2f}" '
                    f'font-family="{SVG_FONT}" font-size="{font_size}" fill="{color}" '
                    f'text-anchor="{anchor}" xml:space="preserve">{escape(line)}</text>'
                )
    parts.append('</g>')
    parts.append('</svg>')
    return '\n'.join(parts) + '\n'


def _png_size(path: Path) -> tuple[int, int]:
    with path.open('rb') as handle:
        head = handle.read(33)
    if head[:8] != b'\x89PNG\r\n\x1a\n':
        return 0, 0
    return struct.unpack('>II', head[16:24])


class _Rasterizer(http.server.BaseHTTPRequestHandler):
    svg_bytes = b''
    scale = 1.0
    output: Path | None = None
    done: threading.Event | None = None

    def log_message(self, *args) -> None:  # keep the CLI quiet
        pass

    def do_GET(self) -> None:  # noqa: N802 - http.server API
        if self.path == '/':
            page = f"""<!doctype html><meta charset="utf-8"><body><script>
const scale = {self.scale};
const img = new Image();
img.onload = () => {{
  const canvas = document.createElement('canvas');
  canvas.width = Math.max(1, Math.round(img.naturalWidth * scale));
  canvas.height = Math.max(1, Math.round(img.naturalHeight * scale));
  const ctx = canvas.getContext('2d');
  ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
  canvas.toBlob(async (blob) => {{
    const bytes = await blob.arrayBuffer();
    await fetch('/result', {{ method: 'POST', body: bytes }});
  }}, 'image/png');
}};
img.onerror = async () => {{
  await fetch('/result', {{ method: 'POST', body: 'SVG_LOAD_FAILED' }});
}};
img.src = '/scene.svg';
</script>"""
            body = page.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        elif self.path == '/scene.svg':
            body = self.svg_bytes
            self.send_response(200)
            self.send_header('Content-Type', 'image/svg+xml')
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self) -> None:  # noqa: N802 - http.server API
        length = int(self.headers.get('Content-Length') or 0)
        payload = self.rfile.read(length)
        if payload != b'SVG_LOAD_FAILED' and self.output is not None:
            self.output.write_bytes(payload)
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'ok')
        if self.done is not None:
            self.done.set()


def rasterize_svg(svg_text: str, output_file: Path, *, scale: float = 1.0,
                  browser: Path, timeout: float = DEFAULT_TIMEOUT) -> dict:
    """Rasterize SVG to PNG in a headless browser at the requested scale."""
    done = threading.Event()
    handler = type('Handler', (_Rasterizer,), {
        'svg_bytes': svg_text.encode('utf-8'),
        'scale': scale,
        'output': output_file,
        'done': done,
    })
    server = socketserver.ThreadingTCPServer(('127.0.0.1', 0), handler)
    server.daemon_threads = True
    port = server.server_address[1]
    threading.Thread(target=server.serve_forever, daemon=True).start()

    output_file.parent.mkdir(parents=True, exist_ok=True)
    profile = tempfile.mkdtemp(prefix='story-map-raster-')
    try:
        process = subprocess.Popen(
            [str(browser), '--headless', '--disable-gpu', '--no-sandbox', '--no-first-run',
             '--disable-extensions', f'--user-data-dir={profile}', '--hide-scrollbars',
             f'http://127.0.0.1:{port}/'],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
    except OSError as exc:
        server.shutdown()
        return {'passed': False, 'errors': [f'failed to launch browser {browser}: {exc}']}
    started = time.time()
    try:
        received = done.wait(timeout)
    finally:
        process.terminate()
        try:
            process.wait(timeout=5)
        except Exception:
            process.kill()
        server.shutdown()
        shutil.rmtree(profile, ignore_errors=True)
    if not received:
        return {'passed': False, 'errors': [f'headless browser produced no image within {timeout:.0f}s']}
    width, height = _png_size(output_file)
    if width <= 0:
        return {'passed': False, 'errors': ['browser returned no PNG data']}
    return {'passed': True, 'width': width, 'height': height,
            'size': output_file.stat().st_size,
            'seconds': round(time.time() - started, 2)}


def render_story_map_vector(data_file: Path, output_file: Path, *, fmt: str = 'png',
                            scale: float = 1.0, browser_path: Path | None = None,
                            strip_emoji: bool = False, timeout: float = DEFAULT_TIMEOUT) -> dict:
    if fmt not in ('png', 'svg'):
        return {'passed': False, 'errors': [f'unsupported format: {fmt}']}
    if not data_file.is_file():
        return {'passed': False, 'errors': [f'data file not found: {data_file}']}
    try:
        data = json.loads(data_file.read_text(encoding='utf-8-sig'))
    except Exception as exc:
        return {'passed': False, 'errors': [f'invalid JSON format in {data_file}: {exc}']}
    try:
        scene = build_scene(data, strip_emoji=strip_emoji)
        svg_text = scene_to_svg(scene)
    except ValueError as exc:
        return {'passed': False, 'errors': [str(exc)]}

    output_file.parent.mkdir(parents=True, exist_ok=True)
    if fmt == 'svg':
        output_file.write_text(svg_text, encoding='utf-8')
        return {'passed': True, 'format': 'svg', 'output': str(output_file.resolve()),
                'size': output_file.stat().st_size}

    browser = browser_path or find_system_browser()
    if not browser:
        return {'passed': False, 'errors': ['no Chrome/Edge found for PNG rasterization; '
                                            'use --format svg or install a browser']}
    result = rasterize_svg(svg_text, output_file, scale=scale, browser=browser, timeout=timeout)
    if result.get('passed'):
        result.update({'format': 'png', 'output': str(output_file.resolve()),
                       'scale': scale, 'elements': len(scene['elements'])})
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--data', required=True, type=Path, help='Story map JSON input file')
    parser.add_argument('--output', required=True, type=Path,
                        help='Output image path (.png or .svg)')
    parser.add_argument('--format', choices=('png', 'svg'), default='png')
    parser.add_argument('--scale', type=float, default=2.0, help='PNG pixel scale (default: 2)')
    parser.add_argument('--browser', type=Path, help='Chrome/Edge executable path')
    parser.add_argument('--strip-emoji', action='store_true',
                        help='Remove emoji/symbols (default: keep them; browsers render them fine)')
    parser.add_argument('--timeout', type=float, default=DEFAULT_TIMEOUT,
                        help=f'Browser rasterization timeout in seconds (default: {DEFAULT_TIMEOUT})')
    args = parser.parse_args(argv)
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    result = render_story_map_vector(
        args.data, args.output, fmt=args.format, scale=args.scale,
        browser_path=args.browser, strip_emoji=args.strip_emoji, timeout=args.timeout,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result.get('passed') else 1


if __name__ == '__main__':
    raise SystemExit(main())
