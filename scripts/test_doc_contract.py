#!/usr/bin/env python3
"""Contract tests for the documentation architecture itself.

These tests encode the layering the skill promises, focusing on structural
invariants (relative link resolution, reachable assets, vocabulary consistency,
and absence of rotting vendor facts) rather than fragile string whitelists.
"""
from pathlib import Path
import inspect
import re
import unittest

import validate_prd


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'SKILL.md'

# Facts rot and rosters date; the benchmark method must stay vendor-free and
# require live verification instead of shipping remembered behaviour.
VENDOR_DENYLIST = ('AutoCAD', 'BricsCAD', 'SolidWorks', 'MicroStation', 'CATIA',
                   'PTC Creo', 'Siemens NX', '中望CAD', 'ZWCAD')


def markdown_files():
    return sorted(path for path in ROOT.rglob('*.md')
                  if not {'.git', '.tmp'} & set(path.parts))


class TemplatePurityTests(unittest.TestCase):
    def setUp(self):
        self.text = (ROOT / 'assets/prd-template.md').read_text(encoding='utf-8-sig')

    def test_template_keeps_the_skeleton_and_points_to_the_rules(self):
        for heading in ('## 0. 决策摘要', '## 1. 背景、用户与目标',
                        '## 3. 功能与交互规格', '## 9. 来源与参考资料'):
            self.assertIn(heading, self.text)
        self.assertIn('prd-standard.md', self.text)
        self.assertIn('delivery.md', self.text)


class NoRottingFactsTests(unittest.TestCase):
    """Rules state purpose and boundaries; vendor facts live in the run, not the skill."""

    def test_benchmark_method_keeps_no_fixed_vendor_roster(self):
        text = (ROOT / 'references/prd-benchmark.md').read_text(encoding='utf-8-sig')
        for vendor in VENDOR_DENYLIST:
            with self.subTest(vendor=vendor):
                self.assertNotIn(vendor, text,
                                 'label the product set at run time; do not ship a fixed roster')

    def test_benchmark_requires_live_verification(self):
        text = (ROOT / 'references/prd-benchmark.md').read_text(encoding='utf-8-sig')
        self.assertIn('查证当前资料', text)
        self.assertIn('来源', text)

    def test_no_shipped_facts_outside_the_benchmark(self):
        # The other reference files carry stable boundaries, not vendor behaviour.
        for path in sorted((ROOT / 'references').glob('*.md')):
            if path.name == 'prd-benchmark.md':
                continue
            text = path.read_text(encoding='utf-8-sig')
            for vendor in VENDOR_DENYLIST:
                with self.subTest(file=path.name, vendor=vendor):
                    self.assertNotIn(vendor, text)


class EntryCoverageTests(unittest.TestCase):
    def setUp(self):
        self.skill = SKILL.read_text(encoding='utf-8-sig')

    def test_every_reference_is_reachable_from_the_entry(self):
        for path in sorted((ROOT / 'references').glob('*.md')):
            with self.subTest(reference=path.name):
                self.assertIn(f'references/{path.name}', self.skill)

    def test_every_runtime_script_is_listed(self):
        for path in sorted((ROOT / 'scripts').glob('*.py')):
            if path.name.startswith('test_'):
                continue
            with self.subTest(script=path.name):
                self.assertIn(path.name, self.skill)

    def test_entry_does_not_reintroduce_mandatory_reading(self):
        self.assertNotIn('每次必读', self.skill)
        self.assertNotIn('必须读取', self.skill)


LINK_PATTERN = re.compile(r'!?\[[^\]]*\]\(([^)\s]+)\)')
REGISTERED_ASSETS = (
    'assets/confluence-toc.xml',
    'assets/prd-template.md',
    'assets/help-template.md',
    'assets/story-map-schema.md',
)
REGISTERED_HELP_ASSETS = (
    'assets/help/help-demo',
    'assets/help/multilanguage-mapping.txt',
)


def docs_blob() -> str:
    return '\n'.join(path.read_text(encoding='utf-8-sig') for path in markdown_files())


class AssetReachabilityTests(unittest.TestCase):
    def test_every_asset_is_referenced_from_documentation(self):
        blob = docs_blob()
        for asset in REGISTERED_ASSETS:
            with self.subTest(asset=asset):
                self.assertIn(asset, blob)

    def test_help_sample_and_dictionary_are_registered(self):
        blob = docs_blob()
        for asset in REGISTERED_HELP_ASSETS:
            with self.subTest(asset=asset):
                self.assertIn(asset, blob)


class RelativeLinkTests(unittest.TestCase):
    def test_relative_markdown_links_resolve(self):
        for path in markdown_files():
            text = validate_prd.without_fenced_code(path.read_text(encoding='utf-8-sig'))
            for target in LINK_PATTERN.findall(text):
                if target.startswith(('http://', 'https://', '#', 'mailto:')):
                    continue
                clean = target.split('#', 1)[0].strip()
                if not clean:
                    continue
                resolved = (path.parent / clean).resolve()
                with self.subTest(file=path.relative_to(ROOT).as_posix(), target=target):
                    self.assertTrue(resolved.exists(),
                                    f'{path.name} links to missing {target}')


class VocabularyTests(unittest.TestCase):
    def test_validator_id_types_are_defined_in_the_standard(self):
        match = re.search(r'\(\?:([A-Z|]+)\)-', validate_prd.ID_EXPR)
        self.assertIsNotNone(match, 'ID_EXPR must expose its type list')
        standard = (ROOT / 'references/prd-standard.md').read_text(encoding='utf-8-sig')
        for id_type in match.group(1).split('|'):
            with self.subTest(id_type=id_type):
                self.assertRegex(standard, rf'(?<![A-Z]){id_type} ')

    def test_validator_section_names_exist_in_the_template(self):
        template = (ROOT / 'assets/prd-template.md').read_text(encoding='utf-8-sig')
        source = inspect.getsource(validate_prd.definitions_in)
        block = re.search(r'reference_prefixes = \{(.*?)\}', source, re.S)
        self.assertIsNotNone(block, 'reference_prefixes must stay discoverable')
        for name in re.findall(r"'([^']+)':", block.group(1)):
            with self.subTest(section=name):
                self.assertIn(name, template,
                              f'"{name}" is hardcoded in validate_prd but absent from the template')


if __name__ == '__main__':
    unittest.main()
