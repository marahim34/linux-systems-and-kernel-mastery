"""
db.py - SQLite-backed persistent progress tracking and mastery badge engine
"""
import sqlite3
import os
import json
from datetime import datetime

DEFAULT_DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "simulator", "progress.db")

class ProgressDB:
    def __init__(self, db_path=DEFAULT_DB_PATH):
        self.db_path = db_path
        self._shared_conn = sqlite3.connect(":memory:") if db_path == ":memory:" else None
        self._init_db()

    def _get_conn(self):
        if self._shared_conn:
            return self._shared_conn
        return sqlite3.connect(self.db_path)

    def _init_db(self):
        if self.db_path != ":memory:" and os.path.dirname(self.db_path):
            os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        with self._get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS completed_challenges (
                challenge_id TEXT PRIMARY KEY,
                tier TEXT,
                category TEXT,
                completed_at TIMESTAMP,
                attempts INTEGER DEFAULT 1,
                user_solution TEXT
            )
            """)
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS execution_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                challenge_id TEXT,
                command TEXT,
                passed INTEGER,
                output TEXT,
                executed_at TIMESTAMP
            )
            """)
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_badges (
                badge_key TEXT PRIMARY KEY,
                name TEXT,
                description TEXT,
                awarded_at TIMESTAMP
            )
            """)
            conn.commit()

    def record_attempt(self, challenge_id, tier, category, command, passed, output):
        with self._get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            INSERT INTO execution_logs (challenge_id, command, passed, output, executed_at)
            VALUES (?, ?, ?, ?, ?)
            """, (challenge_id, command, 1 if passed else 0, output[:2000], datetime.now().isoformat()))

            if passed:
                cursor.execute("""
                INSERT INTO completed_challenges (challenge_id, tier, category, completed_at, attempts, user_solution)
                VALUES (?, ?, ?, ?, 1, ?)
                ON CONFLICT(challenge_id) DO UPDATE SET
                    completed_at = excluded.completed_at,
                    user_solution = excluded.user_solution,
                    attempts = attempts + 1
                """, (challenge_id, tier, category, datetime.now().isoformat(), command))

            conn.commit()
        if passed:
            self.check_and_award_badges()

    def get_completed_ids(self):
        with self._get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT challenge_id FROM completed_challenges")
            return {row[0] for row in cursor.fetchall()}

    def get_progress_summary(self, total_challenges_by_tier):
        with self._get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT tier, count(*) FROM completed_challenges GROUP BY tier")
            completed_by_tier = dict(cursor.fetchall())
            cursor.execute("SELECT count(*) FROM completed_challenges")
            total_completed = cursor.fetchone()[0]

            cursor.execute("SELECT badge_key, name, description, awarded_at FROM user_badges ORDER BY awarded_at")
            badges = [{"key": r[0], "name": r[1], "description": r[2], "awarded_at": r[3]} for r in cursor.fetchall()]

            # Determine Rank
            if total_completed >= 60:
                rank = "Kernel Subsystem Hacker (L4)"
            elif total_completed >= 45:
                rank = "Systems Programming Artisan (L3)"
            elif total_completed >= 25:
                rank = "Linux Operations Specialist (L2)"
            elif total_completed >= 10:
                rank = "Command Line Practitioner (L1)"
            else:
                rank = "Terminal Initiate (L0)"

            return {
                "total_completed": total_completed,
                "completed_by_tier": completed_by_tier,
                "rank": rank,
                "badges": badges
            }

    def check_and_award_badges(self):
        completed = self.get_completed_ids()
        badges_to_award = []

        grep_tasks = {f"grep_{i:02d}" for i in range(1, 16)}
        sed_tasks = {f"sed_{i:02d}" for i in range(16, 31)}
        awk_tasks = {f"awk_{i:02d}" for i in range(31, 51)}
        sys_prog = {f"sysprog_{i:02d}" for i in range(1, 7)}
        kernel_tasks = {f"kernel_{i:02d}" for i in range(1, 5)}

        if grep_tasks.issubset(completed):
            badges_to_award.append(("grep_master", "Grep Grandmaster", "Solved all 15 core grep challenges"))
        if sed_tasks.issubset(completed):
            badges_to_award.append(("sed_surgeon", "Sed Stream Surgeon", "Mastered stream editing across all 15 sed exercises"))
        if awk_tasks.issubset(completed):
            badges_to_award.append(("awk_alchemist", "Awk Alchemist", "Completed all 20 advanced field & aggregation challenges"))
        if len(completed) >= 50:
            badges_to_award.append(("trio_conqueror", "Text Processing Virtuoso", "Completed 50+ text processing exercises"))
        if any(c in completed for c in sys_prog):
            badges_to_award.append(("c_syscaller", "Syscall Sorcerer", "Successfully wrote and verified Linux C System Programs"))
        if any(c in completed for c in kernel_tasks):
            badges_to_award.append(("kernel_craftsman", "Kernel Subsystem Hacker", "Implemented and verified Linux Kernel Driver Modules"))

        with self._get_conn() as conn:
            cursor = conn.cursor()
            for b_key, b_name, b_desc in badges_to_award:
                cursor.execute("""
                INSERT OR IGNORE INTO user_badges (badge_key, name, description, awarded_at)
                VALUES (?, ?, ?, ?)
                """, (b_key, b_name, b_desc, datetime.now().isoformat()))
            conn.commit()

    def reset_progress(self):
        with self._get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM completed_challenges")
            cursor.execute("DELETE FROM execution_logs")
            cursor.execute("DELETE FROM user_badges")
            conn.commit()
