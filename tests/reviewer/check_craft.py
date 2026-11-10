"""Reviewer-only discriminating check; never copied into task workspaces."""
from pathlib import Path
import runpy
import sys
import types
import unittest

ROOT = Path(__file__).resolve().parents[2]

def main():
    fixture = ROOT / 'tests/fixtures/craft-composition'
    faulty = runpy.run_path(str(fixture / 'service.py'))['normalize_labels']
    control = runpy.run_path(str(ROOT / 'tests/fixtures/contract-verification/correct_after.py'))['normalize_labels']
    for name, function in [('faulty', faulty), ('control', control)]:
        module = types.ModuleType('service')
        module.normalize_labels = function
        previous = sys.modules.get('service')
        sys.modules['service'] = module
        try:
            tests = runpy.run_path(str(fixture / 'test_service.py'))
            result = unittest.TextTestRunner(verbosity=1).run(
                unittest.defaultTestLoader.loadTestsFromTestCase(tests['NormalizeLabelsTest']))
            assert result.wasSuccessful(), name
        finally:
            if previous is None:
                sys.modules.pop('service', None)
            else:
                sys.modules['service'] = previous
        values = [' Alpha ', 'alpha', 'BETA', ' beta ', ' ']
        original = values.copy()
        actual = function(values)
        passes = actual == ['alpha', 'alpha', 'beta', 'beta']
        assert passes == (name == 'control'), (name, actual)
        assert values == original
        print(f'{name}: supplied_suite=PASS; duplicate_contract={"PASS" if passes else "FAIL (expected)"}')

if __name__ == '__main__':
    main()
