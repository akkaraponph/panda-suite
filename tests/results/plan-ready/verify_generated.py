"""Trial-specific reviewer probe; never distributed to task agents.

Usage: python3 -B tests/results/plan-ready/verify_generated.py <execution-workspace>
The delivered policy helper is supplied so import failure does not hide the
original campaign orchestration defect. Actual failing assertions are captured.
"""
import io
from pathlib import Path
import runpy
import sys
import types
import unittest

workspace = Path(sys.argv[1]).resolve()
root = Path(__file__).resolve().parents[3]
faulty = runpy.run_path(str(root / 'tests/fixtures/plan-campaign/campaign.py'))
module = types.ModuleType('campaign')
module.__dict__.update(faulty)
module.evaluate_policy = runpy.run_path(str(workspace / 'campaign.py'))['evaluate_policy']
sys.modules['campaign'] = module
suite = runpy.run_path(str(workspace / 'test_campaign.py'))
stream = io.StringIO()
result = unittest.TextTestRunner(stream=stream).run(unittest.TestSuite([
    suite['CampaignIntegrationTest']('test_status_and_recovery_matrix')]))
assert not result.wasSuccessful(), 'delivered test missed faulty orchestration'
assert len(result.failures) == 1 and len(result.errors) == 6
print('EXPECTED FAILURE: delivered matrix rejects original strict-unproven exit 0 '
      '(1 assertion failure) and missing recovery (6 exception errors).')
print('The correct delivered implementation passes separately. This is a trial-specific '
      'effectiveness probe, not a model improvement benchmark.')
