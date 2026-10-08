"""
api/index.py - Vercel Serverless Function entrypoint for Linux Mastery Platform
Routes API requests using Python's BaseHTTPRequestHandler on AWS Lambda / Vercel Edge.
"""
import os
import sys
import json
from http.server import BaseHTTPRequestHandler

# Ensure project root is in sys.path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from simulator.engine import DojoEngine
from simulator.sandbox import Sandbox

# Singleton engine instance for serverless container reuse
engine = DojoEngine()
CURRICULUM_DIR = os.path.join(PROJECT_ROOT, "curriculum")
PRACTICE_DATA_DIR = os.path.join(PROJECT_ROOT, "practice_data")

class handler(BaseHTTPRequestHandler):
    def _send_json(self, data, status_code=200):
        body = json.dumps(data).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        self.wfile.write(body)

    def _read_json_body(self):
        content_len = int(self.headers.get("Content-Length", 0))
        if content_len == 0:
            return {}
        raw = self.rfile.read(content_len)
        return json.loads(raw.decode("utf-8"))

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        url = self.path.split("?")[0]
        if not url.startswith("/api"):
            url = "/api" + url

        if url == "/api/status":
            self._send_json(engine.get_progress())
            return

        if url == "/api/challenges":
            challenges = engine.list_challenges()
            self._send_json({"challenges": challenges})
            return

        if url.startswith("/api/challenges/"):
            c_id = url.replace("/api/challenges/", "")
            ch = engine.get_challenge(c_id)
            if ch:
                completed = c_id in engine.db.get_completed_ids()
                item = dict(ch)
                item["completed"] = completed
                self._send_json(item)
            else:
                self._send_json({"error": "Not found"}, 404)
            return

        if url == "/api/commands":
            c_file = os.path.join(PROJECT_ROOT, "simulator", "commands_reference.json")
            if os.path.exists(c_file):
                with open(c_file, "r") as f:
                    self._send_json(json.load(f))
            else:
                self._send_json([])
            return

        if url == "/api/interviews":
            i_file = os.path.join(PROJECT_ROOT, "simulator", "interview_questions.json")
            if os.path.exists(i_file):
                with open(i_file, "r") as f:
                    self._send_json(json.load(f))
            else:
                self._send_json([])
            return

        if url == "/api/practice-files":
            files = {}
            if os.path.exists(PRACTICE_DATA_DIR):
                for fname in sorted(os.listdir(PRACTICE_DATA_DIR)):
                    fpath = os.path.join(PRACTICE_DATA_DIR, fname)
                    if os.path.isfile(fpath):
                        with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                            files[fname] = f.read()
            self._send_json(files)
            return

        if url == "/api/curriculum":
            tree = {}
            if os.path.exists(CURRICULUM_DIR):
                for root, dirs, files in os.walk(CURRICULUM_DIR):
                    md_files = [f for f in sorted(files) if f.endswith(".md")]
                    if md_files:
                        rel = os.path.relpath(root, CURRICULUM_DIR)
                        tree[rel] = md_files
            self._send_json({"tree": tree})
            return

        if url.startswith("/api/curriculum/"):
            rel_path = url.replace("/api/curriculum/", "")
            file_path = os.path.join(CURRICULUM_DIR, rel_path)
            if os.path.exists(file_path) and os.path.isfile(file_path):
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                self._send_json({"path": rel_path, "content": content})
            else:
                self._send_json({"error": "File not found"}, 404)
            return

        self._send_json({"error": "Endpoint not found", "path": self.path}, 404)

    def do_POST(self):
        url = self.path.split("?")[0]
        if not url.startswith("/api"):
            url = "/api" + url

        if url == "/api/verify":
            payload = self._read_json_body()
            c_id = payload.get("challenge_id")
            cmd = payload.get("command", "")
            if not c_id or not cmd:
                self._send_json({"error": "Missing challenge_id or command"}, 400)
                return
            result = engine.evaluate_solution(c_id, cmd)
            self._send_json(result)
            return

        if url == "/api/run":
            payload = self._read_json_body()
            cmd = payload.get("command", "")
            if not cmd:
                self._send_json({"error": "Empty command"}, 400)
                return
            with Sandbox() as sandbox:
                run_res = sandbox.run_bash(cmd, timeout=10)
            self._send_json(run_res)
            return

        if url == "/api/reset":
            engine.db.reset_progress()
            self._send_json({"message": "Progress reset successfully", "status": engine.get_progress()})
            return

        self._send_json({"error": "Endpoint not found", "path": self.path}, 404)
