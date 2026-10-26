#!/usr/bin/env python3
"""Check the two-way closure between a PRD's frame tables and its frame manifest.

The manifest is a machine asset at `<workspace>/.assets/frames/manifest.json`; the
PRD is the human-readable delivery. This checker never fetches anything: it only
compares the two local sources and the exported image files they name.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

from validate_prd import (FRAME_ID, body_without_metadata, fr_blocks,
                          without_fenced_code)


MANIFEST_NAME = 'manifest.json'
FR_PATTERN = r'FR-\d{2,4}'
DERIVED_SUFFIXES = ('_需求探讨.md', '_竞品分析.md', '_澄清决策记录.md', '_帮助初稿.md')


def default_prd(workspace: Path) -> Path | None:
    """Prefer prd.md; otherwise accept exactly one root-level main draft."""
    direct = workspace / 'prd.md'
    if direct.is_file():
        return direct
    candidates = [path for path in sorted(workspace.glob('*.md'))
                  if not path.name.endswith(DERIVED_SUFFIXES)]
    return candidates[0] if len(candidates) == 1 else None


def load_manifest(path: Path, errors: list[str], warnings: list[str]) -> list[dict] | None:
    if not path.is_file():
        return None
    try:
        data = json.loads(path.read_text(encoding='utf-8-sig'))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        errors.append(f'cannot read frame manifest: {type(exc).__name__}: {path.name}')
        return None
    if not isinstance(data, dict) or not isinstance(data.get('frames'), list):
        errors.append('malformed frame manifest: top level must be an object with a frames array')
        return None
    frames = []
    seen = set()
    for index, entry in enumerate(data['frames']):
        label = f'frames[{index}]'
        if not isinstance(entry, dict):
            errors.append(f'{label} must be an object')
            continue
        missing = [key for key in ('id', 'fr', 'state', 'image')
                   if not isinstance(entry.get(key), str) or not entry[key].strip()]
        if missing:
            errors.append(f'{label} missing or empty: ' + ', '.join(missing))
            continue
        item = entry['id'].strip()
        if not FRAME_ID.fullmatch(item):
            errors.append(f'{label} id must look like FR-001-S1: {entry["id"]!r}')
            continue
        if not re.fullmatch(FR_PATTERN, entry['fr'].strip()):
            errors.append(f'{label} fr must look like FR-001: {entry["fr"]!r}')
            continue
        if item in seen:
            errors.append(f'duplicate frame id in manifest: {item}')
            continue
        seen.add(item)
        frames.append(entry)
    if not data.get('requirement'):
        warnings.append('manifest has no requirement name; add it for traceability')
    return frames


def safe_image(workspace: Path, image: str, errors: list[str]) -> Path | None:
    """Frame images are local and must stay inside the workspace."""
    target = Path(image)
    if target.is_absolute():
        errors.append(f'frame image must be a workspace-relative path: {image}')
        return None
    resolved = (workspace / target).resolve()
    try:
        resolved.relative_to(workspace.resolve())
    except (ValueError, OSError):
        errors.append(f'frame image leaves the workspace: {image}')
        return None
    return resolved


def inspect(workspace: Path, prd: Path | None = None,
            manifest: Path | None = None) -> dict:
    workspace = Path(workspace).resolve()
    prd = Path(prd).resolve() if prd else default_prd(workspace)
    manifest = Path(manifest).resolve() if manifest else workspace / '.assets' / 'frames' / MANIFEST_NAME
    result = {
        'workspace': str(workspace), 'prd': str(prd) if prd else None,
        'manifest': str(manifest), 'errors': [], 'warnings': [],
        'scope': 'Frame closure only; image content and interaction quality require review.',
    }
    errors, warnings = result['errors'], result['warnings']

    if prd is None or not prd.is_file():
        errors.append('no PRD found: pass --prd or keep one main .md in the workspace root')
        result['passed'] = False
        return result
    try:
        text = prd.read_text(encoding='utf-8-sig')
    except (OSError, UnicodeError) as exc:
        errors.append(f'cannot read PRD: {type(exc).__name__}: {prd}')
        result['passed'] = False
        return result

    body = body_without_metadata(without_fenced_code(text))
    prd_frames = sorted(set(FRAME_ID.findall(body)))
    defined_frs = {item for item, _ in fr_blocks(body)}
    frames = load_manifest(manifest, errors, warnings)
    manifest_frames = {entry['id'].strip(): entry for entry in (frames or [])}
    result['counts'] = {'prd_frames': len(prd_frames),
                        'manifest_frames': len(manifest_frames),
                        'defined_frs': len(defined_frs)}

    if frames is None:
        if prd_frames:
            errors.append('PRD references frames but .assets/frames/manifest.json is missing')
        else:
            result['warnings'].append('no interaction frames in PRD and no manifest; nothing to check')
        result['passed'] = not errors
        return result

    if not prd_frames:
        errors.append('manifest lists frames but the PRD references none')

    for frame in prd_frames:
        if frame not in manifest_frames:
            errors.append(f'frame in PRD but not in manifest: {frame}')
    for frame in sorted(manifest_frames):
        if frame not in prd_frames:
            errors.append(f'orphan frame in manifest but not in PRD: {frame}')

    for frame, entry in manifest_frames.items():
        image = safe_image(workspace, entry['image'].strip(), errors)
        if image is None:
            continue
        if not image.is_file():
            errors.append(f'frame image not found: {entry["image"]}')
        elif image.stat().st_size == 0:
            errors.append(f'frame image is empty: {entry["image"]}')
        elif Path(entry['image'].strip()).name not in text:
            warnings.append(f'frame image is not referenced in the PRD body: {entry["image"]}')
        if not entry.get('captured'):
            warnings.append(f'frame has no capture date: {frame}')
        if not entry.get('source'):
            warnings.append(f'frame has no prototype source: {frame}')
        fr = entry['fr'].strip()
        if fr not in defined_frs:
            errors.append(f'frame {frame} points to an FR that the PRD does not define: {fr}')

    result['passed'] = not errors
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--workspace', required=True, type=Path,
                        help='Requirement workspace root (absolute path)')
    parser.add_argument('--prd', type=Path,
                        help='PRD file; default: workspace/prd.md or the single root-level draft')
    parser.add_argument('--manifest', type=Path,
                        help='frame manifest; default: <workspace>/.assets/frames/manifest.json')
    parser.add_argument('--json', action='store_true', help='emit machine-readable results')
    args = parser.parse_args(argv)
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    result = inspect(args.workspace, args.prd, args.manifest)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print('Frame closure passed.' if result['passed'] else 'Frame closure failed.')
        for label in ('errors', 'warnings'):
            for message in result[label]:
                print(f'{label}: {message}')
        print(result['scope'])
    return 0 if result['passed'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
