#!/usr/bin/env python3
"""Convert PRD Markdown to Atlassian Confluence Storage Format XHTML.

Handles:
- Two-column layout with floating collapsible TOC (`assets/confluence-toc.xml`) or inline TOC
- Native anchor macros for FR/BR/AC/NFR/DEC/RK/SRC (`<ac:structured-macro ac:name="anchor">`)
- Native internal links (`<ac:link ac:anchor="...">`)
- Image attachment references (`<ac:image><ri:attachment ri:filename="..."/></ac:image>`)
- Mermaid fenced blocks replaced with deterministically hashed PNG attachment tags
- LaTeX math symbol sanitization (downgrading pseudo-math like `$\ge$` and `$\to$` to Unicode `≥` and `→`)
- Safe XML character escaping for non-HTML angle brackets
"""
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
import re
import sys
from urllib.parse import unquote
import xml.etree.ElementTree as ET


LATEX_MATH_MAP = {
    r'\ge': '≥',
    r'\geq': '≥',
    r'\le': '≤',
    r'\leq': '≤',
    r'\to': '→',
    r'\rightarrow': '→',
    r'\leftarrow': '←',
    r'\pm': '±',
    r'\ne': '≠',
    r'\neq': '≠',
    r'\times': '×',
    r'\approx': '≈',
    r'\in': '∈',
    r'\notin': '∉',
    r'\subset': '⊂',
    r'\cup': '∪',
    r'\cap': '∩',
    r'\infty': '∞',
    r'\degree': '°',
    r'\circ': '°',
}


def sanitize_latex(text: str) -> str:
    """Clean up pseudo-math LaTeX expressions in text.
    
    Replaces common LaTeX comparison and arrow symbols inside $...$ with
    Unicode characters and removes the $ delimiters.
    """
    def replace_math(m: re.Match) -> str:
        content = m.group(1).strip()
        for cmd, sym in LATEX_MATH_MAP.items():
            content = re.sub(re.escape(cmd) + r'(?![a-zA-Z])', sym, content)
        return content

    # Match $...$ where $ is not preceded by backslash and not empty
    cleaned = re.sub(r'(?<!\\)\$([^$\n]+?)(?<!\\)\$', replace_math, text)
    # Also handle standalone unescaped LaTeX command fragments even if $ was missed
    for cmd, sym in LATEX_MATH_MAP.items():
        cleaned = re.sub(re.escape(cmd) + r'(?![a-zA-Z])', sym, cleaned)
    return cleaned


def escape_xml_characters(text: str) -> str:
    """Escape ampersands and angle brackets that are not part of HTML tags or entities."""
    # Escape standalone & that is not already an XML entity
    text = re.sub(r'&(?!(?:amp|lt|gt|quot|apos|#\d+|#x[0-9a-fA-F]+);)', '&amp;', text)
    # Escape non-HTML angle brackets like <全部其他值>, <任意>, etc.
    text = re.sub(r'<([^a-zA-Z/!_][^>]*)>', r'&lt;\1&gt;', text)
    # Escape standalone < followed by space, digit or =
    text = re.sub(r'<(?=[=\s0-9])', r'&lt;', text)
    # Escape standalone > preceded by space, digit or =
    text = re.sub(r'(?<=[=\s0-9])>', r'&gt;', text)
    return text


def inline_formatting(text: str) -> str:
    """Format inline markdown elements into HTML/Storage tags."""
    text = re.sub(r'<br\s*>', '<br/>', text, flags=re.IGNORECASE)
    text = re.sub(r'<hr\s*>', '<hr/>', text, flags=re.IGNORECASE)
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'(?<!\*)\*([^*\n]+?)\*(?!\*)', r'<em>\1</em>', text)
    text = re.sub(r'`([^`\n]+)`', r'<code>\1</code>', text)
    return text


def split_table_row(row_line: str) -> list[str]:
    """Split a Markdown table row on unescaped pipes outside inline code or tags."""
    inner = row_line.strip()[1:-1]
    cells: list[str] = []
    current: list[str] = []
    in_code = False
    in_cdata = False
    i = 0
    n = len(inner)
    while i < n:
        if not in_code and inner.startswith('<![CDATA[', i):
            in_cdata = True
            current.append('<![CDATA[')
            i += 9
            continue
        if in_cdata and inner.startswith(']]>', i):
            in_cdata = False
            current.append(']]>')
            i += 3
            continue
        ch = inner[i]
        if ch == '\\' and i + 1 < n and inner[i + 1] == '|':
            current.append('|')
            i += 2
            continue
        if ch == '`' and not in_cdata:
            in_code = not in_code
            current.append(ch)
            i += 1
            continue
        if ch == '|' and not in_code and not in_cdata:
            cells.append(''.join(current))
            current = []
            i += 1
            continue
        current.append(ch)
        i += 1
    cells.append(''.join(current))
    return cells


def mermaid_asset_stem(source: str) -> str:
    digest = hashlib.sha256(source.encode('utf-8')).hexdigest()[:12]
    return f'mermaid-{digest}'


def replace_mermaid_blocks(text: str) -> str:
    """Replace ```mermaid ... ``` code blocks with attachment tags."""
    pattern = re.compile(r'(?:```|~~~)\s*mermaid\b\s*(.*?)(?:```|~~~)', re.DOTALL | re.IGNORECASE)
    
    def repl(m: re.Match) -> str:
        stem = mermaid_asset_stem(m.group(1).strip())
        return f'<p><ac:image><ri:attachment ri:filename="{stem}.png"/></ac:image></p>'

    return pattern.sub(repl, text)


def md_to_storage_fragment(text: str) -> str:
    """Convert a Markdown section into an XHTML Storage fragment."""
    text = replace_mermaid_blocks(text)
    text = sanitize_latex(text)
    text = escape_xml_characters(text)

    # 1. Convert native anchors <a id="..."></a>
    def replace_anchor(m: re.Match) -> str:
        target = m.group(1).lower()
        return f'<ac:structured-macro ac:name="anchor" ac:schema-version="1"><ac:parameter ac:name="">{target}</ac:parameter></ac:structured-macro>'

    text = re.sub(r'<a\s+id=["\']([^"\']+)["\']\s*>\s*</a>', replace_anchor, text, flags=re.IGNORECASE)

    # 2. Convert internal links [label](#target)
    def replace_link(m: re.Match) -> str:
        label = m.group(1)
        target = unquote(m.group(2).lstrip('#')).lower()
        label_clean = (label.replace('<strong>', '').replace('</strong>', '')
                            .replace('<code>', '').replace('</code>', '')
                            .replace('**', '').replace('`', ''))
        return f'<ac:link ac:anchor="{target}"><ac:plain-text-link-body><![CDATA[{label_clean}]]></ac:plain-text-link-body></ac:link>'

    text = re.sub(r'(?<!!)\[([^\]\n]+)\]\(#([^)\s]+)\)', replace_link, text)

    # 3. Convert image attachments ![alt](path/file.png)
    def replace_img(m: re.Match) -> str:
        raw_src = m.group(2).strip()
        if raw_src.startswith('<') and '>' in raw_src:
            src = raw_src[1:raw_src.index('>')]
        else:
            src = raw_src.split()[0]
        filename = Path(unquote(src)).name
        return f'<p><ac:image><ri:attachment ri:filename="{filename}"/></ac:image></p>'

    text = re.sub(r'!\[([^\]\n]*)\]\(([^)\n]+)\)', replace_img, text)

    lines = text.split('\n')
    out: list[str] = []
    in_table = False
    table_rows: list[list[str]] = []
    list_tag: str | None = None

    def flush_table():
        nonlocal in_table, table_rows
        if not in_table or not table_rows:
            in_table = False
            table_rows = []
            return
        
        html_table = ['<table><tbody>']
        for r_idx, row in enumerate(table_rows):
            if all(re.match(r'^\s*:?-+:?\s*$', c) for c in row if c):
                continue
            tag = 'th' if r_idx == 0 else 'td'
            cells = []
            for cell in row:
                cell_content = inline_formatting(cell.strip())
                cells.append(f'<{tag}>{cell_content}</{tag}>')
            html_table.append('<tr>' + ''.join(cells) + '</tr>')
        html_table.append('</tbody></table>')
        out.append(''.join(html_table))
        in_table = False
        table_rows = []

    def flush_list():
        nonlocal list_tag
        if list_tag:
            out.append(f'</{list_tag}>')
            list_tag = None

    for line in lines:
        stripped = line.strip()
        if not stripped:
            flush_table()
            flush_list()
            continue
        
        if re.match(r'^---+$', stripped):
            flush_table()
            flush_list()
            out.append('<hr/>')
            continue

        h_match = re.match(r'^(#{1,6})\s+(.+)$', stripped)
        if h_match:
            flush_table()
            flush_list()
            level = len(h_match.group(1))
            htext = inline_formatting(h_match.group(2).strip())
            out.append(f'<h{level}>{htext}</h{level}>')
            continue

        if stripped.startswith('|') and stripped.endswith('|'):
            flush_list()
            in_table = True
            raw_cells = split_table_row(stripped)
            table_rows.append(raw_cells)
            continue
        else:
            flush_table()

        ul_match = re.match(r'^\s*[-*]\s+(.+)$', stripped)
        if ul_match:
            if list_tag != 'ul':
                flush_list()
                out.append('<ul>')
                list_tag = 'ul'
            item_text = inline_formatting(ul_match.group(1).strip())
            out.append(f'<li>{item_text}</li>')
            continue

        ol_match = re.match(r'^\s*\d+\.\s+(.+)$', stripped)
        if ol_match:
            if list_tag != 'ol':
                flush_list()
                out.append('<ol>')
                list_tag = 'ol'
            item_text = inline_formatting(ol_match.group(1).strip())
            out.append(f'<li>{item_text}</li>')
            continue

        flush_list()

        if stripped.startswith('>'):
            qtext = inline_formatting(stripped.lstrip('> ').strip())
            out.append(f'<blockquote><p>{qtext}</p></blockquote>')
            continue

        ptext = inline_formatting(stripped)
        out.append(f'<p>{ptext}</p>')

    flush_table()
    flush_list()
    return '\n'.join(out)


def convert_markdown_to_storage(markdown_text: str, template_layout: str, layout: str = 'floating') -> str:
    """Convert full markdown document to storage format."""
    # Strip leading document H1 title (e.g. # Document Title) because Confluence natively
    # renders the page title at the top of the page, avoiding duplicate visual headings.
    markdown_text = re.sub(r'^\s*#\s+[^\n]+\n*', '', markdown_text, count=1)

    # Split markdown into front matter (before ## 目录) and body (after [TOC])
    parts = re.split(r'##\s+目录\s*\n\s*\[TOC\]\s*\n', markdown_text, maxsplit=1)
    if len(parts) == 2:
        front_md, body_md = parts[0], parts[1]
    else:
        front_md, body_md = "", markdown_text

    front_storage = md_to_storage_fragment(front_md)
    body_storage = md_to_storage_fragment(body_md)

    if layout == 'floating':
        final_storage = (template_layout
                         .replace('{{FRONT_MATTER_STORAGE}}', front_storage)
                         .replace('{{BODY_STORAGE}}', body_storage))
    else:
        # Inline TOC layout
        toc_macro = (
            '<ac:structured-macro ac:name="toc" ac:schema-version="1">'
            '<ac:parameter ac:name="minLevel">2</ac:parameter>'
            '<ac:parameter ac:name="maxLevel">3</ac:parameter>'
            '</ac:structured-macro>'
        )
        final_storage = f'{front_storage}\n{toc_macro}\n{body_storage}'

    # Validate XML well-formedness
    wrapped_xml = f'<root xmlns:ac="urn:ac" xmlns:ri="urn:ri">{final_storage}</root>'
    try:
        ET.fromstring(wrapped_xml)
    except ET.ParseError as exc:
        raise ValueError(f'Generated Confluence Storage XML is malformed: {exc}')

    return final_storage


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description='Convert PRD Markdown to Atlassian Confluence Storage Format XHTML')
    parser.add_argument('markdown', type=Path, help='Input PRD Markdown file path')
    parser.add_argument('--output', required=True, type=Path, help='Output Storage XML file path')
    parser.add_argument('--layout', choices=['floating', 'inline'], default='floating',
                        help='Layout style: floating (default, two_right_sidebar with toc) or inline')
    parser.add_argument('--template', type=Path, help='Path to confluence-toc.xml (optional)')
    args = parser.parse_args(argv)

    if not args.markdown.is_file():
        print(f"Error: input markdown file not found: {args.markdown}", file=sys.stderr)
        return 1

    template_path = args.template
    if not template_path:
        # Auto-discover assets/confluence-toc.xml
        skill_root = Path(__file__).resolve().parents[1]
        template_path = skill_root / 'assets' / 'confluence-toc.xml'

    if args.layout == 'floating' and not template_path.is_file():
        print(f"Error: layout template not found: {template_path}", file=sys.stderr)
        return 1

    template_layout = template_path.read_text(encoding='utf-8-sig') if template_path.is_file() else ''
    markdown_text = args.markdown.read_text(encoding='utf-8-sig')

    try:
        storage = convert_markdown_to_storage(markdown_text, template_layout, layout=args.layout)
    except ValueError as exc:
        print(f"Conversion error: {exc}", file=sys.stderr)
        return 1

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(storage, encoding='utf-8')
    print(f"Confluence Storage successfully generated: {args.output}")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
