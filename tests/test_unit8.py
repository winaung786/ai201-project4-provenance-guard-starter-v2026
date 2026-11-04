"""Focused Unit 8 checks that do not download the detector model.

The route checks replace only signal one with a fixed score. They verify
request handling, rate limiting, and audit behavior, not detector accuracy.
"""

import argparse
import contextlib
import io
import sys
import tempfile
import types
import unittest
from pathlib import Path
from unittest import mock

import audit
import config
import run_attacks


class AttackHarnessTests(unittest.TestCase):
    def test_large_csv_field_is_loaded_without_truncation(self):
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp)
            body = "word " * 40_000
            (folder / "attacks.csv").write_text(
                "id,family,targets,text\nBIG,malformed,large body,\""
                + body + "\"\n",
                encoding="utf-8",
            )
            attacks, problems = run_attacks.load_attacks(folder)
            self.assertEqual(problems, [])
            self.assertEqual(len(attacks), 1)
            self.assertEqual(attacks[0]["body"]["text"], body)

    def test_parse_gap_aborts_before_any_requests(self):
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp)
            (folder / "attacks.csv").write_text(
                "id,family,targets\nA,evasion,missing text\n", encoding="utf-8"
            )
            with mock.patch.object(sys, "argv", ["run_attacks.py", "--set", temp, "--show"]):
                with contextlib.redirect_stderr(io.StringIO()) as stderr:
                    with self.assertRaises(SystemExit) as stopped:
                        run_attacks.main()
            self.assertEqual(stopped.exception.code, 1)
            self.assertIn("No requests sent", stderr.getvalue())

    def test_show_accepts_non_object_json_body(self):
        attack = {"id": "LIST", "family": "malformed", "targets": "list body", "body": [1, 2]}
        with contextlib.redirect_stdout(io.StringIO()) as output:
            run_attacks.show_attacks([attack], "http://127.0.0.1:5000")
        self.assertIn("[1, 2]", output.getvalue())

    def test_report_separates_combined_score_and_confidence(self):
        with tempfile.TemporaryDirectory() as temp:
            row = {
                "id": "A", "family": "evasion", "targets": "target", "status": 200,
                "content_id": "one", "creator_id": "attacker_A", "guess": "ai",
                "combined_score": 0.61575, "confidence": 0.2315,
                "model_score": 0.8063, "style_score": 0.4252,
                "label": "example", "error": None, "verdict": "", "note": "",
            }
            with mock.patch.object(config, "RESULTS_DIR", Path(temp)), \
                 mock.patch.object(config, "ROOT", Path(temp)):
                with contextlib.redirect_stdout(io.StringIO()):
                    run_attacks.write_report([row], argparse.Namespace(label="check"))
            report = next(Path(temp).glob("attack_run_*_check.md")).read_text(encoding="utf-8")
            self.assertIn("| Combined score | Confidence | Verdict |", report)
            self.assertIn("| ai | 0.616 | 0.232 |", report)
            self.assertIn('"combined_score": 0.61575', report)


class RouteChecks(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        folder = Path(self.temp.name)
        self.patches = [
            mock.patch.object(config, "LOG_DIR", folder),
            mock.patch.object(config, "AUDIT_LOG", folder / "audit.jsonl"),
            mock.patch.dict(
                sys.modules,
                {"detector": types.SimpleNamespace(
                    model_signal=lambda text: 0.8,
                    DetectorUnavailable=type("DetectorUnavailable", (Exception,), {}),
                )},
            ),
        ]
        for patcher in self.patches:
            patcher.start()
            self.addCleanup(patcher.stop)
        import app
        self.client = app.app.test_client()

    def test_three_appeals_keep_original_decisions_and_unknown_is_404(self):
        for trial in range(3):
            response = self.client.post(
                "/submit",
                json={"creator_id": f"appeal_check_{trial}",
                      "text": "This is a complete test paragraph with several words."},
            )
            self.assertEqual(response.status_code, 200)
            content_id = response.get_json()["content_id"]
            original = audit.entries_for(content_id)[0].copy()
            self.assertTrue({
                "timestamp", "content_id", "creator_id", "guess", "model_score",
                "style_score", "combined_score", "label", "status",
            }.issubset(original))
            appeal = self.client.post(
                "/appeal", json={"content_id": content_id, "reasoning": "Please review."}
            )
            self.assertEqual(appeal.status_code, 200)
            self.assertEqual(appeal.get_json()["status"], "under_review")
            entries = audit.entries_for(content_id)
            self.assertEqual(len(entries), 2)
            self.assertEqual(entries[0], original)
            self.assertEqual(entries[1]["status"], "under_review")
            self.assertEqual(entries[1]["event"], "appeal")
            self.assertEqual(
                self.client.post("/appeal", json={"content_id": f"unknown_{trial}"}).status_code,
                404,
            )

    def test_bad_inputs_are_4xx_and_audited(self):
        bodies = [
            {"creator_id": "bad_empty", "text": ""},
            {"creator_id": "bad_missing"},
            {"creator_id": "bad_null", "text": None},
            {"creator_id": "bad_huge", "text": "x" * (config.MAX_TEXT_CHARS + 1)},
        ]
        for body in bodies:
            response = self.client.post("/submit", json=body)
            self.assertEqual(response.status_code, 400)
        rejections = [e for e in audit.read_entries() if e.get("event") == "rejected"]
        self.assertEqual(len(rejections), 4)
        self.assertEqual(
            {e["reason"] for e in rejections},
            {"empty_text", "invalid_text", "text_too_long"},
        )

    def test_fifteen_same_creator_requests_produce_five_429s(self):
        codes = [self.client.post(
            "/submit",
            json={"creator_id": "flood_check", "text": "A complete test paragraph with enough words."},
        ).status_code for _ in range(15)]
        self.assertEqual(codes, [200] * 10 + [429] * 5)
        rejections = [e for e in audit.read_entries()
                      if e.get("reason") == "rate_limited"]
        self.assertEqual(len(rejections), 5)


if __name__ == "__main__":
    unittest.main()
