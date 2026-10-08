"""
sandbox.py - Sandboxed Execution Environment for Bash, C, and Kernel Drivers
"""
import os
import shutil
import tempfile
import subprocess

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PRACTICE_DATA_DIR = os.path.join(PROJECT_ROOT, "practice_data")

class Sandbox:
    def __init__(self, keep_dir=False):
        self.keep_dir = keep_dir
        self.temp_dir = tempfile.mkdtemp(prefix="dojo_sandbox_")
        self._setup_environment()

    def _setup_environment(self):
        # Copy practice files so user mutations don't alter master files
        if os.path.exists(PRACTICE_DATA_DIR):
            for fname in os.listdir(PRACTICE_DATA_DIR):
                src = os.path.join(PRACTICE_DATA_DIR, fname)
                if os.path.isfile(src):
                    shutil.copy2(src, os.path.join(self.temp_dir, fname))
        # Symlink code_examples so C and Kernel challenges can compile code
        code_ex = os.path.join(PROJECT_ROOT, "code_examples")
        if os.path.exists(code_ex):
            try:
                os.symlink(code_ex, os.path.join(self.temp_dir, "code_examples"))
            except OSError:
                pass

    def run_bash(self, command, timeout=10):
        try:
            res = subprocess.run(
                ["bash", "-c", command],
                cwd=self.temp_dir,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            return {
                "stdout": res.stdout,
                "stderr": res.stderr,
                "returncode": res.returncode,
                "timed_out": False
            }
        except subprocess.TimeoutExpired:
            return {
                "stdout": "",
                "stderr": f"Command timed out after {timeout} seconds.",
                "returncode": -1,
                "timed_out": True
            }
        except Exception as e:
            return {
                "stdout": "",
                "stderr": str(e),
                "returncode": -1,
                "timed_out": False
            }

    def compile_and_run_c(self, c_code, extra_flags=None, timeout=10):
        c_file = os.path.join(self.temp_dir, "solution.c")
        bin_file = os.path.join(self.temp_dir, "solution_bin")
        with open(c_file, "w") as f:
            f.write(c_code)

        flags = ["-Wall", "-Wextra", "-pthread", "-O2"]
        if extra_flags:
            flags.extend(extra_flags)

        compile_cmd = ["gcc"] + flags + [c_file, "-o", bin_file]
        try:
            comp_res = subprocess.run(compile_cmd, cwd=self.temp_dir, capture_output=True, text=True)
            if comp_res.returncode != 0:
                return {
                    "stdout": "",
                    "stderr": "Compilation Error:\n" + comp_res.stderr,
                    "returncode": comp_res.returncode,
                    "compiled": False
                }
        except FileNotFoundError:
            return {
                "stdout": "",
                "stderr": "Note: GCC compiler is not available in cloud serverless environment. Run locally on Linux via './linux-mastery' for full C and Kernel compilation.",
                "returncode": 1,
                "compiled": False
            }

        try:
            run_res = subprocess.run([bin_file], cwd=self.temp_dir, capture_output=True, text=True, timeout=timeout)
            return {
                "stdout": run_res.stdout,
                "stderr": run_res.stderr,
                "returncode": run_res.returncode,
                "compiled": True,
                "timed_out": False
            }
        except subprocess.TimeoutExpired:
            return {
                "stdout": "",
                "stderr": f"Program execution timed out after {timeout} seconds.",
                "returncode": -1,
                "compiled": True,
                "timed_out": True
            }

    def cleanup(self):
        if not self.keep_dir and os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir, ignore_errors=True)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cleanup()
