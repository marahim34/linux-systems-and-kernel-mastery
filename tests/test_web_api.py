"""
test_web_api.py - Integration tests for HTTP REST endpoints
"""
import unittest
import os
import sys
import json
import urllib.request
import threading
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from web.server import run_server

class TestWebAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.port = 18889
        cls.server_thread = threading.Thread(target=run_server, kwargs={"port": cls.port}, daemon=True)
        cls.server_thread.start()
        time.sleep(0.5) # Allow server to bind

    def _get(self, path):
        url = f"http://127.0.0.1:{self.port}{path}"
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as resp:
            return resp.status, json.loads(resp.read().decode("utf-8"))

    def _post(self, path, payload):
        url = f"http://127.0.0.1:{self.port}{path}"
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req) as resp:
            return resp.status, json.loads(resp.read().decode("utf-8"))

    def test_get_status(self):
        status, data = self._get("/api/status")
        self.assertEqual(status, 200)
        self.assertIn("rank", data)
        self.assertIn("total_completed", data)

    def test_get_challenges(self):
        status, data = self._get("/api/challenges")
        self.assertEqual(status, 200)
        self.assertIn("challenges", data)
        self.assertGreaterEqual(len(data["challenges"]), 60)

    def test_verify_endpoint(self):
        status, data = self._post("/api/verify", {
            "challenge_id": "grep_06",
            "command": "grep -c ' 500 ' access.log"
        })
        self.assertEqual(status, 200)
        self.assertTrue(data["passed"])
        self.assertEqual(data["stdout"].strip(), "3")

    def test_sandbox_run_endpoint(self):
        status, data = self._post("/api/run", {
            "command": "echo 'Testing Sandbox API' | tr a-z A-Z"
        })
        self.assertEqual(status, 200)
        self.assertEqual(data["stdout"].strip(), "TESTING SANDBOX API")

    def test_practice_files_endpoint(self):
        status, data = self._get("/api/practice-files")
        self.assertEqual(status, 200)
        self.assertIn("access.log", data)
        self.assertIn("employees.csv", data)

    def test_curriculum_endpoint(self):
        status, data = self._get("/api/curriculum")
        self.assertEqual(status, 200)
        self.assertIn("tree", data)

if __name__ == "__main__":
    unittest.main()
