#!/usr/bin/env python3
"""Read-only, bounded structural checks for PRD working documents.

Profiles do not certify semantic correctness, completion or review status.
Only the supplied document and referenced local images are inspected.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


CORE_HEADINGS = (
    ('## 1. 背景、用户与目标',),
    ('## 2. 范围与边界',),
    ('## 3. 功能与交互规格',),
    ('## 4. 业务规则与异常处理',),
    ('## 5. 验收标准',),
    ('## 8. 风险与开放问题',),
    ('## 9. 来源与参考资料',),
)
ID_EXPR = r'(?:FR|BR|AC|DEC|NFR|RK|DEP|SRC|VAR)-\d{3}'
ID_PATTERN = re.compile(r'\b' + ID_EXPR + r'\b')
PLACEHOLDER_PATTERN = re.compile(
    r'\{(?:REQ-ID|YYYY-MM-DD|需求名称|需求负责人|文档版本|功能名称|填写|待填写|'
    r'草稿/|待补充工作稿/)[^{}\n]*\}|<(?:填写|待填写)[^>\n]*>'
)
TEMPLATE_TAG_PATTERN = re.compile(r'【(?:核心|按需|多功能时填写)[^】\n]*】')
HEADING_DEF = re.compile(r'^#{2,6}\s+(?:\d+(?:\.\d+)*\.?\s+)?(' + ID_EXPR + r')\b')
LIST_DEF = re.compile(r'^\s*(?:[-*]|\d+\.)\s+(' + ID_EXPR + r')(?=\s|[:：]|$)')
TABLE_DEF = re.compile(r'^\|\s*(?:(?:\d+|[-*#])\s*\|\s*)?(' + ID_EXPR + r')(?=\s|[:：]|\|)')
INLINE_IMAGE = re.compile(r'!\[[^\]\n]*\]\(\s*(<[^>\n]+>|[^\s)]+)(?:\s+["\'][^\n]*?["\'])?\s*\)')
REFERENCE_IMAGE = re.compile(r'!\[([^\]\n]*)\]\[([^\]\n]*)\]')
REFERENCE_LINK = re.compile(r'^\s*\[([^\]]+)\]:\s*(<[^>\n]+>|\S+)', re.MULTILINE)


def without_fenced_code(text: str) -> str:
    """Keep line positions while excluding code examples from prose checks."""
    result = []
    marker = None
    for line in text.splitlines():
        fence = re.match(r'^\s{0,3}(`{3,}|~{3,})(.*)$', line)
        if marker is None and fence:
            marker = fence.group(1)
            result.append('')
        elif marker and fence and fence.group(1)[0] == marker[0] and len(fence.group(1)) >= len(marker) and not fence.group(2).strip():
            marker = None
            result.append('')
        elif marker:
            result.append('')
        else:
            result.append(line)
    return '\n'.join(result)


def body_without_metadata(text: str) -> str:
    return re.sub(r'\A---\s*\n.*?\n---\s*(?:\n|$)', '', text, count=1, flags=re.DOTALL)


def definitions_in(text: str) -> list[str]:
    # Revision records describe older versions; they do not define current rules.
    text = without_record_sections(text, include_sources=False)
    # Markdown inline emphasis/code around IDs is only formatting.
    lines = [line.replace('**', '').replace('`', '') for line in text.splitlines()]
    heading_ids = [m.group(1) for line in lines if (m := HEADING_DEF.match(line))]
    definitions = list(heading_ids)
    section = ''
    for line in lines:
        heading = re.match(r'^##\s+(?:\d+\.\s*)?(.+)$', line)
        if heading:
            section = heading.group(1).split('【', 1)[0].strip()
        match = LIST_DEF.match(line)
        if match:
            item = match.group(1)
            # These template sections list references, not new definitions.
            reference_prefixes = {
                '范围与边界': ('FR-',),
                '功能与交互规格': ('BR-', 'NFR-'),
                '核对与版本记录': ('DEC-',),
            }.get(section, ())
            if not item.startswith(reference_prefixes):
                definitions.append(item)
        match = TABLE_DEF.match(line)
        if match:
            item = match.group(1)
            # A functional heading is authoritative; its FR table row is an index.
            if not (item.startswith('FR-') and item in heading_ids):
                definitions.append(item)
    return definitions


def known_placeholders(text: str) -> list[str]:
    found = set(PLACEHOLDER_PATTERN.findall(text))
    template_path = Path(__file__).resolve().parents[1] / 'assets/prd-template.md'
    try:
        template = template_path.read_text(encoding='utf-8-sig')
    except (OSError, UnicodeError):
        template = ''
    # Match actual template tokens rather than rejecting arbitrary JSON or inequalities.
    for token in re.findall(r'\{[^{}\n]+\}', template):
        if token in text:
            found.add(token)
    return sorted(found)


def template_markers_in(text: str) -> list[str]:
    return sorted(set(TEMPLATE_TAG_PATTERN.findall(text)))


def without_record_sections(text: str, *, include_sources: bool = True) -> str:
    """Exclude headed records and the company's unheaded front revision table."""
    lines = []
    skip_level = None
    in_front_revision_table = False
    for line in text.splitlines():
        stripped = line.replace('**', '').replace('`', '').strip()
        heading = re.match(r'^(#{1,6})\s+(.+)$', stripped)
        if heading:
            level = len(heading.group(1))
            if skip_level is not None and level <= skip_level:
                skip_level = None
            in_front_revision_table = False
            title = re.sub(r'^\d+(?:\.\d+)*\.?\s*', '', heading.group(2)).rstrip('：:')
            if skip_level is None and (title == '版本修订记录' or
                                       (include_sources and title == '来源与参考资料')):
                skip_level = level
        if skip_level is not None:
            continue
        if stripped.rstrip('：:') == '版本修订记录':
            in_front_revision_table = True
            continue
        if in_front_revision_table:
            if not stripped or stripped.startswith('|'):
                continue
            in_front_revision_table = False
        lines.append(line)
    return '\n'.join(lines)


def filter_historical_and_source_references(text: str) -> str:
    """Exclude record sections and explicit historical prefixes from ID checks."""
    filtered = without_record_sections(text)
    # Exclude historical ID patterns like "原 BR-002", "旧编号 BR-001", "废弃 FR-001", "历史 DEC-001"
    filtered = re.sub(r'(?:原|旧|废弃|历史|参考外部)(?:规则|功能|需求|决策|编号)?[:：\s]*' + ID_EXPR, '', filtered)
    return filtered


class HTMLImages(HTMLParser):
    """Collect static img sources without fetching or interpreting page scripts."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.targets = []
        self.has_srcset = False

    def handle_starttag(self, tag, attrs):
        if tag.casefold() == 'img':
            values = dict(attrs)
            self.targets.append(values.get('src') or '')
            self.has_srcset |= 'srcset' in values


def check_images(text: str, parent: Path, errors: list[str], warnings: list[str],
                 *, image_policy: str, profile: str) -> None:
    refs = {m.group(1).strip().casefold(): m.group(2) for m in REFERENCE_LINK.finditer(text)}
    targets = [m.group(1) for m in INLINE_IMAGE.finditer(text)]
    html_images = HTMLImages()
    html_images.feed(text)
    targets.extend(html_images.targets)
    # A draft can retain an explicit resource gap; a complete local output cannot.
    localization_findings = errors if profile == 'template' else warnings
    if html_images.has_srcset:
        findings = localization_findings if image_policy == 'local' else warnings
        findings.append('HTML image srcset requires manual verification; use a single local src for portable output')
    for match in REFERENCE_IMAGE.finditer(text):
        label = (match.group(2) or match.group(1)).strip().casefold()
        if label not in refs:
            errors.append(f'undefined image reference: {label}')
        else:
            targets.append(refs[label])
    for target in sorted(set(targets)):
        target = target.strip('<>')
        if target.startswith('//') or re.match(r'^(?:https?|data):', target, re.IGNORECASE):
            if image_policy == 'local':
                localization_findings.append('remote/embedded image must be saved locally and referenced with a relative path')
            else:
                warnings.append('remote/embedded image not verified; availability depends on external access')
            continue
        if re.match(r'^/?[A-Za-z]:[/\\]', target):
            file_path = unquote(target.lstrip('/') if target.startswith('/') else target)
        elif re.match(r'^[A-Za-z][A-Za-z0-9+.-]*:', target):
            findings = localization_findings if image_policy == 'local' else warnings
            findings.append('unsupported image URI scheme; save a local file or verify the explicit external-image choice')
            continue
        else:
            file_path = unquote(urlsplit(target).path)
        if not file_path:
            errors.append('empty local image target')
            continue
        path = Path(file_path)
        if image_policy == 'local':
            if path.is_absolute() or re.match(r'^/?[A-Za-z]:[/\\]', target):
                localization_findings.append('absolute image path is not portable; use a path relative to the document')
            else:
                try:
                    (parent / path).resolve().relative_to(parent.resolve())
                except (ValueError, OSError, RuntimeError):
                    localization_findings.append('image path leaves the document directory; copy the asset into its resource directory')
        if not path.is_absolute():
            path = parent / path
        try:
            exists = path.is_file()
        except OSError:
            exists = False
        if not exists:
            errors.append(f'local image not found: {file_path}')
        else:
            try:
                if path.stat().st_size == 0:
                    errors.append(f'empty local image file: {file_path}')
            except OSError:
                errors.append(f'local image could not be inspected: {file_path}')


def validate(target: Path, profile: str = 'template', image_policy: str | None = None) -> dict:
    if profile not in {'template', 'draft', 'existing'}:
        raise ValueError(f'unknown profile: {profile}')
    if image_policy is None:
        image_policy = 'external' if profile == 'existing' else 'local'
    if image_policy not in {'local', 'external'}:
        raise ValueError(f'unknown image policy: {image_policy}')
    prd = target / 'prd.md' if target.is_dir() else target
    result = {
        'document': str(prd), 'profile': profile, 'image_policy': image_policy,
        'errors': [], 'warnings': [],
        'scope': 'Structure only; not semantic correctness, draft readiness or formal review.',
    }
    errors, warnings = result['errors'], result['warnings']
    if profile == 'existing':
        warnings.append('Input-only diagnostic: PRD template structure is not checked; use template or draft for generated or optimized output.')
    try:
        text = prd.read_text(encoding='utf-8-sig')
    except (OSError, UnicodeError) as exc:
        errors.append(f'cannot read PRD: {type(exc).__name__}: {prd}')
        result['passed'] = False
        return result
    if not text.strip():
        errors.append('empty PRD document')
    prose = without_fenced_code(text)
    body = body_without_metadata(prose)
    lines = [line.strip() for line in body.splitlines()]
    if profile != 'existing':
        findings = errors if profile == 'template' else warnings
        for alternatives in CORE_HEADINGS:
            if not any(line.startswith(h) for line in lines for h in alternatives):
                findings.append(f'missing template section: {alternatives[0]}')
    tokens = known_placeholders(prose)
    if tokens:
        errors.append('unresolved template placeholders: ' + ', '.join(tokens[:5]))
    markers = template_markers_in(prose)
    if markers:
        errors.append('unresolved template markers: ' + ', '.join(markers[:5]))

    definitions = definitions_in(body)
    for item, count in Counter(definitions).items():
        if count > 1:
            errors.append(f'duplicate ID definition: {item}')
    defined = set(definitions)
    if profile != 'existing':
        findings = errors if profile == 'template' else warnings
        for prefix in ('FR-', 'BR-', 'AC-'):
            if not any(item.startswith(prefix) for item in defined):
                findings.append(f'no {prefix} definition; check known content and open issues')
    # Destinations and reference-link URLs are provenance, not business-ID references.
    references = re.sub(r'\]\([^\n]*?\)', ']', body)
    references = REFERENCE_LINK.sub('', references)
    references = filter_historical_and_source_references(references)
    undefined = sorted(set(ID_PATTERN.findall(references)) - defined)
    if undefined:
        errors.append('IDs referenced but not defined: ' + ', '.join(undefined))
    check_images(body, prd.parent, errors, warnings, image_policy=image_policy, profile=profile)
    result['passed'] = not errors
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('target', type=Path, help='PRD file, or directory containing prd.md')
    parser.add_argument('--profile', choices=('template', 'draft', 'existing'), default='template',
                        help='template: new/optimized output; draft: unfinished output; existing: input-only diagnostic')
    parser.add_argument('--json', action='store_true', help='emit machine-readable results')
    parser.add_argument('--image-policy', choices=('local', 'external'), default=None,
                        help='default: local for output, external for existing input; external output requires an explicit user choice')
    args = parser.parse_args(argv)
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    result = validate(args.target, args.profile, args.image_policy)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print('Structural checks passed.' if result['passed'] else 'Structural checks failed.')
        for label in ('errors', 'warnings'):
            for message in result[label]:
                print(f'{label}: {message}')
        print(result['scope'])
    return 0 if result['passed'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
