"""
test_engine.py - Unit tests for DojoEngine and Sandbox
"""
import unittest
import os
import sys

# Add project root to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from simulator.engine import DojoEngine
from simulator.sandbox import Sandbox
from simulator.db import ProgressDB

class TestDojoEngine(unittest.TestCase):
    def setUp(self):
        self.db = ProgressDB(db_path=":memory:")
        self.engine = DojoEngine(db=self.db)

    def test_load_challenges(self):
        challenges = self.engine.list_challenges()
        self.assertGreaterEqual(len(challenges), 60)
        grep_01 = self.engine.get_challenge("grep_01")
        self.assertIsNotNone(grep_01)
        self.assertEqual(grep_01["category"], "grep")

    def test_evaluate_grep_solution(self):
        res = self.engine.evaluate_solution("grep_02", "grep -c ERROR app.log")
        self.assertTrue(res["passed"])
        self.assertEqual(res["stdout"].strip(), "5")

    def test_evaluate_wrong_solution(self):
        res = self.engine.evaluate_solution("grep_02", "echo 99")
        self.assertFalse(res["passed"])

    def test_evaluate_awk_engineering(self):
        res = self.engine.evaluate_solution("awk_39", "awk -F, '$3==\"Engineering\" {sum += $4; n++} END {print sum/n}' employees.csv")
        self.assertTrue(res["passed"])
        self.assertEqual(res["stdout"].strip(), "5960")

    def test_sandbox_bash_timeout(self):
        with Sandbox() as sb:
            res = sb.run_bash("sleep 2", timeout=0.5)
            self.assertTrue(res["timed_out"])

if __name__ == "__main__":
    unittest.main()
