#!/usr/bin/env python3
"""Render Mermaid blocks in Markdown to deterministic PNG files.

The tool uses Mermaid CLI with an installed Edge/Chrome/Chromium executable.
It reuses valid hash-named PNGs and returns nonzero if any diagram cannot be
rendered. When Mermaid CLI is not installed, npx downloads the pinned package.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile


MMDC_PACKAGE = '@mermaid-js/mermaid-cli@11.17.0'


def mermaid_blocks(text: str) -> list[str]:
    """Extract active, closed Mermaid fenced code blocks."""
    blocks: list[str] = []
    marker: str | None = None
    capture = False
    buffered: list[str] = []
    for line in text.splitlines(keepends=True):
        fence = re.match(r'^\s{0,3}(`{3,}|~{3,})(.*)$', line.rstrip('\r\n'))
        if marker is None and fence:
            marker = fence.group(1)
            info = fence.group(2).strip().split(None, 1)
            capture = bool(info and info[0].casefold() == 'mermaid')
            buffered = []
        elif (marker and fence and fence.group(1)[0] == marker[0] and
              len(fence.group(1)) >= len(marker) and not fence.group(2).strip()):
            if capture:
                blocks.append(''.join(buffered).replace('\r\n', '\n').strip())
            marker = None
            capture = False
            buffered = []
        elif marker and capture:
            buffered.append(line)
    return blocks


def mermaid_asset_stem(source: str) -> str:
    digest = hashlib.sha256(source.encode('utf-8')).hexdigest()[:12]
    return f'mermaid-{digest}'


def valid_png(path: Path) -> bool:
    try:
        data = path.read_bytes()
    except OSError:
        return False
    return len(data) > 24 and data.startswith(b'\x89PNG\r\n\x1a\n') and data[12:16] == b'IHDR'


def find_browser() -> str | None:
    """Find a browser that Mermaid CLI can launch through Puppeteer."""
    candidates = [
        os.environ.get('EDGE_BIN'),
        os.environ.get('CHROME_BIN'),
        r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
        r'C:\Program Files\Microsoft\Edge\Application\msedge.exe',
        r'C:\Program Files\Google\Chrome\Application\chrome.exe',
        r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe',
        'msedge', 'google-chrome', 'chromium-browser', 'chromium',
    ]
    for candidate in candidates:
        if not candidate:
            continue
        path = Path(candidate)
        if path.is_file():
            return str(path.resolve())
        resolved = shutil.which(candidate)
        if resolved:
            return resolved
    return None


def find_renderer() -> list[str] | None:
    """Return an mmdc command, falling back to the pinned package via npx."""
    configured = os.environ.get('MMDC_BIN')
    if configured:
        resolved = shutil.which(configured)
        if resolved:
            return [resolved]
        path = Path(configured)
        if path.is_file():
            return [str(path.resolve())]
    resolved = shutil.which('mmdc')
    if resolved:
        return [resolved]
    npx = shutil.which('npx')
    if npx:
        return [npx, '--yes', '--package', MMDC_PACKAGE, 'mmdc']
    return None


def render_block(source: str, output: Path, renderer: list[str], browser: str,
                 timeout: int = 120) -> tuple[bool, str]:
    """Render one Mermaid definition directly to an opaque, high-resolution PNG."""
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='prd-refiner-mermaid-') as temp_name:
        temp = Path(temp_name)
        input_file = temp / 'diagram.mmd'
        config_file = temp / 'puppeteer.json'
        input_file.write_text(source + '\n', encoding='utf-8')
        config_file.write_text(json.dumps({'executablePath': browser}, ensure_ascii=False),
                               encoding='utf-8')
        command = renderer + [
            '--input', str(input_file),
            '--output', str(output),
            '--backgroundColor', '#ffffff',
            '--scale', '2',
            '--puppeteerConfigFile', str(config_file),
        ]
        environment = os.environ.copy()
        environment['PUPPETEER_SKIP_DOWNLOAD'] = 'true'
        environment['PUPPETEER_EXECUTABLE_PATH'] = browser
        try:
            completed = subprocess.run(command, capture_output=True, text=True, errors='replace',
                                       timeout=timeout, env=environment)
        except (OSError, subprocess.SubprocessError) as exc:
            return False, f'{type(exc).__name__}: {exc}'
    if completed.returncode != 0:
        detail = (completed.stderr or completed.stdout or 'Mermaid CLI failed').strip()
        return False, detail[-1200:]
    if not valid_png(output):
        return False, 'Mermaid CLI did not produce a valid PNG'
    return True, ''


def process_markdown(markdown_path: Path, output_dir: Path | None = None, *,
                     force: bool = False, timeout: int = 120) -> dict:
    """Render every distinct Mermaid block and return a machine-readable report."""
    text = markdown_path.read_text(encoding='utf-8-sig')
    blocks = list(dict.fromkeys(mermaid_blocks(text)))
    target_dir = output_dir or (markdown_path.parent / '.assets' / markdown_path.stem / 'images')
    results = []
    renderer: list[str] | None = None
    browser: str | None = None

    for block in blocks:
        stem = mermaid_asset_stem(block)
        png_file = target_dir / f'{stem}.png'
        if not force and valid_png(png_file):
            results.append({'stem': stem, 'status': 'reused', 'png': str(png_file)})
            continue
        if renderer is None:
            renderer = find_renderer()
        if browser is None:
            browser = find_browser()
        if renderer is None or browser is None:
            missing = 'Mermaid CLI/npx' if renderer is None else 'Edge/Chrome/Chromium'
            results.append({'stem': stem, 'status': 'failed',
                            'error': f'{missing} is unavailable'})
            continue
        try:
            png_file.unlink(missing_ok=True)
        except OSError:
            pass
        ok, error = render_block(block, png_file, renderer, browser, timeout)
        item = {'stem': stem, 'status': 'rendered' if ok else 'failed'}
        if ok:
            item['png'] = str(png_file)
        else:
            item['error'] = error
        results.append(item)

    failed = [item for item in results if item['status'] == 'failed']
    status = 'empty' if not blocks else ('failed' if failed else 'complete')
    return {
        'status': status,
        'markdown': str(markdown_path),
        'output_dir': str(target_dir),
        'renderer': renderer,
        'browser': browser,
        'results': results,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description='Render Mermaid blocks in Markdown to hash-named PNG files')
    parser.add_argument('markdown', type=Path, help='Target Markdown PRD')
    parser.add_argument('--output-dir', type=Path, help='PNG output directory')
    parser.add_argument('--force', action='store_true', help='Render again when a valid PNG exists')
    parser.add_argument('--timeout', type=int, default=120, help='Seconds allowed per diagram')
    args = parser.parse_args()
    if not args.markdown.is_file():
        print(json.dumps({'status': 'failed', 'error': f'file not found: {args.markdown}'},
                         ensure_ascii=False, indent=2))
        return 1
    try:
        result = process_markdown(args.markdown, args.output_dir,
                                  force=args.force, timeout=args.timeout)
    except (OSError, UnicodeError, ValueError) as exc:
        result = {'status': 'failed', 'error': f'{type(exc).__name__}: {exc}'}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result.get('status') in {'complete', 'empty'} else 1


if __name__ == '__main__':
    raise SystemExit(main())
