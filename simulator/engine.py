"""
engine.py - Grading and verification engine for practice challenges
"""
import os
import json
import time
from simulator.sandbox import Sandbox
from simulator.db import ProgressDB

CHALLENGES_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "challenges.json")

class DojoEngine:
    def __init__(self, db=None):
        self.db = db or ProgressDB()
        self.challenges = self._load_challenges()

    def _load_challenges(self):
        with open(CHALLENGES_FILE, "r") as f:
            data = json.load(f)
        return {item["id"]: item for item in data}

    def list_challenges(self, tier=None, category=None):
        completed = self.db.get_completed_ids()
        res = []
        for c in self.challenges.values():
            if tier and c.get("tier") != tier:
                continue
            if category and c.get("category") != category:
                continue
            item = dict(c)
            item["completed"] = c["id"] in completed
            res.append(item)
        return res

    def get_challenge(self, challenge_id):
        return self.challenges.get(challenge_id)

    def evaluate_solution(self, challenge_id, user_command):
        challenge = self.get_challenge(challenge_id)
        if not challenge:
            return {"passed": False, "message": f"Challenge '{challenge_id}' not found."}

        start_time = time.time()
        with Sandbox() as sandbox:
            res = sandbox.run_bash(user_command, timeout=12)
        exec_ms = (time.time() - start_time) * 1000

        stdout = res["stdout"]
        stderr = res["stderr"]
        returncode = res["returncode"]

        passed = True
        reasons = []

        if returncode != 0:
            passed = False
            reasons.append(f"Command exited with non-zero status code: {returncode}")

        # Check expected exact output
        if "expected_output" in challenge:
            clean_out = stdout.strip()
            expected = challenge["expected_output"].strip()
            if clean_out != expected:
                passed = False
                reasons.append(f"Expected exact output '{expected}', but received '{clean_out}'")

        # Check expected line count
        if "expected_lines" in challenge:
            lines = [l for l in stdout.splitlines() if l.strip()]
            if len(lines) != challenge["expected_lines"]:
                passed = False
                reasons.append(f"Expected {challenge['expected_lines']} lines of output, got {len(lines)}")

        # Check required substrings
        if "must_contain" in challenge:
            for needle in challenge["must_contain"]:
                if needle not in stdout:
                    passed = False
                    reasons.append(f"Output is missing required text: '{needle}'")

        # Check prohibited substrings
        if "must_not_contain" in challenge:
            for needle in challenge["must_not_contain"]:
                if needle in stdout:
                    passed = False
                    reasons.append(f"Output must not contain: '{needle}'")

        # Record attempt in SQLite database
        self.db.record_attempt(
            challenge_id=challenge["id"],
            tier=challenge.get("tier", "tier1"),
            category=challenge.get("category", "general"),
            command=user_command,
            passed=passed,
            output=stdout if passed else (stderr or stdout)
        )

        return {
            "challenge_id": challenge_id,
            "passed": passed,
            "stdout": stdout,
            "stderr": stderr,
            "reasons": reasons,
            "execution_ms": round(exec_ms, 2),
            "message": "Challenge passed! Excellent work." if passed else "Verification failed: " + "; ".join(reasons)
        }

    def get_progress(self):
        tier_counts = {}
        for c in self.challenges.values():
            t = c.get("tier", "tier1")
            tier_counts[t] = tier_counts.get(t, 0) + 1
        summary = self.db.get_progress_summary(tier_counts)
        summary["total_challenges"] = len(self.challenges)
        return summary
