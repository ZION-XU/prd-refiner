#!/usr/bin/env python3
"""Build a verified local snapshot from page content and downloaded images.

The caller obtains the page body, complete attachment metadata and referenced
image files through the available host tools. This script does not access
Confluence or credentials; it packages downloaded inputs into
an immutable local baseline and fails if any referenced image is missing,
invalid or unsafe. The requirement workspace must be passed explicitly.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import sys
import tempfile
from urllib.parse import unquote, urlsplit


IMAGE_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp', '.bmp'}
IMAGE_PATTERN = re.compile(
    r'!\[([^\]\n]*)\]\(\s*(<[^>\n]+>|[^\s)]+)(?:\s+["\'][^\n]*?["\'])?\s*\)'
)
HTML_IMG_PATTERN = re.compile(
    r'<img\s+[^>]*?src=["\']([^"\']+)["\'][^>]*?>', re.IGNORECASE
)
AC_IMAGE_BLOCK_PATTERN = re.compile(
    r'<ac:image\b[^>]*>[\s\S]*?</ac:image>', re.IGNORECASE,
)
RI_ATTACHMENT_PATTERN = re.compile(
    r'<ri:attachment\b[^>]*\bri:filename=["\']([^"\']+)["\']', re.IGNORECASE,
)
RI_URL_PATTERN = re.compile(
    r'<ri:url\b[^>]*\bri:value=["\']([^"\']+)["\']', re.IGNORECASE,
)
RI_PAGE_PATTERN = re.compile(
    r'<ri:page\b[^>]*\bri:content-title=["\']([^"\']+)["\']', re.IGNORECASE,
)


def without_fenced_code(text: str) -> str:
    lines = []
    marker = None
    for line in text.splitlines(keepends=True):
        fence = re.match(r'^\s{0,3}(`{3,}|~{3,})(.*)$', line.rstrip('\r\n'))
        if marker is None and fence:
            marker = fence.group(1)
            lines.append('\n' if line.endswith('\n') else '')
        elif (marker and fence and fence.group(1)[0] == marker[0] and
              len(fence.group(1)) >= len(marker) and not fence.group(2).strip()):
            marker = None
            lines.append('\n' if line.endswith('\n') else '')
        elif marker:
            lines.append('\n' if line.endswith('\n') else '')
        else:
            lines.append(line)
    return ''.join(lines)


def protect_ignored_blocks(text: str) -> tuple[str, list[tuple[str, str]]]:
    """Hide comments and fenced examples while rewriting active image references."""
    protected: list[tuple[str, str]] = []

    def hide(value: str) -> str:
        token = f'\x00PRD_REFINER_IGNORED_{len(protected)}\x00'
        protected.append((token, value))
        return token

    text = re.sub(r'<!--[\s\S]*?-->', lambda match: hide(match.group(0)), text)
    output = []
    buffered = []
    marker = None
    for line in text.splitlines(keepends=True):
        fence = re.match(r'^\s{0,3}(`{3,}|~{3,})(.*)$', line.rstrip('\r\n'))
        if marker is None and fence:
            marker = fence.group(1)
            buffered = [line]
        elif marker:
            buffered.append(line)
            if (fence and fence.group(1)[0] == marker[0] and
                    len(fence.group(1)) >= len(marker) and not fence.group(2).strip()):
                output.append(hide(''.join(buffered)))
                buffered = []
                marker = None
        else:
            output.append(line)
    if buffered:
        output.append(hide(''.join(buffered)))
    return ''.join(output), protected


def restore_ignored_blocks(text: str, protected: list[tuple[str, str]]) -> str:
    for token, value in protected:
        text = text.replace(token, value)
    return text


def extract_filename_from_target(target: str) -> str:
    """Return a safe image basename from a URL, path or attachment name."""
    target = target.strip().strip('<>')
    if not target or target.casefold().startswith('data:'):
        return ''
    decoded = unquote(urlsplit(target).path or target.split('?', 1)[0].split('#', 1)[0])
    normalized = decoded.replace('\\', '/')
    if '..' in normalized.split('/'):
        return ''
    filename = normalized.rsplit('/', 1)[-1].strip()
    if (not filename or filename in {'.', '..'} or
            re.search(r'[<>:"/\\|?*\x00-\x1f]', filename) or
            Path(filename).suffix.casefold() not in IMAGE_EXTENSIONS):
        return ''
    return filename


def image_macro_target(block: str, current_page_id: str | None = None) -> tuple[str, str, str] | None:
    """Return target, kind and source identity for a Confluence image macro."""
    attachment = RI_ATTACHMENT_PATTERN.search(block)
    url = RI_URL_PATTERN.search(block)
    if bool(attachment) == bool(url):
        return None
    if attachment:
        page = RI_PAGE_PATTERN.search(block)
        origin = page.group(1) if page else (current_page_id if current_page_id else '<current-page>')
        return attachment.group(1), 'confluence-attachment', f'attachment:{origin}/{attachment.group(1)}'
    target = url.group(1)
    parsed = urlsplit(target)
    m = re.search(r'/download/attachments/([^/]+)/([^/?#]+)', parsed.path)
    if m:
        page_id = m.group(1)
        if current_page_id and (page_id == current_page_id or page_id == '<current-page>'):
            page_id = current_page_id
        return target, 'confluence-url', f'attachment:{page_id}/{unquote(m.group(2))}'
    return target, 'confluence-url', f'url:{parsed.netloc}{unquote(parsed.path)}?{parsed.query}'


def extract_referenced_items(text: str, current_page_id: str | None = None) -> list[dict]:
    """Return referenced images with source identities, grouped by local name."""
    active = without_fenced_code(re.sub(r'<!--[\s\S]*?-->', '', text))
    found: dict[str, dict] = {}

    def add(target: str, kind: str, identity: str | None = None) -> None:
        filename = extract_filename_from_target(target)
        if not filename:
            return
        if identity is None:
            parsed = urlsplit(target)
            m = re.search(r'/download/attachments/([^/]+)/([^/?#]+)', parsed.path)
            if m:
                page_id = m.group(1)
                if current_page_id and (page_id == current_page_id or page_id == '<current-page>'):
                    page_id = current_page_id
                identity = f'attachment:{page_id}/{unquote(m.group(2))}'
            else:
                identity = f'url:{parsed.netloc}{unquote(parsed.path)}?{parsed.query}'
        item = found.setdefault(filename, {'filename': filename, 'targets': [], 'kinds': [], 'sources': []})
        if target not in item['targets']:
            item['targets'].append(target)
        if kind not in item['kinds']:
            item['kinds'].append(kind)
        if identity not in item['sources']:
            item['sources'].append(identity)

    for match in IMAGE_PATTERN.finditer(active):
        add(match.group(2).strip('<>'), 'markdown')
    for match in HTML_IMG_PATTERN.finditer(active):
        add(match.group(1), 'html')
    for match in AC_IMAGE_BLOCK_PATTERN.finditer(active):
        parsed = image_macro_target(match.group(0), current_page_id)
        if parsed:
            add(*parsed)
    return list(found.values())


def invalid_referenced_targets(text: str) -> list[dict]:
    """Return image references that cannot be mapped to a safe local filename."""
    active = without_fenced_code(re.sub(r'<!--[\s\S]*?-->', '', text))
    candidates = (
        [(m.group(2).strip('<>'), 'markdown') for m in IMAGE_PATTERN.finditer(active)] +
        [(m.group(1), 'html') for m in HTML_IMG_PATTERN.finditer(active)]
    )
    invalid = [
        {'target': target, 'kind': kind}
        for target, kind in candidates
        if not extract_filename_from_target(target)
    ]
    for match in AC_IMAGE_BLOCK_PATTERN.finditer(active):
        parsed = image_macro_target(match.group(0))
        if parsed is None or not extract_filename_from_target(parsed[0]):
            invalid.append({'target': match.group(0), 'kind': 'confluence-image'})
    if len(re.findall(r'<ac:image\b', active, re.IGNORECASE)) != len(AC_IMAGE_BLOCK_PATTERN.findall(active)):
        invalid.append({'target': '<ac:image>', 'kind': 'incomplete-confluence-image'})
    return invalid


def extract_referenced_filenames(text: str) -> list[str]:
    return [item['filename'] for item in extract_referenced_items(text)]


def rewrite_image_paths_to_local(text: str, relative_dir: str = './images',
                                 available: set[str] | None = None) -> tuple[str, int]:
    """Rewrite verified image targets to local relative paths."""
    count = 0
    prefix = relative_dir.rstrip('/\\').replace('\\', '/') + '/'
    text, protected = protect_ignored_blocks(text)

    def allowed(filename: str) -> bool:
        return bool(filename) and (available is None or filename in available)

    def replace_markdown(match):
        nonlocal count
        filename = extract_filename_from_target(match.group(2))
        if not allowed(filename):
            return match.group(0)
        count += 1
        return f'![{match.group(1)}]({prefix}{filename})'

    rewritten = IMAGE_PATTERN.sub(replace_markdown, text)

    def replace_html(match):
        nonlocal count
        filename = extract_filename_from_target(match.group(1))
        if not allowed(filename):
            return match.group(0)
        count += 1
        return re.sub(r'src=["\'][^"\']+["\']', f'src="{prefix}{filename}"',
                      match.group(0), count=1, flags=re.IGNORECASE)

    rewritten = HTML_IMG_PATTERN.sub(replace_html, rewritten)

    def replace_confluence_image(match):
        nonlocal count
        parsed = image_macro_target(match.group(0))
        filename = extract_filename_from_target(parsed[0]) if parsed else ''
        if not allowed(filename):
            return match.group(0)
        count += 1
        return f'![{filename}]({prefix}{filename})'

    rewritten = AC_IMAGE_BLOCK_PATTERN.sub(replace_confluence_image, rewritten)
    return restore_ignored_blocks(rewritten, protected), count


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open('rb') as source:
        for block in iter(lambda: source.read(1024 * 1024), b''):
            digest.update(block)
    return digest.hexdigest()


def valid_image(path: Path) -> bool:
    """Reject empty files, login pages and obvious extension/content mismatches."""
    try:
        data = path.read_bytes()
    except OSError:
        return False
    if not data or b'<html' in data[:1024].lower() or b'<!doctype html' in data[:1024].lower():
        return False
    suffix = path.suffix.casefold()
    if suffix == '.png':
        return len(data) > 24 and data.startswith(b'\x89PNG\r\n\x1a\n') and data[12:16] == b'IHDR'
    if suffix in {'.jpg', '.jpeg'}:
        return len(data) > 4 and data.startswith(b'\xff\xd8\xff') and data.endswith(b'\xff\xd9')
    if suffix == '.gif':
        return len(data) > 12 and data[:6] in {b'GIF87a', b'GIF89a'}
    if suffix == '.bmp':
        return len(data) > 14 and data.startswith(b'BM')
    if suffix == '.webp':
        return len(data) > 16 and data.startswith(b'RIFF') and data[8:12] == b'WEBP'
    if suffix == '.svg':
        head = data[:4096].lstrip(b'\xef\xbb\xbf\x00\t\r\n ')
        return b'<svg' in head.lower()
    return False


def create_snapshot_from_data(content: str, attachments: list[dict], workspace_dir: Path,
                              cached_files: dict[str, Path] | None = None, *,
                              source_metadata: dict | None = None) -> dict:
    """Create an immutable verified snapshot flat in `.assets`; passed=False on any gap.

    `.assets/manifest.json` is the completion marker and is written last, so an
    interrupted run never leaves a snapshot that looks complete.
    """
    workspace = Path(workspace_dir).resolve()
    assets_root = workspace / '.assets'
    target = assets_root
    marker = target / 'manifest.json'
    if marker.exists():
        return {'passed': False, 'errors': [f'snapshot already exists: {marker}'],
                'snapshot_dir': str(target), 'missing_images': [], 'invalid_images': []}

    metadata = source_metadata or {}
    metadata_errors = []
    if not content.strip():
        metadata_errors.append('source body is empty')
    if not metadata.get('page_id'):
        metadata_errors.append('source page_id is required')
    if metadata.get('version') in {None, ''}:
        metadata_errors.append('source page version is required')
    unsafe = invalid_referenced_targets(content)
    if metadata_errors or unsafe:
        return {
            'passed': False,
            'errors': metadata_errors + (['source contains unsafe image references'] if unsafe else []),
            'snapshot_dir': str(target),
            'missing_images': [],
            'invalid_images': [],
            'unsafe_images': unsafe,
        }

    references = extract_referenced_items(content, current_page_id=metadata.get('page_id'))
    collisions = [item for item in references if len(item['sources']) > 1]
    if collisions:
        return {'passed': False, 'errors': ['different image sources share a local filename'],
                'snapshot_dir': str(target), 'ambiguous_images': collisions,
                'missing_images': [], 'invalid_images': []}
    cached = {key: Path(value) for key, value in (cached_files or {}).items()}
    attachment_by_name = {item.get('title', ''): item for item in attachments if item.get('title')}
    missing, invalid, sources = [], [], {}
    for item in references:
        filename = item['filename']
        source = cached.get(filename)
        if source is None or not source.is_file():
            attachment = attachment_by_name.get(filename, {})
            missing.append({'filename': filename, 'attachment_id': attachment.get('id'),
                            'download_url': attachment.get('download_url')})
            continue
        if not valid_image(source):
            invalid.append({'filename': filename, 'source_path': str(source)})
            continue
        sources[filename] = source

    if missing or invalid:
        return {'passed': False, 'errors': ['snapshot images are incomplete or invalid'],
                'snapshot_dir': str(target), 'referenced_images': [x['filename'] for x in references],
                'missing_images': missing, 'invalid_images': invalid}

    assets_root.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='.snapshot-', dir=assets_root) as temp_name:
        temp = Path(temp_name)
        images_dir = temp / 'images'
        image_records = []
        if sources:
            images_dir.mkdir()
        for item in references:
            filename = item['filename']
            destination = (images_dir / filename).resolve()
            destination.relative_to(images_dir.resolve())
            shutil.copy2(sources[filename], destination)
            attachment = attachment_by_name.get(filename, {})
            image_records.append({
                **item,
                'attachment_id': attachment.get('id'),
                'download_url': attachment.get('download_url'),
                'local_path': f'images/{filename}',
                'size': destination.stat().st_size,
                'sha256': file_sha256(destination),
            })

        rewritten, rewrite_count = rewrite_image_paths_to_local(
            content, './images', set(sources))
        original = temp / 'source.original.txt'
        local = temp / 'source.md'
        original.write_text(content, encoding='utf-8')
        local.write_text(rewritten, encoding='utf-8')
        manifest = {
            'status': 'complete',
            'source': metadata,
            'source_sha256': file_sha256(original),
            'local_source': 'source.md',
            'original_source': 'source.original.txt',
            'images': image_records,
        }
        (temp / 'manifest.json').write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
        if images_dir.exists():
            images_target = assets_root / 'images'
            images_target.mkdir(exist_ok=True)
            for rendered in images_dir.iterdir():
                rendered.replace(images_target / rendered.name)
        (temp / 'source.original.txt').replace(assets_root / 'source.original.txt')
        (temp / 'source.md').replace(assets_root / 'source.md')
        # Completion marker last: its presence means the snapshot is complete.
        (temp / 'manifest.json').replace(assets_root / 'manifest.json')

    return {
        'passed': True,
        'errors': [],
        'snapshot_dir': str(target),
        'snapshot_file': str(target / 'source.md'),
        'manifest_file': str(target / 'manifest.json'),
        'referenced_images': [x['filename'] for x in references],
        'saved_images': [x['local_path'] for x in image_records],
        'missing_images': [],
        'invalid_images': [],
        'rewritten_count': rewrite_count,
    }


def content_and_attachments(data: dict) -> tuple[str, list[dict]]:
    metadata = data.get('metadata', data)
    content = metadata.get('content', {})
    if isinstance(content, dict):
        content = content.get('value', '')
    if not content:
        body = metadata.get('body', {})
        if isinstance(body, dict):
            storage = body.get('storage', body)
            content = storage.get('value', '') if isinstance(storage, dict) else ''
    return content if isinstance(content, str) else '', metadata.get('attachments', [])


def cached_files_from(directory: Path | None) -> tuple[dict[str, Path], list[str]]:
    if directory is None:
        return {}, []
    found, errors = {}, []
    for path in directory.rglob('*'):
        if not path.is_file() or path.suffix.casefold() not in IMAGE_EXTENSIONS:
            continue
        if path.name in found:
            errors.append(f'duplicate downloaded image filename: {path.name}')
        else:
            found[path.name] = path
    return found, errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument('--json-file', type=Path, help='Saved page JSON containing content and attachments')
    source.add_argument('--source-file', type=Path, help='Saved page body')
    parser.add_argument('--asset-dir', type=Path, help='Directory containing downloaded referenced images')
    parser.add_argument('--workspace', required=True, type=Path,
                        help='Requirement workspace root (absolute path); snapshot lands in <workspace>/.assets')
    parser.add_argument('--page-id', required=True)
    parser.add_argument('--page-version', required=True)
    parser.add_argument('--page-url')
    args = parser.parse_args(argv)

    try:
        if args.json_file:
            content, attachments = content_and_attachments(
                json.loads(args.json_file.read_text(encoding='utf-8-sig')))
        else:
            content = args.source_file.read_text(encoding='utf-8-sig')
            attachments = []
        cached, cache_errors = cached_files_from(args.asset_dir)
        if cache_errors:
            result = {'passed': False, 'errors': cache_errors}
        else:
            result = create_snapshot_from_data(
                content, attachments, args.workspace, cached,
                source_metadata={'page_id': args.page_id, 'version': args.page_version,
                                 'url': args.page_url})
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as exc:
        result = {'passed': False, 'errors': [f'{type(exc).__name__}: {exc}']}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result.get('passed') else 1


if __name__ == '__main__':
    raise SystemExit(main())
