#!/usr/bin/env python3
"""Assemble per-FR specification shards and audit Nova-Proto HTML component coverage.

Supports multi-session concurrent workflows where each feature lives in
`<workspace>/features/FR-xxx_<name>/` with its own `prototype.html` and `spec.md`.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
BUNDLED_NOVA_DIR = SKILL_ROOT / 'assets' / 'nova-proto'
NOVA_RUNTIME_FILES = ('cad-design-tokens.css', 'cad-components.js')

OFFICIAL_TAGS = frozenset({
    'cad-button', 'cad-input', 'cad-checkbox', 'cad-radio',
    'cad-select', 'cad-switch', 'cad-slider', 'cad-dialog',
    'cad-tabs', 'cad-alert', 'cad-form-group', 'cad-divider',
    'cad-icon', 'cad-table', 'cad-tag', 'cad-file-loader',
    'cad-picker', 'cad-banner',
})

INSERT_MARKER = '<!-- FEATURES_INSERT_POINT -->'
FR_DIR_PATTERN = re.compile(r'^(FR-(\d{2,4}))(?:[_-](.*))?$', re.IGNORECASE)


def sync_nova_runtime(workspace: Path) -> list[str]:
    """Copy bundled Nova-Proto runtime (CSS & JS) into `<workspace>/.assets/nova-proto/`."""
    target_dir = Path(workspace).resolve() / '.assets' / 'nova-proto'
    target_dir.mkdir(parents=True, exist_ok=True)
    copied: list[str] = []
    for filename in NOVA_RUNTIME_FILES:
        src = BUNDLED_NOVA_DIR / filename
        if src.is_file():
            dst = target_dir / filename
            shutil.copy2(src, dst)
            copied.append(str(dst))
    return copied


def strip_non_dom(raw_html: str) -> str:
    """Remove HTML comments, script blocks, and style blocks before tag scanning."""
    content = re.sub(r'<!--[\s\S]*?-->', '', raw_html)
    content = re.sub(r'<script\b[^>]*>[\s\S]*?</script>', '', content, flags=re.IGNORECASE)
    content = re.sub(r'<style\b[^>]*>[\s\S]*?</style>', '', content, flags=re.IGNORECASE)
    return content


def _extract_attr(attrs: str, name: str) -> str:
    match = re.search(rf'\b{re.escape(name)}\s*=\s*["\']([^"\']*)["\']', attrs, re.IGNORECASE)
    return match.group(1).strip() if match else ''


def audit_prototype_html(html_path: Path, fr_id: str = '') -> dict:
    """Audit a single prototype.html for <cad-*> component coverage and zero raw HTML."""
    raw_content = html_path.read_text(encoding='utf-8-sig')
    content = strip_non_dom(raw_content)

    cad_matches = re.findall(r'<(cad-[a-z0-9\-]+)([^>]*)>', content, flags=re.IGNORECASE)
    official: list[str] = []
    drafts: list[dict] = []

    for tag, attrs in cad_matches:
        tag_lower = tag.lower()
        status_attr = _extract_attr(attrs, 'status').lower()
        is_draft = (
            status_attr == 'draft'
            or 'draft' in tag_lower
            or tag_lower not in OFFICIAL_TAGS
        )
        if is_draft:
            label = (
                _extract_attr(attrs, 'label')
                or _extract_attr(attrs, 'title')
                or _extract_attr(attrs, 'placeholder')
                or '待补充描述'
            )
            drafts.append({
                'fr': fr_id or html_path.parent.name,
                'tag': tag_lower,
                'label': label,
                'file': str(html_path.name),
            })
        else:
            official.append(tag_lower)

    raw_matches = re.findall(r'<(input|button|select|textarea)\b([^>]*)>', content, flags=re.IGNORECASE)
    raw_elements: list[str] = []
    for tag, attrs in raw_matches:
        elem_type = _extract_attr(attrs, 'type').lower() or 'text'
        if elem_type == 'hidden':
            continue
        raw_elements.append(f'<{tag.lower()} type="{elem_type}">')

    total = len(official) + len(drafts) + len(raw_elements)
    coverage = ((len(official) + len(drafts)) / total * 100.0) if total > 0 else 100.0

    return {
        'fr': fr_id or html_path.parent.name,
        'prototype': str(html_path),
        'total_interactive': total,
        'official_count': len(official),
        'draft_count': len(drafts),
        'raw_count': len(raw_elements),
        'coverage_rate': round(coverage, 1),
        'draft_components': drafts,
        'raw_elements': raw_elements,
        'passed': len(raw_elements) == 0,
    }


def normalize_shard_images(spec_text: str) -> str:
    """Normalize `../../.assets/images/...` inside a shard spec to `.assets/images/...`."""
    return re.sub(
        r'(\!\[[^\]\n]*\]\(\s*)(?:\.\./)+(\.assets/)',
        r'\1\2',
        spec_text,
    )


def write_missing_components(workspace: Path, drafts: list[dict]) -> Path | None:
    """Write or update Missing_Components.md when draft components exist."""
    target = workspace / 'Missing_Components.md'
    if not drafts:
        return None
    seen: set[tuple[str, str, str]] = set()
    rows: list[str] = []
    for item in drafts:
        key = (item['fr'], item['tag'], item['label'])
        if key in seen:
            continue
        seen.add(key)
        rows.append(
            f"| {item['fr']} | `{item['tag']}` | {item['label']} | `{item['file']}` | 待设计师补充 Figma 组件 |"
        )
    lines = [
        '# 缺失组件补充需求单 (Missing Components)',
        '',
        '> 本清单由 `assemble_prd.py` 扫描各功能分片 `prototype.html` 中的 `status="draft"` 组件自动汇总，供 UI 设计师在 Figma 组件库中补齐。',
        '',
        '| 所属功能 | 草稿组件标签 | 场景与用途说明 | 所在原型文件 | 状态 |',
        '|---|---|---|---|---|',
        *rows,
        '',
    ]
    target.write_text('\n'.join(lines), encoding='utf-8')
    return target


def discover_shards(workspace: Path) -> list[tuple[int, str, Path]]:
    """Return sorted feature shard directories `(sort_num, fr_id, dir_path)`."""
    features_dir = workspace / 'features'
    if not features_dir.is_dir():
        return []
    shards: list[tuple[int, str, Path]] = []
    for child in sorted(features_dir.iterdir()):
        if not child.is_dir():
            continue
        match = FR_DIR_PATTERN.match(child.name)
        if match:
            fr_id = match.group(1).upper()
            num = int(match.group(2))
            shards.append((num, fr_id, child))
    shards.sort(key=lambda item: (item[0], item[1]))
    return shards


def inject_specs_into_overview(overview_text: str, combined_specs: str) -> str:
    """Insert combined FR specs at `<!-- FEATURES_INSERT_POINT -->` or after section 3.1."""
    if INSERT_MARKER in overview_text:
        return overview_text.replace(INSERT_MARKER, combined_specs.strip(), 1)
    lines = overview_text.splitlines()
    in_sec3 = False
    insert_idx = len(lines)
    for idx, line in enumerate(lines):
        if re.match(r'^##\s+3\.', line.strip()):
            in_sec3 = True
            continue
        if in_sec3 and re.match(r'^##\s+[4-9]\.', line.strip()):
            insert_idx = idx
            break
    before = '\n'.join(lines[:insert_idx]).rstrip()
    after = '\n'.join(lines[insert_idx:]).lstrip()
    parts = [p for p in (before, combined_specs.strip(), after) if p]
    return '\n\n'.join(parts) + '\n'


def assemble(workspace: Path, output: Path | None = None,
             overview: Path | None = None, *, init_only: bool = False) -> dict:
    workspace = Path(workspace).resolve()
    runtime_files = sync_nova_runtime(workspace)
    if init_only:
        return {
            'workspace': str(workspace),
            'runtime_files': runtime_files,
            'passed': len(runtime_files) == len(NOVA_RUNTIME_FILES),
            'errors': [] if len(runtime_files) == len(NOVA_RUNTIME_FILES) else ['failed to copy Nova-Proto runtime assets'],
            'warnings': [],
        }

    overview_path = Path(overview).resolve() if overview else workspace / '00_需求总览.md'
    output_path = Path(output).resolve() if output else workspace / 'prd.md'

    errors: list[str] = []
    warnings: list[str] = []
    audits: list[dict] = []
    all_drafts: list[dict] = []

    if not overview_path.is_file():
        errors.append(f'overview file not found: {overview_path}')
        return {
            'workspace': str(workspace),
            'output': str(output_path),
            'runtime_files': runtime_files,
            'passed': False,
            'errors': errors,
            'warnings': warnings,
            'audits': audits,
        }

    shards = discover_shards(workspace)
    if not shards:
        errors.append('no FR shard directories found under <workspace>/features/ (expected e.g. features/FR-001_name/)')
        return {
            'workspace': str(workspace),
            'output': str(output_path),
            'runtime_files': runtime_files,
            'passed': False,
            'errors': errors,
            'warnings': warnings,
            'audits': audits,
        }

    spec_blocks: list[str] = []
    for _, fr_id, shard_dir in shards:
        proto_path = shard_dir / 'prototype.html'
        spec_path = shard_dir / 'spec.md'

        if proto_path.is_file():
            audit = audit_prototype_html(proto_path, fr_id=fr_id)
            audits.append(audit)
            all_drafts.extend(audit['draft_components'])
            if not audit['passed']:
                errors.append(
                    f"{fr_id} prototype.html contains {audit['raw_count']} raw HTML interactive tag(s): "
                    f"{', '.join(audit['raw_elements'][:5])}; use official <cad-*> components or mark status=\"draft\""
                )
        else:
            warnings.append(f'{fr_id} has no prototype.html in {shard_dir.name}')

        if not spec_path.is_file():
            errors.append(f'{fr_id} missing spec.md in {shard_dir.name}')
            continue
        raw_spec = spec_path.read_text(encoding='utf-8-sig').strip()
        if not raw_spec:
            errors.append(f'{fr_id} spec.md is empty in {shard_dir.name}')
            continue
        spec_blocks.append(normalize_shard_images(raw_spec))

    missing_doc = write_missing_components(workspace, all_drafts)

    if not errors:
        overview_text = overview_path.read_text(encoding='utf-8-sig')
        merged = inject_specs_into_overview(overview_text, '\n\n'.join(spec_blocks))
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(merged, encoding='utf-8')

    return {
        'workspace': str(workspace),
        'overview': str(overview_path),
        'output': str(output_path),
        'runtime_files': runtime_files,
        'shards_count': len(shards),
        'draft_components_count': len(all_drafts),
        'missing_components_file': str(missing_doc) if missing_doc else None,
        'audits': audits,
        'errors': errors,
        'warnings': warnings,
        'passed': not errors,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--workspace', required=True, type=Path,
                        help='Requirement workspace root directory (absolute path)')
    parser.add_argument('--output', type=Path,
                        help='Assembled PRD output path (default: <workspace>/prd.md)')
    parser.add_argument('--overview', type=Path,
                        help='Overview markdown file (default: <workspace>/00_需求总览.md)')
    parser.add_argument('--init-only', action='store_true',
                        help='Only sync bundled Nova-Proto CSS/JS runtime into <workspace>/.assets/nova-proto/')
    parser.add_argument('--json', action='store_true', help='Emit JSON report')
    args = parser.parse_args(argv)
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    result = assemble(args.workspace, output=args.output, overview=args.overview, init_only=args.init_only)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print('PRD assembly passed.' if result['passed'] else 'PRD assembly failed.')
        for label in ('errors', 'warnings'):
            for msg in result[label]:
                print(f'{label}: {msg}')
    return 0 if result['passed'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
