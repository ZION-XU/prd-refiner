#!/usr/bin/env python3
"""Unit tests for the PRD gate ledger."""
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from gate_state import GATE_ORDER, clear, load_state, main, reset, state_path, status, waive


class GateLedgerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def test_read_of_missing_ledger_writes_nothing(self):
        state = load_state(self.root)
        self.assertEqual(status(state)['pending'], list(GATE_ORDER))
        self.assertFalse(status(state)['ready_to_draft'])
        self.assertFalse((self.root / '.assets').exists())

    def test_out_of_order_gate_is_rejected(self):
        result = clear(self.root, 'fr', 'user confirmed FR')
        self.assertFalse(result['passed'])
        self.assertIn('macro', result['errors'][0])
        self.assertFalse(state_path(self.root).exists())

    def test_full_sequence_authorizes_drafting_and_delivery(self):
        self.assertTrue(clear(self.root, 'macro', 'user confirmed macro')['passed'])
        self.assertFalse(clear(self.root, 'scope', 'reported scope')['passed'])  # fr still pending
        self.assertTrue(clear(self.root, 'fr', 'user decided FR mechanism')['passed'])
        self.assertFalse(clear(self.root, 'scope', 'reported scope')['passed'])  # ux still pending
        self.assertTrue(clear(self.root, 'ux', 'user confirmed frames and states')['passed'])
        draft_ready = clear(self.root, 'scope', 'user confirmed scope and structure')
        self.assertTrue(draft_ready['passed'])
        self.assertEqual(draft_ready['state']['cleared'], ['macro', 'fr', 'ux', 'scope'])
        self.assertTrue(draft_ready['state']['ready_to_draft'])
        self.assertFalse(draft_ready['state']['ready_to_deliver'])
        self.assertEqual(draft_ready['state']['pending'], ['review'])

        final = clear(self.root, 'review', 'user confirmed downstream review and resolution')
        self.assertTrue(final['passed'])
        self.assertEqual(final['state']['cleared'], ['macro', 'fr', 'ux', 'scope', 'review'])
        self.assertTrue(final['state']['ready_to_draft'])
        self.assertTrue(final['state']['ready_to_deliver'])
        self.assertFalse(final['state']['pending'])

    def test_legacy_ledger_without_ux_gate_reports_it_pending(self):
        path = state_path(self.root)
        path.parent.mkdir(parents=True)
        path.write_text(json.dumps({'gates': {gate: {'at': '2026-01-01T00:00:00+08:00',
                                                     'evidence': 'older session'}
                                             for gate in ('macro', 'fr', 'scope')}}),
                        encoding='utf-8')
        state = status(load_state(self.root))
        self.assertFalse(state['ready_to_draft'])
        self.assertEqual(state['pending'], ['ux', 'review'])

    def test_waiver_records_the_user_shortcut(self):
        result = waive(self.root, 'user asked for a direct draft')
        self.assertTrue(result['passed'])
        self.assertTrue(result['state']['ready_to_draft'])
        self.assertTrue(result['state']['ready_to_deliver'])
        self.assertEqual(result['state']['waived']['evidence'], 'user asked for a direct draft')
        blocked = clear(self.root, 'macro', 'later confirmation')
        self.assertFalse(blocked['passed'])
        self.assertIn('--reset', blocked['errors'][0])

    def test_reset_starts_a_new_requirement(self):
        clear(self.root, 'macro', 'first requirement')
        result = reset(self.root, 'new requirement: QSELECT rework')
        self.assertTrue(result['passed'])
        self.assertEqual(result['state']['pending'], list(GATE_ORDER))
        self.assertIsNone(result['state']['waived'])

    def test_unknown_or_malformed_ledger_fails_closed(self):
        path = state_path(self.root)
        path.parent.mkdir(parents=True)
        path.write_text('{"gates": {"unknown": {}}}', encoding='utf-8')
        with self.assertRaises(ValueError):
            load_state(self.root)
        path.write_text('not json', encoding='utf-8')
        with self.assertRaises(ValueError):
            load_state(self.root)
        path.write_text('[]', encoding='utf-8')
        with self.assertRaises(ValueError):
            load_state(self.root)

    def test_cli_requires_evidence_and_supports_read(self):
        with patch('sys.stdout', new=io.StringIO()):
            self.assertEqual(main(['--workspace', str(self.root), '--clear', 'macro']), 1)
        self.assertFalse(state_path(self.root).exists())
        with patch('sys.stdout', new=io.StringIO()):
            self.assertEqual(main(['--workspace', str(self.root), '--read']), 0)
        self.assertFalse((self.root / '.assets').exists())

    def test_cli_writes_machine_readable_state(self):
        buffer = io.StringIO()
        with patch('sys.stdout', new=buffer):
            code = main(['--workspace', str(self.root), '--clear', 'macro',
                         '--evidence', 'user confirmed macro'])
        self.assertEqual(code, 0)
        self.assertTrue(json.loads(buffer.getvalue())['state']['cleared'], ['macro'])
        ledger = json.loads(state_path(self.root).read_text(encoding='utf-8'))
        self.assertEqual(ledger['gates']['macro']['evidence'], 'user confirmed macro')
        self.assertIn('updated', ledger)


if __name__ == '__main__':
    unittest.main()
