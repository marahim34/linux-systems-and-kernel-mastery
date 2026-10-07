15. Walk the four-layer network diagnosis order and the tool for each. (Ch. 10) 16. Why UUIDs in fstab, and
what does nofail prevent? (Ch. 9) 17. Explain the Docker-bypasses-ufw trap and its fix. (Ch. 21) 18. Describe
key-only SSH hardening AND the verification step that prevents lockout. (Ch. 14) 19. What is an SSH local
forward, with a database example? (Ch. 10) 20. Your pg_dump runs nightly — why is that alone not yet a
backup strategy? (Ch. 20)





Appendix C — Glossary
Term

Meaning

cgroup

Kernel mechanism limiting a process group's CPU/RAM/IO — powers containers and systemd
resource caps

CIDR (/24)

Subnet notation: /24 = first 24 bits are the network = 256 addresses

daemon

A background service process (sshd, nginx — the trailing d)

file descriptor

A process's numeric handle to an open file/socket; 0=stdin, 1=stdout, 2=stderr

HBA

PostgreSQL's host-based authentication rules (pg_hba.conf)

inode

The on-disk record of a file's metadata; filenames are just links to inodes

initramfs

Mini root filesystem the kernel uses at boot to load storage drivers

LVM

Logical Volume Manager — flexible layer between partitions and filesystems

namespace

Kernel isolation of a process's view (PIDs, network, mounts) — powers containers

OOM killer

Kernel's last resort under memory exhaustion: kills the 'worst' process

PID 1

The first process; systemd; ancestor of everything

reverse proxy

Front server (nginx) forwarding requests to backend apps

shebang

#!/usr/bin/env bash — the interpreter line of a script

socket

An endpoint for network (or local) communication, identified by IP:port

swap

Disk space used as overflow RAM

syscall

A request from a process to the kernel (open, read, connect) — what strace shows

target (systemd)

A named group of units; boot destinations like multi-user.target

TTL (DNS)

Seconds a resolver may cache a DNS answer

tuple/tup (pg)

A row version inside PostgreSQL; dead tuples = bloat

UUID

Stable unique ID for filesystems — the right identifier in fstab

unit (systemd)

Anything systemd manages: .service, .timer, .mount, .target

zombie

A finished process whose parent hasn't read its exit status — harmless in ones, a bug in hundreds

— End of the Ultimate Edition —