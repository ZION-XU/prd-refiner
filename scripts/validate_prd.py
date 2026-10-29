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
    ('## 6. 风险与开放问题', '## 8. 风险与开放问题'),
    ('## 7. 来源与参考资料', '## 9. 来源与参考资料'),
)
ID_EXPR = r'(?:FR|BR|AC|DEC|NFR|RK|SRC)-\d{2,4}'
ID_PATTERN = re.compile(r'\b' + ID_EXPR + r'\b')
# Frame identifiers belong to one FR's interaction card; they are not entity IDs.
FRAME_ID = re.compile(r'FR-\d{2,4}-S\d{1,2}')
TABLE_SEPARATOR = re.compile(r'^\s*\|(?:\s*:?-{2,}:?\s*\|)+\s*$')
NONE_DECLARED = re.compile(r'交互卡\s*[：:]\s*未涉及\s*[（(][^）)\n]{4,}[）)]')
PLACEHOLDER_PATTERN = re.compile(
    r'\{(?:REQ-ID|YYYY-MM-DD|需求名称|需求负责人|文档版本|功能名称|填写|待填写|'
    r'草稿/|待补充工作稿/)[^{}\n]*\}|<(?:填写|待填写)[^>\n]*>'
)
TEMPLATE_TAG_PATTERN = re.compile(r'【(?:核心|按需|多功能时填写)[^】\n]*】')
HEADING_DEF = re.compile(r'^#{2,6}\s+(?:\d+(?:\.\d+)*\.?\s+)?(' + ID_EXPR + r')\b')
LIST_DEF = re.compile(r'^\s*(?:[-*]|\d+\.)\s+(' + ID_EXPR + r')(?=\s|[:：]|$)')
TABLE_DEF = re.compile(r'^\|\s*(?:(?:\d+|[-*#])\s*\|\s*)?(' + ID_EXPR + r')(?=\s|[:：]|\|)')
# Name-first declarations are bounded to a heading, list label or first data cell.
# Linked labels are references, so they must not satisfy missing definitions.
NAMED_ID = r'[^|\[\]\n]+?[（(](' + ID_EXPR + r')[）)]'
NAMED_HEADING_DEF = re.compile(r'^#{2,6}\s+' + NAMED_ID + r'\s*(?:#+\s*)?$')
NAMED_LIST_DEF = re.compile(r'^\s*(?:[-*]|\d+\.)\s+' + NAMED_ID + r'(?=\s|[:：]|$)')
NAMED_TABLE_DEF = re.compile(r'^\|\s*(?:(?:\d+|[-*#])\s*\|\s*)?' + NAMED_ID + r'\s*\|')
EMPTY_ANCHOR = re.compile(r'<a\s+(?:id|name)\s*=\s*["\'][^"\']*["\']\s*>\s*</a>', re.IGNORECASE)
INLINE_IMAGE = re.compile(r'!\[[^\]\n]*\]\(\s*(<[^>\n]+>|[^\s)]+)(?:\s+["\'][^\n]*?["\'])?\s*\)')
REFERENCE_IMAGE = re.compile(r'!\[([^\]\n]*)\]\[([^\]\n]*)\]')
REFERENCE_LINK = re.compile(r'^\s*\[([^\]]+)\]:\s*(<[^>\n]+>|\S+)', re.MULTILINE)

VENDOR_DENYLIST = (
    'AutoCAD', 'BricsCAD', 'SolidWorks', 'MicroStation', 'CATIA',
    'PTC Creo', 'Siemens NX'
)


def _vendor_pattern(vendor: str) -> re.Pattern:
    parts = [re.escape(p) for p in re.split(r'\s+', vendor.strip())]
    sub = r'\s+'.join(parts)
    return re.compile(rf'(?<![A-Za-z]){sub}(?![A-Za-z])', re.IGNORECASE)


VENDOR_PATTERNS = tuple((vendor, _vendor_pattern(vendor)) for vendor in VENDOR_DENYLIST)


def check_vendor_mentions(prose: str, findings: list[str]) -> None:
    """Flag competitor vendor names in PRD prose to uphold cleanroom and objective style contracts."""
    for line_no, line in enumerate(prose.splitlines(), start=1):
        for vendor, pattern in VENDOR_PATTERNS:
            match = pattern.search(line)
            if match:
                findings.append(
                    f'forbidden vendor mention: "{match.group(0)}" on line {line_no} (matches {vendor}); '
                    'use neutral engineering terminology (e.g. 传统 CAD / 主流第三方 CAD 宿主) '
                    'and keep competitor benchmarks in _需求探讨.md / _竞品分析.md'
                )


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
    lines = [EMPTY_ANCHOR.sub('', line).replace('**', '').replace('`', '')
             for line in text.splitlines()]
    heading_ids = [m.group(1) for line in lines
                   if (m := HEADING_DEF.match(line) or NAMED_HEADING_DEF.match(line))]
    definitions = list(heading_ids)
    section = ''
    for line in lines:
        heading = re.match(r'^##\s+(?:\d+\.\s*)?(.+)$', line)
        if heading:
            section = heading.group(1).split('【', 1)[0].strip()
        match = LIST_DEF.match(line) or NAMED_LIST_DEF.match(line)
        if match:
            item = match.group(1)
            # These template sections list references, not new definitions.
            reference_prefixes = {
                '范围与边界': ('FR-',),
                '功能与交互规格': ('BR-', 'NFR-'),
            }.get(section, ())
            if not item.startswith(reference_prefixes):
                definitions.append(item)
        match = TABLE_DEF.match(line) or NAMED_TABLE_DEF.match(line)
        if match:
            item = match.group(1)
            # A functional heading is authoritative; its FR table row is an index.
            if not (item.startswith('FR-') and item in heading_ids):
                definitions.append(item)
    return definitions


def split_table_row(line: str) -> list[str]:
    text = line.strip()
    if text.startswith('|'):
        text = text[1:]
    if text.endswith('|'):
        text = text[:-1]
    return [cell.strip() for cell in text.split('|')]


def markdown_tables(lines: list[str]) -> list[tuple[list[str], list[list[str]]]]:
    """Return pipe tables that carry a header separator; prose is left alone."""
    tables = []
    index = 0
    while index < len(lines) - 1:
        if lines[index].strip().startswith('|') and TABLE_SEPARATOR.match(lines[index + 1]):
            header = split_table_row(lines[index])
            rows = []
            cursor = index + 2
            while cursor < len(lines) and lines[cursor].strip().startswith('|'):
                rows.append(split_table_row(lines[cursor]))
                cursor += 1
            tables.append((header, rows))
            index = cursor
        else:
            index += 1
    return tables


def fr_blocks(body: str) -> list[tuple[str, str]]:
    """Return each FR definition heading with the lines that belong to it."""
    lines = body.splitlines()
    found = []
    for index, line in enumerate(lines):
        match = HEADING_DEF.match(line) or NAMED_HEADING_DEF.match(line)
        if match and match.group(1).startswith('FR-'):
            found.append((index, len(line) - len(line.lstrip('#')), match.group(1)))
    blocks = []
    for index, level, item in found:
        end = len(lines)
        for later in range(index + 1, len(lines)):
            heading = re.match(r'^(#{1,6})\s', lines[later])
            if heading and len(heading.group(1)) <= level:
                end = later
                break
        blocks.append((item, '\n'.join(lines[index + 1:end])))
    return blocks


def check_interaction_cards(body: str, findings: list[str]) -> dict:
    """Check that every FR definition carries a usable interaction card."""
    coverage = {'fr_total': 0, 'with_frames': 0, 'explicit_none': 0, 'missing': 0}
    for item, block in fr_blocks(body):
        coverage['fr_total'] += 1
        if '交互卡' not in block:
            coverage['missing'] += 1
            findings.append(
                f'{item} 缺少交互卡：涉及界面或命令行时须给出帧清单与状态事件表，'
                '确无交互时写“交互卡：未涉及（具体理由）”')
            continue
        if NONE_DECLARED.search(block):
            coverage['explicit_none'] += 1
            continue
        state_ok = False
        frames_ok = False
        has_state_table = False
        has_frame_table = False
        for header, rows in markdown_tables(block.splitlines()):
            joined = ' '.join(header)
            data = [row for row in rows if any(cell.strip() for cell in row)]
            if '状态' in joined:
                has_state_table = True
                if '反馈' in joined or '可见' in joined:
                    state_ok = state_ok or len(data) >= 2
            if '帧 ID' in joined and '画面' in joined:
                has_frame_table = True
                picture = next((i for i, cell in enumerate(header) if '画面' in cell), None)
                for row in data:
                    if not FRAME_ID.search(' '.join(row)):
                        continue
                    cell = row[picture] if picture is not None and picture < len(row) else ' '.join(row)
                    if '![' in cell or '](' in cell:
                        frames_ok = True
        if not state_ok and not has_state_table:
            # Also accept prototype-centric state walkthrough sections (e.g. 状态一 / S1 with UI feedback)
            state_headings = re.findall(r'(?:#{3,6}\s+.*?(?:状态|S\d)|(?:^|\n)\s*[-*]\s*.*?S\d)', block)
            has_feedback_prose = any(kw in block for kw in ('反馈', '可见', '操作说明', '界面要素', '回显'))
            if len(state_headings) >= 1 and has_feedback_prose:
                state_ok = True
        if not frames_ok and not has_frame_table:
            # Also accept inline prototype frame images embedded in the section
            found_frames = FRAME_ID.findall(block)
            has_image = bool(INLINE_IMAGE.search(block) or REFERENCE_IMAGE.search(block) or '![' in block)
            if found_frames and has_image:
                frames_ok = True

        if not state_ok:
            findings.append(f'{item} 交互卡缺少状态与事件表（表头含“状态”“可见反馈”，至少两个状态行，或采用以原型为中心的状态走查）')
        if not frames_ok:
            findings.append(
                f'{item} 交互卡缺少有效帧清单（表头含“帧 ID”“画面”，'
                '至少一行含 FR-xxx-Sx 帧号并给出本地图片或原型链接；或在走查中嵌入有效帧图）')
        if '取消' not in block:
            findings.append(f'{item} 交互卡未写明取消、回滚与撤销')
        if frames_ok:
            coverage['with_frames'] += 1
    return coverage


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


def check_empty_echo_headings(body: str, errors: list[str]) -> None:
    """Detect and forbid empty echo headings like '见上表详细定义'."""
    lines = body.splitlines()
    i = 0
    n = len(lines)
    while i < n:
        line = lines[i].strip()
        # Look for section headings defining an ID
        if re.match(r'^#{2,6}\s+[^|\n]+?[（(](' + ID_EXPR + r')[）)]\s*#*$', line):
            heading_title = line
            prose_lines = []
            j = i + 1
            while j < n and not re.match(r'^#{1,6}\s+', lines[j].strip()):
                cleaned = lines[j].strip()
                if cleaned and not cleaned.startswith('<!--') and not EMPTY_ANCHOR.match(cleaned):
                    prose_lines.append(cleaned)
                j += 1
            if prose_lines:
                combined = ''.join(prose_lines).replace(' ', '')
                if re.match(r'^(?:(?:详?见|参考|按)?(?:上表|上述表格|前表)(?:详细(?:定义|用例|说明|记录|内容|规格))?[。.]?|见上[。.]?)$', combined):
                    errors.append(f'empty echo heading without substantive rules: "{heading_title}" -> "{combined}"; use table anchor instead of empty heading')
            i = j
        else:
            i += 1


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
        self.native_count = 0

    def handle_starttag(self, tag, attrs):
        if tag.casefold() == 'ac:image':
            self.native_count += 1
        if tag.casefold() == 'img':
            values = dict(attrs)
            self.targets.append(values.get('src') or '')
            self.has_srcset |= 'srcset' in values


def image_reference_count(text: str) -> int:
    """Count embedded references, not attachments or filenames in prose."""
    text = without_fenced_code(re.sub(r'<!--[\s\S]*?-->', '', text))
    images = HTMLImages()
    images.feed(text)
    return (len(images.targets) + images.native_count +
            len(INLINE_IMAGE.findall(text)) + len(REFERENCE_IMAGE.findall(text)))


def compare_image_counts(source_count: int, output_count: int, errors: list[str],
                         warnings: list[str], profile: str = 'template') -> dict:
    if source_count and not output_count:
        (errors if profile == 'template' else warnings).append(
            'source contains images but output has none; preserve source images or report an explicit omission')
    elif output_count < source_count:
        warnings.append('fewer image references than source; reconcile retained, replaced and omitted images individually')
    return {'source_references': source_count, 'output_references': output_count,
            'scope': 'Counts only; image identity, justified omissions and visual content require review.'}


def compare_source_images(source: Path, output: str, errors: list[str],
                          warnings: list[str], profile: str = 'template') -> dict | None:
    try:
        original = source.read_text(encoding='utf-8-sig')
    except (OSError, UnicodeError) as exc:
        errors.append(f'cannot read source image baseline: {type(exc).__name__}: {source}')
        return None
    return compare_image_counts(image_reference_count(original), image_reference_count(output),
                                errors, warnings, profile)


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


def validate(target: Path, profile: str = 'template', image_policy: str | None = None,
             *, source: Path | None = None) -> dict:
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

    # Complete outputs reject empty echo headings; drafts and source documents
    # report them without turning an input diagnostic into a failed deliverable.
    check_empty_echo_headings(body, errors if profile == 'template' else warnings)

    # Vendor purity check: cleanroom PRDs must not mention competitor vendors.
    check_vendor_mentions(prose, errors if profile == 'template' else warnings)

    # Interaction cards are where per-function detail lives; drafts and source
    # documents report the same findings as warnings.
    if profile != 'existing':
        result['interaction_coverage'] = check_interaction_cards(
            body, errors if profile == 'template' else warnings)

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
    if source is not None:
        result['image_comparison'] = compare_source_images(source, text, errors, warnings, profile)
    result['passed'] = not errors
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('target', type=Path, help='PRD file, or directory containing prd.md')
    parser.add_argument('--profile', choices=('template', 'draft', 'existing'), default='template',
                        help='template: new/optimized output; draft: unfinished output; existing: input-only diagnostic')
    parser.add_argument('--json', action='store_true', help='emit machine-readable results')
    parser.add_argument('--source', type=Path, help='original Markdown/HTML/Storage snapshot for image-retention checks')
    parser.add_argument('--image-policy', choices=('local', 'external'), default=None,
                        help='default: local for output, external for existing input; external output requires an explicit user choice')
    args = parser.parse_args(argv)
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    result = validate(args.target, args.profile, args.image_policy, source=args.source)
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
