"""
cli.py - Command-Line Interface and Interactive Terminal Dojo
"""
import sys
import os
import argparse
from simulator.engine import DojoEngine

def print_banner():
    banner = r"""
  ╔═════════════════════════════════════════════════════════════════════════╗
  ║    __    _____ _   _ _   ___  __   __  __    _    ____ _____ _____ ____   ║
  ║   / /   |_   _| \ | | | | \ \/ /  |  \/  |  / \  / ___|_   _| ____|  _ \  ║
  ║  / /      | | |  \| | | | |\  /   | |\/| | / _ \ \___ \ | | |  _| | |_) | ║
  ║  \ \      | | | |\  | |_| |/  \   | |  | |/ ___ \ ___) || | | |___|  _ <  ║
  ║   \_\     |_| |_| \_|\___//_/\_\  |_|  |_/_/   \_\____/ |_| |_____|_| \_\ ║
  ║                                                                         ║
  ║     LINUX MASTERY ENGINE: FROM ZERO COMMAND TO KERNEL HACKER           ║
  ║            Interactive Dojo · Built for MD Abdur Rahim                  ║
  ╚═════════════════════════════════════════════════════════════════════════╝
    """
    print(banner)

def main():
    parser = argparse.ArgumentParser(
        prog="linux-mastery",
        description="Linux Mastery Platform: Core, Bash, Sysadmin, C Systems Programming, and Kernel Modules"
    )
    subparsers = parser.add_subparsers(dest="command")

    # list
    list_p = subparsers.add_parser("list", help="List all practice challenges")
    list_p.add_argument("--tier", choices=["tier1", "tier2", "tier3", "tier4"], help="Filter by tier")
    list_p.add_argument("--cat", help="Filter by category (grep, sed, awk, combo, c_systems, kernel)")

    # show
    show_p = subparsers.add_parser("show", help="Show challenge instructions and details")
    show_p.add_argument("challenge_id", help="Challenge ID (e.g., grep_01, awk_39, kernel_01)")

    # run
    run_p = subparsers.add_parser("run", help="Submit and verify a challenge solution")
    run_p.add_argument("challenge_id", help="Challenge ID")
    run_p.add_argument("user_command", help="The bash/sh command line solution to evaluate")

    # hint
    hint_p = subparsers.add_parser("hint", help="View hint for a challenge")
    hint_p.add_argument("challenge_id", help="Challenge ID")

    # solution
    sol_p = subparsers.add_parser("solution", help="Reveal reference solution for a challenge")
    sol_p.add_argument("challenge_id", help="Challenge ID")

    # status
    subparsers.add_parser("status", help="View your learning progress and mastery rank")

    # test-all
    subparsers.add_parser("test-all", help="Run automated test suite verifying all reference solutions")

    # web
    web_p = subparsers.add_parser("web", help="Launch interactive Web GUI application")
    web_p.add_argument("--port", type=int, default=8080, help="Web server port (default: 8080)")

    args = parser.parse_args()
    engine = DojoEngine()

    if not args.command:
        print_banner()
        progress = engine.get_progress()
        print(f"  Current Rank       : \033[1;32m{progress['rank']}\033[0m")
        print(f"  Progress           : {progress['total_completed']} / {progress['total_challenges']} challenges solved")
        print(f"  Badges Earned      : {len(progress['badges'])}")
        print("\nCommands:")
        print("  ./linux-mastery list             - List all available challenges")
        print("  ./linux-mastery show <id>        - View instructions for a challenge")
        print("  ./linux-mastery run <id> '<cmd>' - Submit solution for verification")
        print("  ./linux-mastery hint <id>        - Get a hint")
        print("  ./linux-mastery solution <id>    - Reveal solution")
        print("  ./linux-mastery status           - View full mastery dashboard")
        print("  ./linux-mastery web              - Launch interactive browser UI")
        print()
        return

    if args.command == "list":
        items = engine.list_challenges(tier=args.tier, category=args.cat)
        print("\n" + "=" * 80)
        print(f"{'STATUS':<8} {'ID':<14} {'TIER':<10} {'CATEGORY':<12} {'TITLE'}")
        print("=" * 80)
        for item in items:
            status = "\033[32m[✓]\033[0m" if item["completed"] else "\033[90m[ ]\033[0m"
            print(f"{status:<17} {item['id']:<14} {item.get('tier',''):<10} {item.get('category',''):<12} {item['title']}")
        print("=" * 80)
        print(f"Total: {len(items)} challenges. Use './linux-mastery show <id>' to inspect a challenge.\n")

    elif args.command == "show":
        c = engine.get_challenge(args.challenge_id)
        if not c:
            print(f"Error: Challenge '{args.challenge_id}' not found.")
            return
        print("\n" + "=" * 70)
        print(f"CHALLENGE: {c['id']} - {c['title']} ({c.get('tier','').upper()})")
        print("=" * 70)
        print(f"Category    : {c.get('category','')}")
        print(f"Description : {c['description']}")
        print(f"\nPractice Files Available in Workspace:")
        print("  access.log, app.log, employees.csv, server.conf, users.txt")
        print("\nTo submit your solution:")
        print(f"  ./linux-mastery run {c['id']} \"<your_command_here>\"")
        print(f"To see hint: ./linux-mastery hint {c['id']}")
        print("=" * 70 + "\n")

    elif args.command == "run":
        res = engine.evaluate_solution(args.challenge_id, args.user_command)
        print("\n" + "=" * 70)
        if res["passed"]:
            print(f"\033[1;32m✓ PASSED!\033[0m Execution time: {res['execution_ms']}ms")
            print("=" * 70)
            if res["stdout"].strip():
                print("OUTPUT:")
                print(res["stdout"].strip())
        else:
            print(f"\033[1;31m✗ FAILED\033[0m Execution time: {res['execution_ms']}ms")
            print("=" * 70)
            print("Reasons:")
            for r in res.get("reasons", []):
                print(f"  - {r}")
            if res["stdout"].strip():
                print("\nYour STDOUT:\n" + res["stdout"].strip())
            if res["stderr"].strip():
                print("\nYour STDERR:\n" + res["stderr"].strip())
        print("=" * 70 + "\n")

    elif args.command == "hint":
        c = engine.get_challenge(args.challenge_id)
        if not c:
            print(f"Error: Challenge '{args.challenge_id}' not found.")
            return
        print(f"\n[HINT for {c['id']}]: {c.get('hint', 'No hint provided.')}\n")

    elif args.command == "solution":
        c = engine.get_challenge(args.challenge_id)
        if not c:
            print(f"Error: Challenge '{args.challenge_id}' not found.")
            return
        print(f"\n[REFERENCE SOLUTION for {c['id']}]:\n  {c.get('solution')}\n")

    elif args.command == "status":
        p = engine.get_progress()
        print("\n" + "=" * 65)
        print("             LINUX MASTERY STATUS & PROGRESS")
        print("=" * 65)
        print(f"  Mastery Rank       : \033[1;32m{p['rank']}\033[0m")
        print(f"  Solved Challenges  : {p['total_completed']} / {p['total_challenges']}")
        print("\n  Tier Breakdown:")
        for t, count in p.get("completed_by_tier", {}).items():
            print(f"    - {t.upper():<10} : {count} completed")
        print("\n  Badges Awarded:")
        if p["badges"]:
            for b in p["badges"]:
                print(f"    - \033[1;33m🏆 {b['name']}\033[0m: {b['description']}")
        else:
            print("    (Complete exercises to unlock mastery badges!)")
        print("=" * 65 + "\n")

    elif args.command == "test-all":
        items = engine.list_challenges()
        print(f"\nExecuting verification run across {len(items)} challenges...")
        passed = 0
        for it in items:
            res = engine.evaluate_solution(it["id"], it["solution"])
            if res["passed"]:
                passed += 1
                sys.stdout.write(".")
            else:
                sys.stdout.write("F")
            sys.stdout.flush()
        print(f"\n\nResults: {passed} / {len(items)} challenges verified successfully!\n")

    elif args.command == "web":
        from web.server import run_server
        run_server(port=args.port)

if __name__ == "__main__":
    main()
