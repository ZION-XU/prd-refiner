#!/usr/bin/env python3
"""Read or record the PRD gate ledger at `<workspace>/.assets/gates.json`.

The four-stage gate is a user decision, never an inference: every write command
requires --evidence describing what the user actually confirmed. The ledger only
records order (macro -> fr -> scope -> review) and provenance; it cannot judge whether the
confirmed content is correct.
"""
from __future__ import annotations

import argparse
from datetime import datetime
import json
from pathlib import Path
import sys
import tempfile


GATE_ORDER = ('macro', 'fr', 'scope', 'review')
GATE_TITLES = {
    'macro': '宏观范围与目标确认门禁',
    'fr': '核心 FR 机制击穿门禁',
    'scope': '成稿范围与结构确认门禁',
    'review': '下游审查与消缺确认门禁',
}
PRE_DRAFT_GATES = ('macro', 'fr', 'scope')
STATE_NAME = 'gates.json'


def state_path(workspace: Path) -> Path:
    return Path(workspace).resolve() / '.assets' / STATE_NAME


def load_state(workspace: Path) -> dict:
    """Return the ledger, or an empty one when no gate has been recorded yet."""
    path = state_path(workspace)
    if not path.is_file():
        return {'gates': {}, 'waived': None}
    try:
        data = json.loads(path.read_text(encoding='utf-8-sig'))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ValueError(f'cannot read gate ledger: {type(exc).__name__}: {exc}')
    if not isinstance(data, dict) or not isinstance(data.get('gates'), dict):
        raise ValueError('malformed gate ledger: gates must be an object')
    if data.get('waived') is not None and not isinstance(data['waived'], dict):
        raise ValueError('malformed gate ledger: waived must be an object')
    unknown = sorted(set(data['gates']) - set(GATE_ORDER))
    if unknown:
        raise ValueError('unknown gate recorded: ' + ', '.join(unknown))
    return {'gates': {k: v for k, v in data['gates'].items()}, 'waived': data.get('waived')}


def status(state: dict) -> dict:
    pending = [gate for gate in GATE_ORDER if gate not in state['gates']]
    waived = state.get('waived')
    ready_to_draft = bool(waived) or all(gate in state['gates'] for gate in PRE_DRAFT_GATES)
    ready_to_deliver = bool(waived) or not pending
    return {
        'cleared': [gate for gate in GATE_ORDER if gate in state['gates']],
        'cleared_titles': {gate: GATE_TITLES[gate] for gate in GATE_ORDER if gate in state['gates']},
        'pending': pending,
        'pending_titles': {gate: GATE_TITLES[gate] for gate in pending},
        'waived': waived,
        'ready_to_draft': ready_to_draft,
        'ready_to_deliver': ready_to_deliver,
        'scope': 'Gate ledger only; it records what the user confirmed, not whether the content is correct.',
    }


def _write(workspace: Path, state: dict) -> Path:
    state['updated'] = datetime.now().astimezone().isoformat(timespec='seconds')
    path = state_path(workspace)
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile('w', encoding='utf-8', dir=path.parent,
                                     prefix='.gates-', suffix='.tmp', delete=False) as handle:
        json.dump(state, handle, ensure_ascii=False, indent=2)
        handle.write('\n')
        temporary = Path(handle.name)
    temporary.replace(path)
    return path


def clear(workspace: Path, gate: str, evidence: str) -> dict:
    """Record one confirmed gate; enforce that earlier gates are already recorded."""
    if gate not in GATE_ORDER:
        raise ValueError(f'unknown gate: {gate}; expected one of {", ".join(GATE_ORDER)}')
    state = load_state(workspace)
    if state.get('waived'):
        # The user shortcut already authorizes drafting; keep the ledger honest
        # instead of silently reordering recorded decisions.
        return {'passed': False, 'errors': ['gates were waived by the user; use --reset to start a new requirement'],
                'state': status(state)}
    missing = [earlier for earlier in GATE_ORDER[:GATE_ORDER.index(gate)] if earlier not in state['gates']]
    if missing:
        titles = '; '.join(f'{item}={GATE_TITLES[item]}' for item in missing)
        return {'passed': False,
                'errors': [f'cannot record {gate} before earlier gates: {titles}'],
                'state': status(state)}
    state['gates'][gate] = {
        'at': datetime.now().astimezone().isoformat(timespec='seconds'),
        'evidence': evidence,
    }
    path = _write(workspace, state)
    return {'passed': True, 'ledger': str(path), 'state': status(state)}


def waive(workspace: Path, evidence: str) -> dict:
    """Record the documented user shortcut: the user asked for a direct draft."""
    state = load_state(workspace)
    state['waived'] = {
        'at': datetime.now().astimezone().isoformat(timespec='seconds'),
        'evidence': evidence,
    }
    path = _write(workspace, state)
    return {'passed': True, 'ledger': str(path), 'state': status(state)}


def reset(workspace: Path, evidence: str) -> dict:
    """Clear the ledger inside one workspace; a new requirement uses a new workspace."""
    state = {'gates': {}, 'waived': None, 'reset': {
        'at': datetime.now().astimezone().isoformat(timespec='seconds'),
        'evidence': evidence,
    }}
    path = _write(workspace, state)
    return {'passed': True, 'ledger': str(path), 'state': status(state)}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description='Read or record the PRD gate ledger in <workspace>/.assets/gates.json')
    parser.add_argument('--workspace', required=True, type=Path,
                        help='Requirement workspace root (absolute path)')
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument('--read', action='store_true', help='Print the ledger status without writing')
    action.add_argument('--clear', choices=GATE_ORDER, metavar='GATE',
                        help='Record one confirmed gate (macro, fr, scope or review) in order')
    action.add_argument('--waive', action='store_true',
                        help='Record the user shortcut: the user asked for a direct draft')
    action.add_argument('--reset', action='store_true',
                        help='Discard the whole ledger in this workspace; only for revoking a waiver or correcting a misrecorded gate, not for continuing in a new session')
    parser.add_argument('--evidence', help='What the user actually confirmed; required for every write')
    args = parser.parse_args(argv)
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    try:
        if args.read:
            result = {'passed': True, 'ledger': str(state_path(args.workspace)),
                      'state': status(load_state(args.workspace))}
        else:
            if not (args.evidence or '').strip():
                raise ValueError('--evidence is required: record what the user actually confirmed')
            evidence = args.evidence.strip()
            if args.clear:
                result = clear(args.workspace, args.clear, evidence)
            elif args.waive:
                result = waive(args.workspace, evidence)
            else:
                result = reset(args.workspace, evidence)
    except (OSError, UnicodeError, ValueError) as exc:
        result = {'passed': False, 'errors': [f'{type(exc).__name__}: {exc}']}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result.get('passed') else 1


if __name__ == '__main__':
    raise SystemExit(main())
