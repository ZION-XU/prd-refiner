#!/usr/bin/env python3
"""Look up interface strings in a user-supplied help translation dictionary.

The dictionary is keyed by English UI strings, one section per target language
(`[eng_kor]`, `[eng_deu]`, ...). Two properties decide the lookup rules:

* Key case is meaningful. `LINE` (the command token, echoed untranslated) and
  `Line` (the interface noun, translated) are separate entries, so an exact key
  always wins; a case-insensitive fallback is used only when no exact key
  exists, and it reports the variants it chose between.
* There are no Chinese keys, so a Chinese-only term cannot be looked up. Such
  terms are reported as needing an English source, never translated here.

A hit is a recorded dictionary match, not a verified translation, and this tool
never produces one. Read-only by default: results go to stdout. `--out` writes
them to an explicit absolute path; an output location is never inferred from the
current directory.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys


SECTION = re.compile(r'^\[([^\]]+)\]$')
PAIR = re.compile(r'^(.*?)==>(.*)$')
CJK = re.compile(r'[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]')


def parse_mapping(path: Path) -> tuple[dict[str, dict], dict[str, list[str]], dict[str, int], list[str]]:
    """Index exact `english -> entry`, `casefold -> [exact keys]`, and per-section counts."""
    index: dict[str, dict] = {}
    folded: dict[str, list[str]] = {}
    counts: dict[str, int] = {}
    languages: list[str] = []
    language = ''
    for line in path.read_text(encoding='utf-8-sig').splitlines():
        section = SECTION.match(line.strip())
        if section:
            language = section.group(1)
            if language not in counts:
                counts[language] = 0
                languages.append(language)
            continue
        if not language:
            continue
        pair = PAIR.match(line)
        if not pair:
            continue
        english, translation = pair.group(1).strip(), pair.group(2).strip()
        if not english:
            continue
        counts[language] += 1
        entry = index.setdefault(english, {'english': english, 'translations': {}})
        entry['translations'].setdefault(language, translation)
        variants = folded.setdefault(english.casefold(), [])
        if english not in variants:
            variants.append(english)
    return index, folded, counts, languages


def resolve(term: str, index: dict[str, dict], folded: dict[str, list[str]]) -> tuple[str | None, list[str]]:
    """Return the entry key for a term and the case variants passed over.

    Exact keys win because the dictionary distinguishes a command token from the
    interface noun spelled the same way. In the fallback, the variant carrying
    the most translations is used so that an untranslated command echo does not
    shadow the translated UI string.
    """
    if term in index:
        return term, []
    candidates = folded.get(term.casefold(), [])
    if not candidates:
        return None, []
    chosen = max(candidates, key=lambda key: len(index[key]['translations']))
    return chosen, [key for key in candidates if key != chosen]


def lookup(terms: list[str], index: dict[str, dict], folded: dict[str, list[str]],
           languages: list[str]) -> tuple[list[dict], list[str], list[str]]:
    """Split terms into dictionary hits, unmatched English, and Chinese-only terms."""
    hits: list[dict] = []
    missing: list[str] = []
    needs_english: list[str] = []
    for term in terms:
        if CJK.search(term):
            needs_english.append(term)
            continue
        english, variants = resolve(term, index, folded)
        if english is None:
            missing.append(term)
            continue
        entry = index[english]
        hits.append({
            'term': term,
            'english': english,
            'translations': {lang: entry['translations'][lang] for lang in languages
                             if lang in entry['translations']},
            'absent': [lang for lang in languages if lang not in entry['translations']],
            'case_variants': variants,
        })
    return hits, missing, needs_english


def read_terms(terms: list[str] | None, terms_file: Path | None) -> list[str]:
    """Collect terms in order, dropping blanks, comments and repeats."""
    collected = list(terms or [])
    if terms_file:
        for line in terms_file.read_text(encoding='utf-8-sig').splitlines():
            stripped = line.strip()
            if stripped and not stripped.startswith('#'):
                collected.append(stripped)
    seen: set[str] = set()
    unique: list[str] = []
    for term in collected:
        term = term.strip()
        if term and term not in seen:
            seen.add(term)
            unique.append(term)
    return unique


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description='Look up interface strings in a help translation dictionary')
    parser.add_argument('--mapping', required=True, type=Path,
                        help='Dictionary file path (absolute)')
    parser.add_argument('--terms', action='append', metavar='STRING',
                        help='One interface string; repeat the flag for several '
                             '(single strings may contain commas)')
    parser.add_argument('--terms-file', type=Path,
                        help='File with one interface string per line; # starts a comment')
    parser.add_argument('--langs',
                        help='Comma-separated dictionary sections to report (default: all found)')
    parser.add_argument('--out', type=Path,
                        help='Write the JSON result here instead of stdout (absolute path)')
    args = parser.parse_args(argv)
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    try:
        terms = read_terms(args.terms, args.terms_file)
        if not terms:
            raise ValueError('no terms given: use --terms or --terms-file')
        if not args.mapping.is_file():
            raise ValueError(f'mapping file not found: {args.mapping}')
        index, folded, counts, languages = parse_mapping(args.mapping)
        if not languages:
            raise ValueError(f'no language section found in {args.mapping}')
        wanted = languages
        if args.langs:
            wanted = [part.strip() for part in args.langs.split(',') if part.strip()]
            unknown = [lang for lang in wanted if lang not in languages]
            if unknown:
                raise ValueError('unknown language section(s): ' + ', '.join(unknown)
                                 + '; found: ' + ', '.join(languages))
        hits, missing, needs_english = lookup(terms, index, folded, wanted)
        result = {
            'ok': True,
            'mapping': {'path': str(args.mapping), 'entries': len(index),
                        'sections': languages, 'section_entries': counts},
            'requested_languages': wanted,
            'hits': hits,
            'missing': missing,
            'needs_english': needs_english,
            'scope': ('Exact dictionary lookup only: a hit is a recorded match, not a verified '
                      'translation. Missing and Chinese-only terms are reported for human '
                      'follow-up and are never translated here.'),
        }
        text = json.dumps(result, ensure_ascii=False, indent=2) + '\n'
        if args.out:
            if not args.out.is_absolute():
                raise ValueError(f'--out must be an absolute path: {args.out}')
            args.out.parent.mkdir(parents=True, exist_ok=True)
            args.out.write_text(text, encoding='utf-8')
            print(json.dumps({'ok': True, 'out': str(args.out)}, ensure_ascii=False))
        else:
            print(text, end='')
        return 0
    except (OSError, UnicodeError, ValueError) as exc:
        print(json.dumps({'ok': False, 'errors': [f'{type(exc).__name__}: {exc}']},
                         ensure_ascii=False, indent=2))
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
