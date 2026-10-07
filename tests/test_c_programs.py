"""
test_c_programs.py - Automated verification of C System Programming Suite
"""
import unittest
import os
import subprocess

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SYS_PROG_DIR = os.path.join(PROJECT_ROOT, "code_examples", "03_system_programming")

class TestCPrograms(unittest.TestCase):
    def test_build_and_run_all(self):
        res = subprocess.run(["make", "test"], cwd=SYS_PROG_DIR, capture_output=True, text=True)
        self.assertEqual(res.returncode, 0, f"Makefile test failed:\n{res.stderr}")
        self.assertIn("All system programming tests passed successfully!", res.stdout)

if __name__ == "__main__":
    unittest.main()
