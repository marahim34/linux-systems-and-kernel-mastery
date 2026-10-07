# 🐧 Linux Mastery: From Zero Command to Kernel Hacker

[![Platform](https://img.shields.io/badge/Platform-Linux%20Ubuntu%2024.04%20LTS-orange.svg)]()
[![Kernel](https://img.shields.io/badge/Kernel-7.0.0-blue.svg)]()
[![C-Standard](https://img.shields.io/badge/Standard-GNU11%20%7C%20POSIX.1--2008-brightgreen.svg)]()
[![Dependencies](https://img.shields.io/badge/Dependencies-Zero%20External-success.svg)]()
[![Tests](https://img.shields.io/badge/Tests-Passing%20(107%2F107)-green.svg)]()

> **The Ultimate Linux Systems Engineering & Kernel Development Platform**  
> Specially prepared for **MD Abdur Rahim** · Tampere, Finland · 2026  
> Synthesizing 20 canonical Linux texts, 9-volume mastery series, *The Linux Programming Interface* (Michael Kerrisk), *Linux Kernel Development* (Robert Love), and *Understanding the Linux Kernel* (Bovet & Cesati).

---

## 🏛️ System Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       LINUX MASTERY ECOSYSTEM                               │
└─────────────────────────────────────────────────────────────────────────────┘
          │                                                  │
          ▼                                                  ▼
┌────────────────────────────────┐         ┌──────────────────────────────────┐
│      INTERACTIVE CLI / TUI     │         │       CYBER-DARK WEB APP         │
│  ./linux-mastery list/run/web  │         │  http://localhost:8080 (REST)    │
└────────────────┬───────────────┘         └─────────────────┬────────────────┘
                 │                                           │
                 └─────────────────────┬─────────────────────┘
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                      SIMULATOR & GRADING ENGINE                             │
│  Isolated Sandbox · Timeout Guards · Strict Testing · SQLite Progress DB   │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │
         ┌─────────────────────────────┼─────────────────────────────┐
         ▼                             ▼                             ▼
┌──────────────────┐         ┌───────────────────┐         ┌──────────────────┐
│  TIER 1 & 2:     │         │  TIER 3:          │         │  TIER 4:         │
│  Bash, FHS, Sudo │         │  C Systems Code   │         │  Kernel Modules  │
│  Grep/Sed/Awk    │         │  Syscalls, epoll  │         │  Char Drivers    │
│  50 Graded Tasks │         │  Pthreads, IPC    │         │  Mock K-Harness  │
└──────────────────┘         └───────────────────┘         └──────────────────┘
```

---

## 🌟 Key Features

1. **Complete 4-Tier Master Curriculum**:
   - **Tier 1 (Foundations & Shell Craft)**: File streams, redirections, FHS 3.0 hierarchy, user/group/shadow databases, sudoers grammar, and bash scripting strict mode.
   - **Tier 2 (Systems Administration & DevOps)**: Storage (LVM, software RAID mdadm, LUKS encryption), advanced networking, systemd unit architecture, cgroups v2, and security auditing with auditd.
   - **Tier 3 (Advanced Linux System Programming in C)**: Direct syscalls (`open`, `read`, `write`, `lseek`), process trees (`fork`, `execve`, `waitpid`), robust signal handling (`sigaction`, `SA_SIGINFO`), POSIX thread pools (`pthread_mutex_t`, `pthread_cond_t`), IPC (`pipe`, POSIX shared memory, semaphores, UNIX domain sockets), memory-mapped files (`mmap`), and high-performance event loops (`epoll`).
   - **Tier 4 (Linux Kernel Programming & Subsystems)**: Loadable Kernel Modules (LKMs), character device drivers (`cdev`, `file_operations`), user-kernel memory isolation (`copy_to_user`, `copy_from_user`), concurrency (`spinlock_t`, `mutex`, RCU), bottom-half workqueues, and `/proc` virtual files.
2. **50 Graded Text-Processing Tasks with Real Practice Datasets**:
   - `access.log` (Apache webserver log)
   - `app.log` (Application log with ERROR, WARN, INFO)
   - `employees.csv` (10 employee records with salaries, departments, cities)
   - `server.conf` (Production configuration with comments & blanks)
   - `users.txt` (Passwd-style user database)
3. **Safe User-Space Kernel Simulator Harness**:
   - Compiles and tests kernel drivers with standard `gcc` without requiring root permissions or risking kernel panics.
4. **Zero External Dependencies**:
   - Built entirely on Python 3 standard library (`http.server`, `sqlite3`, `subprocess`, `urllib`) and GCC. No `pip install`, no `npm`, no setup headaches.

---

## 🚀 Quick Start

### 1. Launch the Interactive Web Platform
```bash
./linux-mastery web --port 8080
# Open http://localhost:8080 in your browser
```

### 2. Practice Challenges via the Command-Line Dojo
```bash
# View dashboard & mastery rank
./linux-mastery

# List challenges by category
./linux-mastery list --cat grep
./linux-mastery list --cat awk
./linux-mastery list --cat c_systems
./linux-mastery list --cat kernel

# Inspect a challenge
./linux-mastery show grep_02

# Run and grade your solution
./linux-mastery run grep_02 "grep -c ERROR app.log"

# Ask for a hint or reveal reference solution
./linux-mastery hint grep_02
./linux-mastery solution grep_02

# View progress & earned badges
./linux-mastery status
```

### 3. Build & Test C System Programming Suite
```bash
make -C code_examples/03_system_programming test
```

### 4. Run the Safe Kernel Driver Simulator
```bash
make -C code_examples/04_kernel_modules test
```

### 5. Execute Full Platform Verification Suite
```bash
make test
```

---

## 📚 Curriculum Library Overview

| Tier | Topic | Guide Path |
|---|---|---|
| **Tier 1** | Shell & Redirections | [`curriculum/tier1_core_and_bash/01_terminal_and_shell_foundations.md`](curriculum/tier1_core_and_bash/01_terminal_and_shell_foundations.md) |
| **Tier 1** | Filesystem Hierarchy (FHS) | [`curriculum/tier1_core_and_bash/02_fhs_filesystem_hierarchy.md`](curriculum/tier1_core_and_bash/02_fhs_filesystem_hierarchy.md) |
| **Tier 1** | Permissions & ACLs | [`curriculum/tier1_core_and_bash/03_permissions_ownership_acls.md`](curriculum/tier1_core_and_bash/03_permissions_ownership_acls.md) |
| **Tier 1** | Users & Groups | [`curriculum/tier1_core_and_bash/04_user_group_management.md`](curriculum/tier1_core_and_bash/04_user_group_management.md) |
| **Tier 1** | Sudo & Privilege | [`curriculum/tier1_core_and_bash/05_sudo_and_privilege.md`](curriculum/tier1_core_and_bash/05_sudo_and_privilege.md) |
| **Tier 1** | Grep, Sed & Awk (50 Ex) | [`curriculum/tier1_core_and_bash/06_grep_sed_awk_complete_handbook.md`](curriculum/tier1_core_and_bash/06_grep_sed_awk_complete_handbook.md) |
| **Tier 2** | Storage (LVM/RAID/LUKS) | [`curriculum/tier2_system_administration/01_storage_lvm_raid_luks.md`](curriculum/tier2_system_administration/01_storage_lvm_raid_luks.md) |
| **Tier 2** | Systemd & Services | [`curriculum/tier2_system_administration/02_systemd_and_services.md`](curriculum/tier2_system_administration/02_systemd_and_services.md) |
| **Tier 3** | Syscalls & Direct File I/O | [`curriculum/tier3_system_programming_c/01_system_calls_and_file_io.md`](curriculum/tier3_system_programming_c/01_system_calls_and_file_io.md) |
| **Tier 3** | Processes & Pthreads | [`curriculum/tier3_system_programming_c/02_processes_and_threads.md`](curriculum/tier3_system_programming_c/02_processes_and_threads.md) |
| **Tier 3** | High-Performance epoll | [`curriculum/tier3_system_programming_c/03_epoll_and_event_loops.md`](curriculum/tier3_system_programming_c/03_epoll_and_event_loops.md) |
| **Tier 4** | Kernel Architecture | [`curriculum/tier4_kernel_programming/01_kernel_architecture_and_tour.md`](curriculum/tier4_kernel_programming/01_kernel_architecture_and_tour.md) |
| **Tier 4** | Loadable Kernel Modules | [`curriculum/tier4_kernel_programming/02_loadable_kernel_modules.md`](curriculum/tier4_kernel_programming/02_loadable_kernel_modules.md) |
| **Tier 4** | Character Device Drivers | [`curriculum/tier4_kernel_programming/03_character_device_drivers.md`](curriculum/tier4_kernel_programming/03_character_device_drivers.md) |
| **Tier 4** | Kernel Concurrency & RCU | [`curriculum/tier4_kernel_programming/04_kernel_concurrency_and_rcu.md`](curriculum/tier4_kernel_programming/04_kernel_concurrency_and_rcu.md) |

---

## 🏆 Mastery Badges System

- 🔍 **Grep Grandmaster**: Solve all 15 core grep challenges
- ✂️ **Sed Stream Surgeon**: Master stream editing across all 15 sed exercises
- ⚗️ **Awk Alchemist**: Complete all 20 advanced field & aggregation challenges
- 🧙‍♂️ **Text Processing Virtuoso**: Conquer all 50 text processing exercises + bonus combos
- ⚡ **Syscall Sorcerer**: Write and verify Linux C System Programs
- 🐧 **Kernel Subsystem Hacker**: Implement and verify Linux Kernel Driver Modules

---

## 📂 Project Directory Structure

```
├── .gitignore
├── README.md
├── Makefile
├── linux-mastery                      # Interactive CLI executable
├── curriculum/                        # Comprehensive Markdown study series
├── practice_data/                     # 5 sample files for grep, sed, awk exercises
├── code_examples/
│   ├── 01_bash_scripts/               # Production bash administration scripts
│   ├── 02_text_processing/            # Complete 50 grep/sed/awk solutions
│   ├── 03_system_programming/         # Compilable C syscall/epoll programs + Makefile
│   └── 04_kernel_modules/             # Real LKMs + user-space mock simulator
├── simulator/                         # Python grading engine, SQLite DB, CLI
├── web/                               # Interactive Web Platform (HTML5/CSS3/Vanilla JS)
└── tests/                             # Automated test suite (Python unittest + C Make)
```

---

## 📜 Dedication & License
Designed and engineered for **MD Abdur Rahim** as a permanent, production-ready operating system dojo.  
Released under the MIT License.
