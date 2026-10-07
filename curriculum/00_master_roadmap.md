# 🗺️ Master Curriculum Blueprint: From Linux Novice to Kernel Hacker

Welcome to the **Complete Linux Systems & Kernel Mastery Platform**, prepared for **MD Abdur Rahim**.
This roadmap synthesizes knowledge across 20 canonical Linux texts, including:
- *The Linux Mastery Complete Library (9 Volumes)*
- *The Linux Programming Interface (TLPI)* by Michael Kerrisk
- *Linux Kernel Development (3rd Edition)* by Robert Love
- *Understanding the Linux Kernel (ULK3)* by Bovet & Cesati
- *Advanced Linux Programming* by Mitchell, Oldham & Samuel
- *The Linux Command Line* by William Shotts
- *Grep, Sed & Awk Mastery & Practice Guides*
- *Linux Filesystem Hierarchy & Sudo / User Management Guides*

---

## 🎯 The Four Mastery Tiers

```
  ┌─────────────────────────────────────────────────────────────┐
  │ TIER 4: LINUX KERNEL PROGRAMMING & SUBSYSTEMS               │
  │ LKMs · Char Drivers · Memory Alloc · Concurrency/RCU · IRQs │
  └──────────────────────────────▲──────────────────────────────┘
                                 │
  ┌──────────────────────────────┴──────────────────────────────┐
  │ TIER 3: ADVANCED LINUX SYSTEM PROGRAMMING IN C              │
  │ Syscalls · Process Tree · Signals · Pthreads · IPC · epoll  │
  └──────────────────────────────▲──────────────────────────────┘
                                 │
  ┌──────────────────────────────┴──────────────────────────────┐
  │ TIER 2: SYSTEM ADMINISTRATION, DEVOPS & SPECIALIST OPS      │
  │ LVM/RAID · WireGuard · systemd · cgroups · SELinux · auditd │
  └──────────────────────────────▲──────────────────────────────┘
                                 │
  ┌──────────────────────────────┴──────────────────────────────┐
  │ TIER 1: LINUX FOUNDATIONS, SHELL CRAFT & TEXT PROCESSING    │
  │ Core Shell · FHS · Permissions · Sudo · Grep/Sed/Awk (50 Ex)│
  └─────────────────────────────────────────────────────────────┘
```

---

## 📌 Tier Breakdown & Learning Milestones

### 🟢 Tier 1: Core Shell, System Foundations & Text Wrangling
1. **The Linux Mindset & Shell Mechanics**: STDIN/STDOUT/STDERR, pipes, redirections, globbing, quoting rules.
2. **Filesystem Hierarchy Standard (FHS 3.0)**: `/etc`, `/var`, `/usr`, `/proc`, `/sys`, `/dev`, `/boot`, and the `usr-merge`.
3. **Permissions & Access Control**: Octal/symbolic chmod, chown/chgrp, special bits (SUID, SGID, Sticky bit), POSIX ACLs (`getfacl`/`setfacl`).
4. **User & Group Administration**: `/etc/passwd`, `/etc/shadow`, `/etc/group`, `/etc/gshadow`, PAM basics, account aging (`chage`).
5. **Sudo & Privilege Escalation**: Sudoers grammar, `Cmnd_Alias`, `User_Alias`, environment passing (`env_keep`), secure configuration.
6. **The Text-Processing Trio (Grep, Sed, Awk)**:
   - 15 Graded Grep exercises: regex, context lines, inversion, counting, IP extraction.
   - 15 Graded Sed exercises: substitutions, address ranges, line deletion, backreferences.
   - 20 Graded Awk exercises: columnar fields, record separators, math aggregations, arrays, formatting.
   - 5 Bonus Combo Pipelines: real-world log forensics and anomaly detection.
7. **Production Shell Scripting**: Strict mode (`set -euo pipefail`), traps, functions, parameter expansion, robust error exits.

### 🟡 Tier 2: Linux Administration, DevOps & Specialist Operations
1. **Storage Subsystems**: Partitioning (GPT/MBR), LVM (PV, VG, LV live resizing), software RAID (`mdadm`), LUKS disk encryption.
2. **Networking & Firewalls**: `ip` route/addr, socket states (`ss`), `nftables`/`iptables`, WireGuard VPN tunnels, Network Namespaces.
3. **Init & Service Architecture**: systemd unit files (`[Unit]`, `[Service]`, `[Install]`), target states, cgroups v2 resource slicing, journald.
4. **Linux Security & Sandboxing**: SELinux type enforcement, AppArmor profiles, Linux Capabilities (`capsh`, `setcap`), `auditd` logging.
5. **Troubleshooting & Observability**: Load averages, `/proc/meminfo`, vmstat, iostat, sar, `strace`, `lsof`, `perf`, `bpftrace`.

### 🟠 Tier 3: Advanced Linux System Programming in C (TLPI & ALP)
1. **System Call Architecture & Low-Level I/O**: `open`, `read`, `write`, `close`, `lseek`, atomic flags `O_CREAT|O_EXCL`, `O_DIRECT`, `O_NONBLOCK`, `fcntl`, `ioctl`.
2. **Process Lifecycle**: `fork` copy-on-write semantics, `execve` environment setup, `waitpid` status macros (`WIFEXITED`, `WEXITSTATUS`, `WTERMSIG`), daemonization.
3. **Signals & Asynchronous Events**: Signal safety, `sigaction`, signal masks, `sigprocmask`, `sig_atomic_t`, realtime signals, `signalfd`.
4. **POSIX Multithreading & Synchronization**: `pthread_create`, `pthread_join`, thread safety, mutexes (`pthread_mutex_t`), condition variables (`pthread_cond_t`), rwlocks, memory ordering.
5. **Inter-Process Communication (IPC)**:
   - Anonymous pipes & named FIFOs.
   - POSIX Message Queues (`mq_open`, `mq_send`, `mq_receive`).
   - POSIX Shared Memory (`shm_open`, `ftruncate`, `mmap`, `sem_open`).
6. **Virtual Memory & Zero-Copy I/O**: `mmap`, `munmap`, `mprotect`, `madvise`, `brk`/`sbrk`, page fault mechanics, memory leak detection with Valgrind.
7. **High-Performance Event Loops**: BSD sockets, `select`, `poll`, `epoll` (`epoll_create1`, `epoll_ctl`, `epoll_wait`, edge-triggered vs level-triggered), and Linux `io_uring`.

### 🔴 Tier 4: Linux Kernel Subsystem & Driver Development (LKD & ULK3)
1. **Kernel Architecture & Source Navigation**: Monolithic kernel with modularity, kernel address space vs user address space, syscall dispatch table (`sys_call_table`).
2. **Loadable Kernel Modules (LKMs)**: Module structure, `module_init`, `module_exit`, `MODULE_LICENSE`, `printk` log levels, `module_param`.
3. **Character Device Drivers**: `alloc_chrdev_region`, `cdev_init`, `cdev_add`, `file_operations` table (`open`, `read`, `write`, `unlocked_ioctl`, `release`).
4. **User-Kernel Memory Boundary**: Safe pointer validation, `copy_to_user`, `copy_from_user`, preventing kernel memory leakage and corruption.
5. **Kernel Memory Management**: `kmalloc` vs `vmalloc`, GFP flags (`GFP_KERNEL`, `GFP_ATOMIC`), SLAB/SLUB cache allocators (`kmem_cache_create`), page allocation (`alloc_pages`).
6. **Kernel Concurrency & Synchronization**: Interrupt context rules (no sleeping!), spinlocks (`spinlock_t`, `spin_lock_irqsave`), mutexes, atomic operations (`atomic_t`), Read-Copy-Update (RCU: `rcu_read_lock`, `synchronize_rcu`), lockdep validator.
7. **Interrupts & Deferral**: Top-half ISR (`request_irq`), bottom halves (Softirqs, Tasklets, Workqueues), timers (`jiffies`, `HZ`, `timer_list`).
8. **Kernel Interfaces & Tracing**: `/proc` interface (`proc_create`, `proc_ops`), `/sys` (kobjects, device attributes), debugfs, kprobes, tracepoints, and eBPF.
