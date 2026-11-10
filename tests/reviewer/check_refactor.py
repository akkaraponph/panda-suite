#!/usr/bin/env python3
"""Reviewer-only checks; never copy this file into task-performing workspaces."""
import argparse
import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[2]


def check_target(folder, kind):
    # Separate process so service imports from previous cases cannot leak.
    spec = importlib.util.spec_from_file_location('subject', folder / 'service.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    if kind == 'labels':
        values = [' A ', 'a', '', ' B ', 'a']
        before = values[:]
        actual = module.normalize_labels(values)
        assert actual == ['a', 'a', 'b', 'a'], actual
        assert values == before, values
        assert actual is not values
    elif kind == 'greeting':
        class EffectfulName:
            def __str__(self):
                raise AssertionError('formatted before permission check')
        service = module.MessageService()
        for actor, expected in [({'role': 'member'}, PermissionError), ({}, KeyError)]:
            try:
                service.greet(actor, EffectfulName())
            except expected:
                pass
            else:
                raise AssertionError(f'missing {expected.__name__}')
        sys.path.insert(0, str(folder))
        from consumer import welcome
        assert welcome({'role': 'admin'}, 'Ada') == 'Hello, Ada'


def validate_fixtures():
    for name in ['small', 'green', 'conflict', 'effects', 'nochange', 'baseline']:
        folder = ROOT / 'tests/fixtures' / ('refactor-' + name)
        result = subprocess.run([sys.executable, '-B', '-m', 'unittest', '-v'],
                                cwd=folder, capture_output=True, text=True)
        expected = 1 if name == 'baseline' else 0
        assert result.returncode == expected, result.stdout + result.stderr
        print(f'{name}: supplied tests exit {result.returncode} (expected {expected})')
    for name, kind, expected in [('green', 'labels', 0), ('conflict', 'labels', 1),
                                 ('small', 'greeting', 0)]:
        result = subprocess.run([sys.executable, '-B', __file__, '--target',
                                 str(ROOT / 'tests/fixtures' / ('refactor-' + name)),
                                 '--kind', kind], capture_output=True, text=True)
        assert result.returncode == expected, result.stdout + result.stderr
        print(f'{name}: reviewer oracle exit {result.returncode} (expected {expected})')
    # Validate that the review fixture really exposes the guard-order regression.
    review = ROOT / 'tests/fixtures/refactor-review'
    for filename, expected in [('before.py', 0), ('after.py', 1)]:
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp)
            (folder / 'service.py').write_bytes((review / filename).read_bytes())
            (folder / 'consumer.py').write_bytes(
                (ROOT / 'tests/fixtures/refactor-small/consumer.py').read_bytes())
            result = subprocess.run([sys.executable, '-B', __file__, '--target', temp,
                                     '--kind', 'greeting'], capture_output=True, text=True)
            assert result.returncode == expected, result.stdout + result.stderr
            print(f'review {filename}: oracle exit {result.returncode} (expected {expected})')
    print('Fixture distinctions validated; model behavior was not evaluated.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--target', type=Path)
    parser.add_argument('--kind', choices=['labels', 'greeting'], default='labels')
    args = parser.parse_args()
    if args.target:
        check_target(args.target.resolve(), args.kind)
    else:
        validate_fixtures()
