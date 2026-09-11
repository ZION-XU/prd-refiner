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
from pathlib import Path
from urllib.parse import unquote, urlsplit


CORE_HEADINGS = (
    ('## 1. 背景、用户与目标',),
    ('## 2. 范围与边界',),
    ('## 3. 功能与交互规格',),
    ('## 4. 业务规则与异常处理',),
    ('## 5. 验收标准',),
    ('## 8. 风险与开放问题',),
    ('## 9. 核对与版本记录',),
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


def filter_historical_and_source_references(text: str) -> str:
    """Exclude version revision history, sources section, and historical prefixes from undefined ID checks."""
    lines = []
    in_history_or_sources = False
    for line in text.splitlines():
        stripped = line.strip()
        # Detect Section 9.2 (版本修订记录) and 9.3 (来源与参考资料)
        if re.match(r'^#{2,3}\s+(?:9\.[23]|版本修订记录|来源与参考资料)\b', stripped):
            in_history_or_sources = True
        elif in_history_or_sources and re.match(r'^#{1,3}\s+', stripped):
            in_history_or_sources = False
        if not in_history_or_sources:
            lines.append(line)
    filtered = '\n'.join(lines)
    # Exclude historical ID patterns like "原 BR-002", "旧编号 BR-001", "废弃 FR-001", "历史 DEC-001"
    filtered = re.sub(r'(?:原|旧|废弃|历史|参考外部)(?:规则|功能|需求|决策|编号)?[:：\s]*' + ID_EXPR, '', filtered)
    return filtered


def check_images(text: str, parent: Path, errors: list[str], warnings: list[str]) -> None:
    refs = {m.group(1).strip().casefold(): m.group(2) for m in REFERENCE_LINK.finditer(text)}
    targets = [m.group(1) for m in INLINE_IMAGE.finditer(text)]
    for match in REFERENCE_IMAGE.finditer(text):
        label = (match.group(2) or match.group(1)).strip().casefold()
        if label not in refs:
            errors.append(f'undefined image reference: {label}')
        else:
            targets.append(refs[label])
    for target in sorted(set(targets)):
        target = target.strip('<>')
        if target.startswith('//') or re.match(r'^(?:https?|data):', target, re.IGNORECASE):
            warnings.append(f'remote/embedded image not verified: {target.split("?")[0][:160]}')
            continue
        if re.match(r'^/?[A-Za-z]:[/\\]', target):
            file_path = unquote(target.lstrip('/') if target.startswith('/') else target)
        elif re.match(r'^[A-Za-z][A-Za-z0-9+.-]*:', target):
            warnings.append('unsupported image URI scheme; verify manually')
            continue
        else:
            file_path = unquote(urlsplit(target).path)
        if not file_path:
            errors.append('empty local image target')
            continue
        path = Path(file_path)
        if not path.is_absolute():
            path = parent / path
        try:
            exists = path.is_file()
        except OSError:
            exists = False
        if not exists:
            errors.append(f'local image not found: {file_path}')


def validate(target: Path, profile: str = 'template') -> dict:
    if profile not in {'template', 'draft', 'existing'}:
        raise ValueError(f'unknown profile: {profile}')
    prd = target / 'prd.md' if target.is_dir() else target
    result = {
        'document': str(prd), 'profile': profile, 'errors': [], 'warnings': [],
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
    check_images(body, prd.parent, errors, warnings)
    result['passed'] = not errors
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('target', type=Path, help='PRD file, or directory containing prd.md')
    parser.add_argument('--profile', choices=('template', 'draft', 'existing'), default='template',
                        help='template: new/optimized output; draft: unfinished output; existing: input-only diagnostic')
    parser.add_argument('--json', action='store_true', help='emit machine-readable results')
    args = parser.parse_args(argv)
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    result = validate(args.target, args.profile)
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
