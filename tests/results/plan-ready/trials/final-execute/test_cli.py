import contextlib
import io
import json
from pathlib import Path
import tempfile
import unittest

from cli import main
from test_campaign import CountingTransport


class CliTest(unittest.TestCase):
    def test_cli_config_status_and_recovery_matrix(self):
        configs = [{}, {"legacyOption": "retained"},
                   {"requireAllGuardrailsProven": False},
                   {"requireAllGuardrailsProven": True}]
        outcomes = ["proven", "unproven", TimeoutError("timeout"),
                    InterruptedError("interrupted")]
        with tempfile.TemporaryDirectory() as directory:
            config_path = Path(directory) / "config.json"
            for config in configs:
                for outcome in outcomes:
                    with self.subTest(config=config, outcome=outcome):
                        config_text = json.dumps(config)
                        config_path.write_text(config_text)
                        transport = CountingTransport(outcome)
                        output = io.StringIO()
                        with contextlib.redirect_stdout(output):
                            code = main(str(config_path), transport)
                        lines = output.getvalue().splitlines()
                        self.assertEqual(1, len(lines))
                        report = json.loads(lines[0])
                        status = outcome if isinstance(outcome, str) else "unproven"
                        expected_code = (
                            2 if config.get("requireAllGuardrailsProven", False)
                            and status != "proven" else 0
                        )
                        self.assertEqual({
                            "schema_version": 1, "exit_code": expected_code,
                            "guardrails": [{"id": "safety", "status": status}],
                        }, report)
                        self.assertIs(type(code), int)
                        self.assertIs(type(report["exit_code"]), int)
                        self.assertEqual(expected_code, code)
                        self.assertEqual(report["exit_code"], code)
                        self.assertEqual(1, transport.calls)
                        self.assertEqual(config_text, config_path.read_text())

    def test_unrelated_exception_propagates_without_output(self):
        with tempfile.TemporaryDirectory() as directory:
            config_path = Path(directory) / "config.json"
            config_path.write_text("{}")
            error = RuntimeError("unrelated")
            transport = CountingTransport(error)
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                with self.assertRaises(RuntimeError) as caught:
                    main(str(config_path), transport)
            self.assertIs(error, caught.exception)
            self.assertEqual("", output.getvalue())
            self.assertEqual(1, transport.calls)
