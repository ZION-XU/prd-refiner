#!/usr/bin/env python3
"""Read-only Confluence delivery gate: local Markdown, Storage links and TOC.

Run against the exact submitted body, then again against the server readback.
Passing is static evidence only, never proof of browser clicks or floating CSS.
Exceptions describe explicit user choices; the script cannot verify consent.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit
import xml.etree.ElementTree as ET

from build_snapshot import valid_image
from validate_links import active_lines, inspect, parse_storage, storage_markdown
from validate_prd import (validate as validate_prd, definitions_in, ID_PATTERN,
                          HTMLImages, INLINE_IMAGE, REFERENCE_IMAGE, REFERENCE_LINK,
                          without_fenced_code)
from validate_prd import compare_source_images, compare_image_counts, image_reference_count

AC = '{urn:ac}'


def mermaid_blocks(text: str) -> tuple[list[str], bool]:
    """Extract active Mermaid fenced blocks and report an unclosed block."""
    blocks = []
    marker = None
    capture = False
    buffered = []
    for line in text.splitlines(keepends=True):
        fence = re.match(r'^\s{0,3}(`{3,}|~{3,})(.*)$', line.rstrip('\r\n'))
        if marker is None and fence:
            marker = fence.group(1)
            info = fence.group(2).strip().split(None, 1)
            capture = bool(info and info[0].casefold() == 'mermaid')
            buffered = []
        elif marker and fence and fence.group(1)[0] == marker[0] and len(fence.group(1)) >= len(marker) and not fence.group(2).strip():
            if capture:
                blocks.append(''.join(buffered).replace('\r\n', '\n').strip())
            marker = None
            capture = False
            buffered = []
        elif marker and capture:
            buffered.append(line)
    return blocks, bool(marker and capture)


def mermaid_asset_stem(source: str) -> str:
    digest = hashlib.sha256(source.encode('utf-8')).hexdigest()[:12]
    return f'mermaid-{digest}'


def inspect_mermaid_delivery(markdown: str, storage: str, workspace: Path) -> tuple[dict, list[str]]:
    blocks, unclosed = mermaid_blocks(markdown)
    stems = sorted({mermaid_asset_stem(block) for block in blocks})
    local_files = {
        path.name: path for path in workspace.rglob('*')
        if path.is_file() and path.suffix.casefold() == '.png'
    }
    attachment_names = set(re.findall(
        r'<ri:attachment\b[^>]*\bri:filename=["\']([^"\']+)["\']', storage, re.IGNORECASE))
    errors = []
    if unclosed:
        errors.append('Markdown contains an unclosed Mermaid fenced block')
    for stem in stems:
        expected = stem + '.png'
        local = expected in local_files and valid_image(local_files[expected])
        remote = expected in attachment_names
        if not local:
            errors.append(f'Mermaid diagram lacks rendered local PNG: {expected}')
        if not remote:
            errors.append(f'Mermaid diagram lacks Confluence PNG attachment reference: {expected}')
    if re.search(r'(?:```|~~~)\s*mermaid\b', storage, re.IGNORECASE):
        errors.append('Storage must replace Mermaid fences with uploaded attachment images')
    try:
        for node in parse_storage(storage).iter(AC + 'structured-macro'):
            if node.get(AC + 'name') not in {'code', 'noformat'}:
                continue
            parameters = ' '.join(''.join(p.itertext()) for p in node.findall(AC + 'parameter'))
            if 'mermaid' in parameters.casefold():
                errors.append('Storage must not publish Mermaid as a code/noformat macro')
    except (ValueError, ET.ParseError):
        pass
    return {
        'source_blocks': len(blocks),
        'expected_assets': [stem + '.png' for stem in stems],
        'attachment_references': sorted(attachment_names),
    }, errors


def extract_local_image_filenames(markdown: str) -> list[str]:
    """Return sorted basenames of local images referenced in active Markdown."""
    active = without_fenced_code(re.sub(r'<!--[\s\S]*?-->', '', markdown))
    refs = {m.group(1).strip().casefold(): m.group(2) for m in REFERENCE_LINK.finditer(active)}
    targets = [m.group(1) for m in INLINE_IMAGE.finditer(active)]
    html_images = HTMLImages()
    html_images.feed(active)
    targets.extend(html_images.targets)
    for match in REFERENCE_IMAGE.finditer(active):
        label = (match.group(2) or match.group(1)).strip().casefold()
        if label in refs:
            targets.append(refs[label])
    filenames: set[str] = set()
    for target in targets:
        cleaned = target.strip('<>')
        if not cleaned or cleaned.startswith('//') or re.match(r'^(?:https?|data):', cleaned, re.IGNORECASE):
            continue
        file_path = unquote(urlsplit(cleaned).path)
        if file_path and Path(file_path).name:
            filenames.add(Path(file_path).name)
    return sorted(filenames)


def inspect_local_image_delivery(markdown: str | None, storage: str, *,
                                 image_policy: str = 'local') -> tuple[list[str], list[str]]:
    """Verify local Markdown images are mapped to Confluence attachment tags in Storage."""
    errors: list[str] = []
    local_filenames = extract_local_image_filenames(markdown) if markdown else []
    attachment_names = set(re.findall(
        r'<ri:attachment\b[^>]*\bri:filename=["\']([^"\']+)["\']', storage, re.IGNORECASE))
    if image_policy == 'local':
        for filename in local_filenames:
            if filename not in attachment_names:
                errors.append(f'Local image lacks Confluence attachment reference in Storage: {filename}')
        storage_images = HTMLImages()
        storage_images.feed(storage)
        for src in storage_images.targets:
            cleaned = src.strip()
            if cleaned and not cleaned.startswith('//') and not re.match(r'^(?:https?|data):', cleaned, re.IGNORECASE):
                errors.append(f'Storage must use ri:attachment instead of local img src: {cleaned}')
    return local_filenames, errors


def inspect_native_references(text: str) -> list[str]:
    root = parse_storage(text)
    active = []

    def visit(node):
        if node.tag == AC + 'structured-macro' and node.get(AC + 'name') in {'code', 'noformat'}:
            return
        active.append(node)
        for child in node:
            visit(child)

    visit(root)
    targets = {''.join(p.itertext()).strip()
               for node in active if node.tag == AC + 'structured-macro' and node.get(AC + 'name') == 'anchor'
               for p in node.findall(AC + 'parameter') if p.get(AC + 'name') == ''}
    errors = []
    for node in active:
        if node.tag not in {'a', AC + 'link'} or not ID_PATTERN.search(''.join(node.itertext())):
            continue
        if node.tag == 'a' and 'href' in node.attrib:
            errors.append('numbered references must use native ac:link, not HTML href')
        elif node.tag == AC + 'link' and node.get(AC + 'anchor') not in targets:
            errors.append('numbered reference must target a native anchor macro: ' + node.get(AC + 'anchor', ''))
    return errors


def inspect_toc(text: str, layout: str = 'floating') -> list[str]:
    root = parse_storage(text)
    parents = {child: parent for parent in root.iter() for child in parent}

    def ancestors(node):
        while node in parents:
            node = parents[node]
            yield node

    def macro(node, name):
        return node.tag == AC + 'structured-macro' and node.get(AC + 'name') == name

    tocs = [node for node in root.iter() if macro(node, 'toc') and
            not any(macro(a, 'code') or macro(a, 'noformat') for a in ancestors(node))]
    if len(tocs) != 1:
        return ['Storage must contain exactly one native toc macro']
    toc = tocs[0]
    errors = []
    if '{{FRONT_MATTER_STORAGE}}' in text or '{{BODY_STORAGE}}' in text:
        errors.append('unreplaced Storage layout placeholders')
    params = {p.get(AC + 'name'): ''.join(p.itertext()).strip()
              for p in toc.findall(AC + 'parameter')}
    try:
        low, high = int(params.get('minLevel', '')), int(params.get('maxLevel', ''))
        if not 1 <= low <= high <= 6:
            raise ValueError()
        if not any(re.fullmatch(r'h[1-6]', n.tag) and low <= int(n.tag[1]) <= high
                   for n in root.iter()):
            errors.append('toc heading range contains no document headings')
    except ValueError:
        errors.append('toc needs an explicit valid minLevel/maxLevel')
    # With a visible TOC heading, avoid including the directory in itself.
    if any(re.fullmatch(r'h[1-6]', n.tag) and ''.join(n.itertext()).strip() == '目录'
           for n in root.iter()) and params.get('exclude') != '^目录$':
        errors.append('toc must exclude its own 目录 heading')
    if layout == 'floating':
        expand = next((a for a in ancestors(toc) if macro(a, 'expand')), None)
        expand_body = expand.find(AC + 'rich-text-body') if expand is not None else None
        if expand_body is None or toc not in expand_body.iter():
            errors.append('toc must be inside expand rich-text-body')
        containers = [a for a in ancestors(expand) if a.tag == 'div' and
                      'zwFloatingTocRight' in a.get('class', '').split()] if expand is not None else []
        if len(containers) != 1:
            errors.append('floating class must wrap the entire expand/toc group exactly once')
            return errors
        container = containers[0]
        # The site class supplies position: fixed. The native right cell supplies
        # its static position; inline coordinates do not survive visual editing.
        if re.search(r'(?:^|;)\s*(?:position|top|right|left|bottom|inset(?:-[\w-]+)?)\s*:',
                     container.get('style', ''), re.I):
            errors.append('floating container must not depend on inline positioning')
        styles = {}
        for declaration in container.get('style', '').split(';'):
            if ':' not in declaration:
                continue
            name, value = declaration.split(':', 1)
            styles[name.strip().casefold()] = value.strip().casefold()
        bg = styles.get('background-color', '').replace(' ', '')
        if bg not in {'#ffffff', '#fff', 'rgb(255,255,255)', 'white'}:
            errors.append('floating container must keep opaque background-color: #ffffff')
        if styles.get('z-index') != '1000':
            errors.append('floating container must keep z-index: 1000')
        cell = next((a for a in ancestors(container) if a.tag == AC + 'layout-cell'), None)
        section = parents.get(cell)
        native_layout = parents.get(section)
        if (section is None or section.tag != AC + 'layout-section' or
                section.get(AC + 'type') != 'two_right_sidebar' or
                native_layout is None or native_layout.tag != AC + 'layout'):
            errors.append('floating group must be in a native two_right_sidebar layout')
            return errors
        cells = section.findall(AC + 'layout-cell')
        if len(cells) != 2 or cell is not cells[1]:
            errors.append('floating group must occupy the right cell, not the left cell')
        sections = native_layout.findall(AC + 'layout-section')
        if not sections or sections[0] is not section:
            errors.append('floating directory layout must be at the document top')
        following = sections[sections.index(section) + 1:]
        if (not following or any(s.get(AC + 'type') != 'single' or
                                 len(s.findall(AC + 'layout-cell')) != 1 for s in following)):
            errors.append('main body must use subsequent single full-width sections')
        elif not any(re.fullmatch(r'h[1-6]', n.tag) for s in following for n in s.iter()):
            errors.append('subsequent full-width body must contain the document chapters')
    return errors


def validate(storage: Path, workspace: Path, markdown: Path | None = None, *,
             output_dir: Path | None = None, remote_only: bool = False,
             layout: str = 'floating', image_policy: str = 'local',
             reference_policy: str = 'linked', source: Path | None = None) -> dict:
    result = {'storage': str(storage), 'markdown': str(markdown) if markdown else None,
              'errors': [], 'warnings': [], 'rendered': 'unverified',
              'scope': 'Static delivery checks only; verify content parity, authorized diff and rendered behavior separately.'}
    errors = result['errors']
    result['reference_policy'] = reference_policy
    if reference_policy == 'location':
        result['warnings'].append('Location fallback enabled: verify reader limitation; clickable navigation is not certified.')
    md_text = None
    if remote_only and markdown is not None:
        errors.append('remote-only conflicts with a supplied Markdown delivery')
    elif not remote_only:
        if markdown is None:
            errors.append('local Markdown delivery is required before publication')
        else:
            expected = (output_dir or workspace).resolve()
            actual = markdown.resolve()
            # Default is a visible file directly in the workspace root. An explicit
            # user-selected folder is allowed, but hidden internal artifacts are not.
            if actual.parent != expected or markdown.absolute().parent != (output_dir or workspace).absolute():
                errors.append('Markdown must be directly in workspace root or the explicit output directory')
            if any(part.startswith('.') for part in actual.parts) or any(part.startswith('.') for part in markdown.absolute().parts):
                errors.append('hidden artifact paths are not local Markdown delivery')
            if actual.suffix.lower() != '.md':
                errors.append('local delivery must be a .md file')
            checked = validate_prd(markdown, 'template', image_policy, source=source)
            if source is not None:
                result['markdown_image_comparison'] = checked.get('image_comparison')
            errors.extend('Markdown: ' + e for e in checked['errors'])
            result['warnings'].extend('Markdown: ' + w for w in checked['warnings'])
            try:
                md_text = markdown.read_text(encoding='utf-8-sig')
                errors.extend('Markdown: ' + e for e in inspect(md_text, reference_policy=reference_policy))
            except (OSError, UnicodeError) as exc:
                errors.append(f'cannot read Markdown: {exc}')
    try:
        body = storage.read_text(encoding='utf-8-sig')
        if not body.strip():
            errors.append('empty Storage body')
        if source is not None:
            result['storage_image_comparison'] = compare_source_images(source, body, errors, result['warnings'])
        if md_text is not None:
            result['format_image_comparison'] = compare_image_counts(
                image_reference_count(md_text), image_reference_count(body), errors, result['warnings'])
            result['mermaid_delivery'], mermaid_errors = inspect_mermaid_delivery(
                md_text, body, workspace.resolve())
            errors.extend(mermaid_errors)
        local_images, local_img_errors = inspect_local_image_delivery(
            md_text, body, image_policy=image_policy)
        errors.extend(local_img_errors)
        if md_text is not None:
            mermaid_assets = result.get('mermaid_delivery', {}).get('expected_assets', [])
            result['required_attachments'] = sorted(set(local_images) | set(mermaid_assets))
        errors.extend('Storage: ' + e for e in inspect(body, 'storage', reference_policy))
        errors.extend(inspect_native_references(body))
        if layout == 'floating':
            for node in parse_storage(body).iter(AC + 'structured-macro'):
                if node.get(AC + 'name') in {'code', 'noformat'}:
                    errors.append('floating directory layout cannot contain code/noformat macros')
        errors.extend(inspect_toc(body, layout))
        normalized = storage_markdown(body)
        storage_ids = set(definitions_in('\n'.join(active_lines(normalized))))
        for prefix in ('FR-', 'BR-', 'AC-'):
            if not any(item.startswith(prefix) for item in storage_ids):
                errors.append(f'Storage has no {prefix} definition')
        if md_text is not None and set(definitions_in('\n'.join(active_lines(md_text)))) != storage_ids:
            errors.append('Markdown and Storage current definition IDs differ; check missing or stale content')
    except (OSError, UnicodeError, ValueError, ET.ParseError) as exc:
        errors.append(f'cannot inspect Storage: {exc}')
    result['passed'] = not errors
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('storage', type=Path)
    parser.add_argument('--workspace', required=True, type=Path)
    parser.add_argument('--markdown', type=Path)
    parser.add_argument('--source', type=Path, help='original Markdown/HTML/Storage snapshot for image-retention checks')
    parser.add_argument('--output-dir', type=Path, help='Only for a user-selected output folder')
    parser.add_argument('--remote-only', action='store_true', help='Only when user explicitly requests no local output')
    parser.add_argument('--layout', choices=('floating', 'inline'), default='floating', help='inline only for an explicit user choice')
    parser.add_argument('--image-policy', choices=('local', 'external'), default='local')
    parser.add_argument('--reference-policy', choices=('linked', 'location'), default='linked',
                        help='location only when actual navigation is unavailable')
    args = parser.parse_args()
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    result = validate(**vars(args))
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result['passed'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
