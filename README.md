# 🐧 Linux Mastery University: Zero to Kernel Hacker

[![Platform](https://img.shields.io/badge/Platform-Linux%20Ubuntu%2024.04%20LTS-orange.svg)]()
[![Kernel](https://img.shields.io/badge/Kernel-7.0.0-blue.svg)]()
[![Curriculum](https://img.shields.io/badge/Curriculum-536%20Chapters-purple.svg)]()
[![Challenges](https://img.shields.io/badge/Labs-107%20Interactive%20Labs-success.svg)]()
[![C-Standard](https://img.shields.io/badge/Standard-GNU11%20%7C%20POSIX.1--2008-brightgreen.svg)]()
[![Dependencies](https://img.shields.io/badge/Dependencies-Zero%20External-success.svg)]()
[![Tests](https://img.shields.io/badge/Tests-Passing%20(107%2F107)-green.svg)]()

> **The Definitive Linux Systems Engineering, Architecture & Kernel Development Platform**  
> Specially prepared for **MD Abdur Rahim** · Tampere, Finland · 2026  
> Synthesizing all **9 Volumes of the Linux Mastery Series**, Michael Kerrisk's *The Linux Programming Interface* (TLPI - 1556 pages), Robert Love's *Linux Kernel Development* (LKD), Bovet & Cesati's *Understanding the Linux Kernel* (ULK3), and the complete TAMK (Tampere University of Applied Sciences) Practice Guides.

---

## 🏛️ System Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                   LINUX MASTERY UNIVERSITY ECOSYSTEM                        │
└─────────────────────────────────────────────────────────────────────────────┘
          │                                                  │
          ▼                                                  ▼
┌────────────────────────────────┐         ┌──────────────────────────────────┐
│      INTERACTIVE CLI / TUI     │         │    FULL-FEATURED SINGLE PAGE APP │
│  ./linux-mastery list/run/web  │         │  http://localhost:8080 (REST)    │
└────────────────┬───────────────┘         └─────────────────┬────────────────┘
                 │                                           │
                 └─────────────────────┬─────────────────────┘
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                    ZERO-DEPENDENCY BACKEND & RUNTIME                        │
│  Python 3 ThreadingHTTPServer · Isolated Subprocess Sandbox · SQLite DB     │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │
     ┌───────────────────┬─────────────┴───────┬───────────────────┐
     ▼                   ▼                     ▼                   ▼
┌──────────────┐   ┌───────────────┐     ┌───────────────┐   ┌────────────────┐
│ 536 CHAPTER  │   │ 107 GRADED    │     │ 55 COMMANDS & │   │ KERNEL DRIVER  │
│ KNOWLEDGE    │   │ INTERACTIVE   │     │ INTERVIEW     │   │ & C SYSPROG    │
│ LIBRARY      │   │ DOJO LABS     │     │ PREP DOJO     │   │ HARNESSES      │
└──────────────┘   └───────────────┘     └───────────────┘   └────────────────┘
```

---

## 🌟 Key Features & Platform Modules

### 1. 📚 9-Volume Curriculum & Canonical Reference Library (536 Markdown Chapters)
Extracted, curated, and indexed into a searchable interactive tree viewer:
- **Volume 01: The Ultimate Edition (151 chapters)**: Terminal survival, filesystem hierarchy, Vim mastery, processes, networking, bash scripting, permissions, and production deployments.
- **Volume 02: Specialist Topics (63 chapters)**: In-depth storage (LVM, RAID, LUKS), systemd units, advanced networking, and security hardening.
- **Volume 03: TAMK Practice Workbook (53 chapters)**: 60 worked lab exercises with solutions from Tampere University of Applied Sciences: directory navigation, globbing, redirections, archiving, and text tools.
- **Volume 04: Internals & Architecture (35 chapters)**: Kernel subsystems, CFS CPU scheduler, virtual memory paging, page cache, VFS inodes, and direct syscall dispatch.
- **Volume 05: Operating System Theory (25 chapters)**: Concurrency, race conditions, deadlocks, memory management, and file systems.
- **Volume 06: Installing Software (32 chapters)**: Package managers (`dpkg`, `apt`, `rpm`, `dnf`), source builds (`autotools`, `cmake`, `make`), and containerization foundations.
- **Volume 07: Bash Configuration & Scripting (49 chapters)**: Shell environments (`.bashrc`, `.bash_profile`), arrays, parameter expansions, signals, and debugging.
- **Volume 08: Kernel Development Core (45 chapters)**: Loadable Kernel Modules, character drivers, `copy_to_user`/`copy_from_user`, device nodes, and kbuild Makefiles.
- **Volume 09: Kernel Deep Subsystems (50 chapters)**: Interrupt handling (top-half & bottom-half workqueues), spinlocks, mutexes, RCU (Read-Copy Update), memory allocators (Buddy allocator & Slab cache), and the unified Linux Device Model.
- **Specialist Guides**: Full guides on Grep/Sed/Awk Mastery, Linux Filesystem Hierarchy (FHS), Sudo Mastery, User/Group Management, and the Linux Job Hunting Guide for Finland.
- **Michael Kerrisk: TLPI 64-Chapter Roadmap**: Detailed breakdown of the canonical 1556-page systems programming standard.
- **Robert Love: LKD & Bovet: ULK3 Subsystems**: Kernel subsystem roadmap spanning memory management, process lifecycle, VFS, and driver frameworks.

### 2. 🎯 Interactive Practice Dojo (107 Graded Labs)
Automated testing and real-time grading against sandbox datasets:
- **Grep (19 Labs)**: Case insensitivity, line numbering, inverted matching, counting, IP extraction, UUID validation, context lines (`-A`, `-B`, `-C`).
- **Sed (19 Labs)**: In-place substitution, delimiter flexibility, line deletion, address ranges, uppercase transformations, and append/insert commands.
- **Awk (22 Labs)**: Field extraction, condition filtering, sum/average aggregations, custom FS/OFS separators, associative arrays, status code groupings.
- **Core & TAMK (20 Labs)**: Directory creation, hidden files, globbing patterns, file permissions (`chmod`, `chown`), symbolic/hard links, and tar archiving.
- **Sorting & Archiving (7 Labs)**: Numeric sorting, reverse deduplication, column-based sorting, piping filters, and gzip compression.
- **C Systems Programming (11 Modules)**: Direct file I/O syscalls, process trees (`fork`, `execve`, `waitpid`), signal handlers (`sigaction`), POSIX threads, IPC pipes, shared memory, and `epoll`.
- **Kernel Drivers (6 Labs)**: Loadable kernel modules, character device drivers, read/write callbacks, spinlocks, and procfs interfaces.

### 3. 📖 Comprehensive Linux Command Reference
Quick search and cheat sheets for 55+ essential commands:
- Includes full syntax, key options, and verified one-liner production examples for tools including `ls`, `grep`, `sed`, `awk`, `find`, `xargs`, `tar`, `chmod`, `chown`, `systemctl`, `journalctl`, `lsof`, `strace`, `ss`, `ip`, `ps`, `top`, `rsync`, `dd`, `curl`, and more.

### 4. 🧠 Linux Technical Interview Preparation Dojo
In-depth interview questions and detailed answers covering:
- Process vs. Thread memory architectures.
- Exact mechanics of the `syscall` CPU instruction and mode transitions (Ring 3 to Ring 0).
- Linux page faults (minor vs. major) and demand paging.
- Completely Fair Scheduler (CFS) and virtual runtime (`vruntime`).
- Virtual Filesystem (VFS) object model (`super_block`, `inode`, `dentry`, `file`).
- Read-Copy Update (RCU) vs. Spinlocks in kernel concurrent programming.
- Hard links vs. Symbolic links at the inode level.
- High-performance I/O multiplexing (`epoll` edge-triggered vs. level-triggered).

### 5. 🏗️ Kernel & OS Architecture Visualizer
ASCII architectural diagrams mapping:
- The System Call Boundary (glibc -> register dispatch -> `sys_call_table` -> VFS -> drivers).
- x86_64 48-bit Virtual Memory canonical layout (User Space bottom 128 TB vs. Kernel Space top 128 TB).
- The VFS Object Model relationship hierarchy.

### 6. 📁 Built-In Practice Datasets
Realistic production datasets located in `practice_data/`:
- `access.log` (Webserver traffic log)
- `app.log` (Production application log with ERROR, WARN, INFO entries)
- `employees.csv` (Employee department and salary records)
- `server.conf` (Configuration file with comments and blank lines)
- `users.txt` (System user database)
- `data.txt`, `names.txt`, `1.txt`, `2.txt` (TAMK lab datasets)

### 7. ⚙️ Safe User-Space Kernel Simulator Harness
- Test character device driver logic (`open`, `release`, `read`, `write`, `copy_to_user`, `copy_from_user`) using GCC without requiring root privileges or risking kernel panics.

### 8. ⚡ Zero External Dependencies
- Requires only standard Python 3 (`http.server`, `sqlite3`, `subprocess`, `urllib`) and standard GCC build tools. Runs out of the box on any standard Linux distribution.

---

## 🚀 Quick Start Guide

### 1. Launch the Web Platform
```bash
# Launch server on port 8080 (zero dependencies required)
./linux-mastery web --port 8080

# Or run directly via Python 3:
python3 web/server.py 8080
```
Open your browser at **`http://localhost:8080`**.

### 2. Practice Challenges via the Command-Line Dojo (CLI)
```bash
# Show status dashboard and current rank
./linux-mastery

# List challenges by category or tier
./linux-mastery list --cat grep
./linux-mastery list --cat awk
./linux-mastery list --cat core
./linux-mastery list --cat c_systems
./linux-mastery list --cat kernel

# Inspect challenge instructions
./linux-mastery show grep_01

# Submit and verify your bash solution
./linux-mastery run grep_01 "grep ERROR app.log"

# Get a hint or reveal reference solution
./linux-mastery hint grep_01
./linux-mastery solution grep_01

# Inspect overall progress & badges
./linux-mastery status
```

### 3. Compile and Test C System Programming Modules
```bash
make -C code_examples/03_system_programming test
```

### 4. Run the Safe Kernel Driver Simulator
```bash
make -C code_examples/04_kernel_modules test
```

### 5. Run the Automated Test Suite (107/107 Verification)
```bash
make test
```

---

## 📂 Project Directory Structure

```
├── .gitignore
├── README.md                          # Comprehensive documentation
├── Makefile                           # Global test and build orchestration
├── linux-mastery                      # Interactive CLI executable
├── curriculum/                        # 536 Markdown chapters & roadmaps
│   ├── volume_01_the_ultimate_edition/
│   ├── volume_02_specialist_topics/
│   ├── volume_03_practice_workbook/
│   ├── volume_04_internals_and_architecture/
│   ├── volume_05_operating_system_theory/
│   ├── volume_06_installing_software/
│   ├── volume_07_bash_configuration_and_scripting/
│   ├── volume_08_kernel_development/
│   ├── volume_09_kernel_deep_guide/
│   ├── specialist_guides/
│   ├── tlpi_systems_programming/
│   └── kernel_subsystems_lkd_ulk3/
├── practice_data/                     # Production log & CSV datasets
│   ├── access.log
│   ├── app.log
│   ├── employees.csv
│   ├── server.conf
│   └── users.txt
├── code_examples/
│   ├── 01_bash_scripts/               # Production bash scripts
│   ├── 02_text_processing/            # Reference solutions
│   ├── 03_system_programming/         # Compilable C syscall/epoll programs + Makefile
│   └── 04_kernel_modules/             # LKMs + user-space mock driver harness
├── simulator/                         # Grading engine, SQLite DB, CLI logic
│   ├── challenges.json                # 107 interactive challenges
│   ├── commands_reference.json        # 55+ command reference dictionary
│   └── interview_questions.json       # 8 technical interview deep questions
├── web/                               # Web platform (Vanilla JS, CSS3, REST API)
│   ├── server.py                      # Threaded HTTP server daemon
│   └── static/                        # SPA interface (index.html, styles.css, app.js)
└── tests/                             # Automated verification test suite
```

---

## 🏆 Mastery Badges & Ranks

### Ranks Progression:
- **Terminal Initiate (L0)**: 0 - 19 Labs Completed
- **Shell Journeyman (L1)**: 20 - 49 Labs Completed
- **Systems Craftsman (L2)**: 50 - 79 Labs Completed
- **Kernel Hacker (L3)**: 80 - 106 Labs Completed
- **Grandmaster of Linux (L4)**: All 107 Labs Completed

### Badges:
- 🔍 **Grep Grandmaster**: Solve all 19 grep challenges.
- ✂️ **Sed Stream Surgeon**: Master stream editing across all 19 sed exercises.
- ⚗️ **Awk Alchemist**: Complete all 22 advanced field & aggregation challenges.
- 🛡️ **TAMK Lab Veteran**: Complete all TAMK directory and archiving labs.
- 🧙‍♂️ **Text Processing Virtuoso**: Conquer 60+ text processing exercises.
- ⚡ **Syscall Sorcerer**: Write and verify Linux C System Programs.
- 🐧 **Kernel Subsystem Hacker**: Implement and verify Linux Kernel Driver Modules.

---

## 📜 Dedication & License
Designed and engineered for **MD Abdur Rahim** as a lifelong, comprehensive operating systems, systems engineering, and Linux kernel mastery platform.

Released under the **MIT License**.
