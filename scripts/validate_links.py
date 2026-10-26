#!/usr/bin/env python3
"""Read-only PRD reference checks; no network access or rendering certification.

Supports conventional Markdown and Confluence Storage anchor/link macros.
Storage is normalized for analysis; reported lines refer to that normalized text.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from html import escape, unescape
import json
from pathlib import Path
import re
import xml.etree.ElementTree as ET
from urllib.parse import unquote

from validate_prd import (ID_EXPR, ID_PATTERN, FRAME_ID, HEADING_DEF, NAMED_HEADING_DEF,
                          LIST_DEF, NAMED_LIST_DEF, TABLE_DEF, NAMED_TABLE_DEF,
                          without_fenced_code, body_without_metadata)

ANCHOR = re.compile(r'<a\s+(?:id|name)=["\']([^"\']+)["\']\s*>\s*</a>', re.I)
INLINE = re.compile(r'(?<!!)\[([^\]\n]+)\]\(\s*(<[^>\n]+>|(?:[^\s()]|\([^()]*\))+)(?:\s+["\'][^\n]*?["\'])?\s*\)')
REF_DEF = re.compile(r'^\s*\[([^\]]+)\]:\s*(<[^>\n]+>|\S+)\s*.*$')
REF_USE = re.compile(r'(?<!!)\[([^\]\n]+)\]\[([^\]\n]*)\]')
SHORT_REF = re.compile(r'(?<!!)\[([^\]\n]+)\]')
NAMED_LABEL = re.compile(r'^(.+?)[（(](' + ID_EXPR + r')[）)]$')
LOCATION_REF = re.compile(r'〔([^〔〕\n]+?)[；;]\s*位置[：:]\s*([^〔〕\n]+)〕')


def plain(text: str) -> str:
    text = re.sub(r'<[^>]*>', '', text)
    return unescape(text).replace('**', '').replace('`', '').strip()


def parse_storage(text: str) -> ET.Element:
    """Parse a Storage fragment without DTDs or external resources."""
    if re.search(r'<!DOCTYPE|<!ENTITY', text, re.I):
        raise ValueError('DTD and entity declarations are not supported')
    # Common HTML named entities are not predefined XML entities.
    text = re.sub(r'&([A-Za-z][A-Za-z0-9]+);',
                  lambda m: m.group(0) if m.group(1) in {'amp', 'lt', 'gt', 'quot', 'apos'}
                  else ''.join(f'&#{ord(c)};' for c in unescape(m.group(0))), text)
    return ET.fromstring('<root xmlns:ac="urn:ac" xmlns:ri="urn:ri">' + text + '</root>')


def storage_markdown(text: str) -> str:
    """Normalize supported Storage structure without fetching any resources."""
    root = parse_storage(text)

    def render(node):
        tag = node.tag.split('}')[-1]
        inner = (node.text or '') + ''.join(render(c) + (c.tail or '') for c in node)
        if node.tag == '{urn:ac}structured-macro':
            name = node.get('{urn:ac}name')
            if name == 'anchor':
                parameter = next((p for p in node.findall('{urn:ac}parameter')
                                  if p.get('{urn:ac}name') == ''), None)
                target = ''.join(parameter.itertext()).strip() if parameter is not None else ''
                if not target:
                    raise ValueError('empty anchor macro')
                return '<a id="' + escape(target, quote=True) + '"></a>'
            if name in {'code', 'noformat', 'toc'}:
                return ''
            body = node.find('{urn:ac}rich-text-body')
            return render(body) if body is not None else ''
        if node.tag == '{urn:ac}link':
            body = node.find('{urn:ac}plain-text-link-body')
            if body is None:
                body = node.find('{urn:ac}link-body')
            label = ''.join(body.itertext()) if body is not None else ''
            target = node.get('{urn:ac}anchor', '')
            if any(c.tag.startswith('{urn:ri}') for c in node):
                # Explicit page/attachment context is external, never a local anchor.
                return '[' + label + '](external:resource)'
            return '[' + label + '](#' + target + ')' if target else label
        if tag == 'a':
            if 'href' in node.attrib:
                return '[' + inner + '](' + node.attrib['href'] + ')'
            target = node.get('id') or node.get('name')
            return '<a id="' + escape(target, quote=True) + '"></a>' + inner if target else inner
        if re.fullmatch(r'h[1-6]', tag):
            return '\n' + '#' * int(tag[1]) + ' ' + inner.strip() + '\n'
        if tag == 'tr':
            cells = [render(c).strip().replace('\n', ' ') for c in node]
            return '\n| ' + ' | '.join(cells) + ' |\n'
        if tag in {'code', 'pre'}:
            return ''
        if tag in {'p', 'div', 'table', 'ul', 'ol', 'br'}:
            return '\n' + inner + '\n'
        if tag == 'li':
            return '\n- ' + inner.strip() + '\n'
        return inner

    return render(root)


def active_lines(text: str) -> list[str]:
    """Keep positions but exclude revision records and external source row content."""
    text = re.sub(r'<!--[\s\S]*?-->', lambda m: '\n' * m[0].count('\n'), text)
    lines = without_fenced_code(body_without_metadata(text)).splitlines()
    skip_level = None
    front_table = False
    sources = False
    for i, line in enumerate(lines):
        cleaned = plain(line)
        heading = re.match(r'^(#{1,6})\s+(.+)', cleaned)
        if heading:
            level = len(heading[1])
            if skip_level is not None and level <= skip_level:
                skip_level = None
            title = re.sub(r'^\d+(?:\.\d+)*\.?\s*', '', heading[2]).rstrip('：:')
            front_table = False
            if level <= 2:
                sources = title == '来源与参考资料'
            if title == '版本修订记录':
                skip_level = level
        if skip_level is not None:
            lines[i] = ''
            continue
        if cleaned.rstrip('：:') == '版本修订记录':
            front_table = True
            lines[i] = ''
            continue
        if front_table:
            if not cleaned or cleaned.startswith('|'):
                lines[i] = ''
                continue
            front_table = False
        if sources and line.lstrip().startswith('|'):
            # Preserve the source definition; other cells describe external material.
            cells = line.split('|')
            lines[i] = '| ' + cells[1] + ' |' if len(cells) > 2 else ''
        lines[i] = re.sub(r'(?:原|旧|废弃|历史|参考外部)(?:规则|功能|需求|决策|编号)?[:：\s]*' + ID_EXPR,
                          '', lines[i])
    return lines


def inspect(text: str, format: str = 'markdown', reference_policy: str = 'linked') -> list[str]:
    if reference_policy not in {'linked', 'location'}:
        raise ValueError('unsupported reference policy: ' + reference_policy)
    if format == 'storage':
        text = storage_markdown(text)
    lines = active_lines(text)
    findings = []
    definitions = defaultdict(list)
    definition_names = {}
    line_definitions = {}
    headings = []
    heading_titles = defaultdict(list)
    anchors = defaultdict(list)
    links = []
    refs = {}
    counts = Counter()
    section = ''
    parsed = [plain(ANCHOR.sub('', line)) for line in lines]
    fr_headings = {m[1] for line in parsed
                   if (m := HEADING_DEF.match(line) or NAMED_HEADING_DEF.match(line))
                   and m[1].startswith('FR-')}

    for i, line in enumerate(lines):
        if m := REF_DEF.match(line):
            refs[m[1].casefold()] = m[2].strip('<>')
        for m in ANCHOR.finditer(line):
            anchors[unescape(m[1])].append(i)
        cleaned = parsed[i]
        heading = re.match(r'^(#{1,6})\s+(.+?)\s*#*$', cleaned)
        if heading:
            level = len(heading[1])
            headings.append((i, level))
            heading_titles[heading[2]].append((i, level))
            if level == 2:
                section = re.sub(r'^\d+\.?\s*', '', heading[2]).strip()
            if format == 'markdown':
                label = INLINE.sub(lambda m: m[1], heading[2])
                slug = re.sub(r'[^\w\-\s]', '', label.lower()).replace(' ', '-')
                suffix = counts[slug]
                counts[slug] += 1
                anchors[slug + (f'-{suffix}' if suffix else '')].append(i)
        match = HEADING_DEF.match(cleaned) or NAMED_HEADING_DEF.match(cleaned)
        if match is None:
            match = LIST_DEF.match(cleaned) or NAMED_LIST_DEF.match(cleaned)
            if match and match[1].startswith({'范围与边界': ('FR-',),
                                              '功能与交互规格': ('BR-', 'NFR-')}.get(section, ())):
                match = None
        if match is None:
            match = TABLE_DEF.match(cleaned) or NAMED_TABLE_DEF.match(cleaned)
            if match and match[1] in fr_headings:
                match = None
        if match:
            item = match[1]
            definitions[item].append(i)
            line_definitions[i] = item
            label = cleaned[:match.end()]
            named = re.search(r'(.+?)[（(]' + re.escape(item) + r'[）)]', label)
            if not named:
                findings.append(f'line {i + 1}: definition must use name (ID): {item}')
            else:
                name = re.sub(r'^(?:#{1,6}\s+(?:\d+(?:\.\d+)*\.?\s+)?|[-*]\s+|\d+\.\s+|\|\s*(?:\d+\s*\|\s*)?)', '', named[1]).strip()
                definition_names[item] = name

    for target, locations in anchors.items():
        if len(locations) != 1:
            findings.append(f'duplicate anchor: {target}')
    for item, locations in definitions.items():
        if len(locations) != 1:
            findings.append(f'duplicate definition: {item}')

    for i, line in enumerate(lines):
        if REF_DEF.match(line):
            continue
        # Ignore inline examples, images, targets and tags when locating naked IDs.
        remainder = re.sub(r'`+[^`]*`+', '', line)
        remainder = re.sub(r'!\[[^\]]*\](?:\([^\n]*?\)|\[[^\]]*\])', '', remainder)

        def take(match):
            links.append((i, plain(match[1]), match[2].strip('<>')))
            return ''

        remainder = INLINE.sub(take, remainder)

        def take_ref(match):
            key = (match[2] or match[1]).casefold()
            links.append((i, plain(match[1]), refs.get(key, '')))
            return ''

        remainder = REF_USE.sub(take_ref, remainder)

        def take_short(match):
            if match[1].casefold() in refs:
                links.append((i, plain(match[1]), refs[match[1].casefold()]))
                return ''
            return match[0]

        remainder = SHORT_REF.sub(take_short, remainder)
        remainder = re.sub(r'<[^>]*>|https?://\S+', '', remainder)

        def take_location(match):
            label, title = plain(match[1]), plain(match[2])
            named = NAMED_LABEL.fullmatch(label)
            if not named or not named[1].strip() or len(ID_PATTERN.findall(label)) != 1:
                findings.append(f'line {i + 1}: location reference must use one name (ID): {label}')
                return ''
            name, item = named[1].strip(), named[2]
            locations = definitions.get(item, [])
            if len(locations) != 1 or definition_names.get(item) != name:
                findings.append(f'line {i + 1}: location reference name or unique definition mismatch: {item}')
                return ''
            targets = heading_titles.get(title, [])
            if len(targets) != 1:
                findings.append(f'line {i + 1}: missing or ambiguous location heading: {title}')
                return ''
            start, level = targets[0]
            end = next((n for n, depth in headings if n > start and depth <= level), len(lines))
            if not start <= locations[0] < end:
                findings.append(f'line {i + 1}: location does not contain definition {item}: {title}')
            return ''

        if reference_policy == 'location':
            remainder = LOCATION_REF.sub(take_location, remainder)
        # Frame IDs address one FR's interaction card, not a separate entity.
        remainder = FRAME_ID.sub('', remainder)
        bare = ID_PATTERN.findall(remainder)
        if i in line_definitions and line_definitions[i] in bare:
            bare.remove(line_definitions[i])
        for item in bare:
            findings.append(f'line {i + 1}: unlinked reference: {item}')

    for i, label, target in links:
        items = ID_PATTERN.findall(label)
        if not items:
            continue  # TOCs and general source links are outside this checker.
        if len(items) > 1:
            findings.append(f'line {i + 1}: reference must not combine multiple IDs in one link: {label}')
        if not target.startswith('#'):
            findings.append(f'line {i + 1}: external/unsupported reference target requires verification: {", ".join(items)}')
            continue
        target = unquote(target[1:])
        locations = anchors.get(target, [])
        if len(locations) != 1:
            findings.append(f'line {i + 1}: missing or ambiguous anchor: {target}')
            continue
        location = locations[0]
        # An anchor on its own belongs to the immediately following definition/heading.
        if not parsed[location]:
            following = next((n for n in range(location + 1, len(lines)) if parsed[n]), None)
            if following is not None:
                location = following
        heading = next(((n, level) for n, level in headings if n == location), None)
        end = location + 1
        if heading:
            end = next((n for n, level in headings if n > location and level <= heading[1]), len(lines))
        for item in items:
            definitions_here = definitions.get(item, [])
            # Definitions with IDs must match exactly, even if they contain subheadings.
            correct = (len(definitions_here) == 1 and
                       (definitions_here[0] == location or
                        (heading and location not in line_definitions and
                         parsed[definitions_here[0]].startswith('|') and
                         location <= definitions_here[0] < end)))
            if not correct:
                findings.append(f'line {i + 1}: anchor does not locate definition {item}: {target}')
    return findings


def validate(target: Path, format: str = 'markdown', profile: str = 'template',
             reference_policy: str = 'linked') -> dict:
    result = {'document': str(target), 'format': format, 'profile': profile,
              'reference_policy': reference_policy,
              'errors': [], 'warnings': [],
              'scope': 'Static PRD references only; no name semantics, remote access or rendered navigation verification.'}
    try:
        findings = inspect(target.read_text(encoding='utf-8-sig'), format, reference_policy)
        result['errors' if profile == 'template' else 'warnings'] = findings
        if reference_policy == 'location':
            result['warnings'].append('Location fallback enabled: verify reader limitation; clickable navigation is not certified.')
    except (OSError, UnicodeError, ValueError, ET.ParseError) as exc:
        result['errors'].append(f'cannot inspect document: {exc}')
    result['passed'] = not result['errors']
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('document', type=Path)
    parser.add_argument('--format', choices=('markdown', 'storage'), default='markdown')
    parser.add_argument('--profile', choices=('template', 'draft', 'existing'), default='template')
    parser.add_argument('--reference-policy', choices=('linked', 'location'), default='linked',
                        help='location only when navigation is unavailable; requires named references with exact heading locations')
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args()
    result = validate(args.document, args.format, args.profile, args.reference_policy)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print('Reference checks passed.' if result['passed'] else 'Reference checks failed.')
        for key in ('errors', 'warnings'):
            for message in result[key]:
                print(f'{key}: {message}')
        print(result['scope'])
    return 0 if result['passed'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
