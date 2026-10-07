# Tier 1 · Chapter 2: The Linux Filesystem Hierarchy (FHS 3.0)

Synthesized from *The Linux Filesystem Hierarchy Explained Guide*.

In Linux, everything is attached to a single unified hierarchical tree starting at the root directory `/`.

## Directory Blueprint & Architectural Roles

| Directory | Full Name / Meaning | Purpose & Contents |
|---|---|---|
| `/bin` & `/sbin` | Binaries / System Binaries | Core executable binaries needed in single-user mode. (Symlinked to `/usr/bin` in modern systems). |
| `/usr` | Unix System Resources | Secondary hierarchy for read-only user programs, libraries, headers (`/usr/include`), docs. |
| `/etc` | "et cetera" / Configuration | System-wide text configuration files (`/etc/passwd`, `/etc/fstab`, `/etc/ssh/sshd_config`). |
| `/var` | Variable Data | Dynamic data that changes during execution: logs (`/var/log`), spool queues, databases (`/var/lib`). |
| `/tmp` | Temporary Space | Volatile scratch space; world-writable with sticky bit enabled; wiped on reboot. |
| `/dev` | Device Nodes | Character and block device files representing hardware (`/dev/sda`, `/dev/null`, `/dev/urandom`). |
| `/proc` | Process & Kernel Info | Virtual pseudo-filesystem generated dynamically by the Linux kernel (`/proc/cpuinfo`, `/proc/meminfo`). |
| `/sys` | System / sysfs | Unified device driver model hierarchy; exposes kernel objects, bus topologies, and power tunables. |
| `/boot` | Bootloader & Kernels | GRUB configuration, initramfs archives, and compressed kernel images (`vmlinuz`). |
| `/opt` | Optional Software | Self-contained third-party application suites. |
