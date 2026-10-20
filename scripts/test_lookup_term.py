#!/usr/bin/env python3
"""Unit tests for the help translation dictionary lookup."""
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from lookup_term import main, parse_mapping


# Synthetic, de-identified dictionary: the real one is internal and is never committed.
MAPPING = """\
[eng_kor]
9 1==>18 1
Line==>선
LINE==>LINE
Options==>옵션
Snap, Midpoint==>스냅, 중간점
[eng_deu]
Line==>Linie
Options==>Optionen
[eng_chs]
ZWCAD==>中望CAD
"""


def run(argv):
    """Run the CLI and return (exit code, parsed JSON)."""
    buffer = io.StringIO()
    with patch('sys.stdout', new=buffer):
        code = main(argv)
    return code, json.loads(buffer.getvalue())


class MappingParseTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.mapping = self.root / 'mapping.txt'
        self.mapping.write_text(MAPPING, encoding='utf-8')

    def test_sections_and_counts_follow_file_order(self):
        index, folded, counts, languages = parse_mapping(self.mapping)
        self.assertEqual(languages, ['eng_kor', 'eng_deu', 'eng_chs'])
        self.assertEqual(counts, {'eng_kor': 5, 'eng_deu': 2, 'eng_chs': 1})
        self.assertEqual(len(index), 6)  # Line and LINE stay distinct keys
        self.assertEqual(folded['line'], ['Line', 'LINE'])

    def test_exact_key_wins_over_case_variant(self):
        code, result = run(['--mapping', str(self.mapping), '--terms', 'LINE'])
        self.assertEqual(code, 0)
        self.assertEqual(result['hits'][0]['english'], 'LINE')
        self.assertEqual(result['hits'][0]['case_variants'], [])
        code, result = run(['--mapping', str(self.mapping), '--terms', 'Line'])
        self.assertEqual(code, 0)
        self.assertEqual(result['hits'][0]['english'], 'Line')

    def test_case_fallback_prefers_the_translated_variant(self):
        code, result = run(['--mapping', str(self.mapping), '--terms', 'line'])
        self.assertEqual(code, 0)
        hit = result['hits'][0]
        self.assertEqual(hit['english'], 'Line')  # not the untranslated LINE echo
        self.assertEqual(hit['case_variants'], ['LINE'])

    def test_lookup_keeps_canonical_english_and_all_sections(self):
        code, result = run(['--mapping', str(self.mapping), '--terms', 'Line'])
        self.assertEqual(code, 0)
        self.assertEqual(result['hits'][0]['english'], 'Line')
        self.assertEqual(result['hits'][0]['translations']['eng_kor'], '선')
        self.assertEqual(result['hits'][0]['translations']['eng_deu'], 'Linie')

    def test_terms_may_contain_commas(self):
        code, result = run(['--mapping', str(self.mapping), '--terms', 'Snap, Midpoint'])
        self.assertEqual(code, 0)
        self.assertEqual(result['hits'][0]['term'], 'Snap, Midpoint')
        self.assertEqual(result['hits'][0]['translations']['eng_kor'], '스냅, 중간점')

    def test_chinese_term_needs_an_english_source(self):
        code, result = run(['--mapping', str(self.mapping), '--terms', '多段线'])
        self.assertEqual(code, 0)
        self.assertEqual(result['needs_english'], ['多段线'])
        self.assertFalse(result['hits'])
        self.assertFalse(result['missing'])

    def test_unmatched_english_term_is_reported_not_translated(self):
        code, result = run(['--mapping', str(self.mapping), '--terms', 'Polyline'])
        self.assertEqual(code, 0)
        self.assertEqual(result['missing'], ['Polyline'])
        self.assertFalse(result['hits'])

    def test_language_filter_limits_reported_sections(self):
        code, result = run(['--mapping', str(self.mapping), '--terms', 'Line',
                            '--langs', 'eng_kor'])
        self.assertEqual(code, 0)
        self.assertEqual(result['requested_languages'], ['eng_kor'])
        self.assertEqual(list(result['hits'][0]['translations']), ['eng_kor'])

    def test_partial_entry_reports_absent_languages(self):
        code, result = run(['--mapping', str(self.mapping), '--terms', 'ZWCAD'])
        self.assertEqual(code, 0)
        self.assertEqual(result['hits'][0]['translations'], {'eng_chs': '中望CAD'})
        self.assertEqual(result['hits'][0]['absent'], ['eng_kor', 'eng_deu'])

    def test_terms_file_skips_comments_and_repeats(self):
        path = self.root / 'terms.txt'
        path.write_text('# interface strings\nLine\n\nLine\nOptions\n', encoding='utf-8')
        code, result = run(['--mapping', str(self.mapping), '--terms-file', str(path)])
        self.assertEqual(code, 0)
        self.assertEqual([hit['term'] for hit in result['hits']], ['Line', 'Options'])

    def test_unknown_language_is_an_error(self):
        code, result = run(['--mapping', str(self.mapping), '--terms', 'Line',
                            '--langs', 'eng_kor,eng_zzz'])
        self.assertEqual(code, 1)
        self.assertIn('eng_zzz', result['errors'][0])

    def test_missing_mapping_is_an_error(self):
        code, result = run(['--mapping', str(self.root / 'absent.txt'), '--terms', 'Line'])
        self.assertEqual(code, 1)
        self.assertIn('mapping file not found', result['errors'][0])

    def test_no_terms_is_an_error(self):
        code, result = run(['--mapping', str(self.mapping)])
        self.assertEqual(code, 1)
        self.assertIn('no terms given', result['errors'][0])

    def test_relative_out_is_rejected_and_writes_nothing(self):
        code, result = run(['--mapping', str(self.mapping), '--terms', 'Line', '--out', 'terms.json'])
        self.assertEqual(code, 1)
        self.assertIn('absolute path', result['errors'][0])
        self.assertFalse((self.root / 'terms.json').exists())

    def test_out_writes_the_result_to_an_explicit_path(self):
        target = self.root / 'machine' / 'terms.json'
        code, result = run(['--mapping', str(self.mapping), '--terms', 'Line',
                            '--out', str(target)])
        self.assertEqual(code, 0)
        self.assertEqual(result['out'], str(target))
        written = json.loads(target.read_text(encoding='utf-8'))
        self.assertEqual(written['hits'][0]['translations']['eng_deu'], 'Linie')


if __name__ == '__main__':
    unittest.main()
