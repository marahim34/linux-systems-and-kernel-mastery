import os

docs = {}

docs["curriculum/tier1_core_and_bash/01_terminal_and_shell_foundations.md"] = """# Tier 1 · Chapter 1: Terminal & Shell Foundations

## 1. The Anatomy of the Linux Terminal
In Linux, the terminal is a text-based interface connecting the user to the command interpreter.
When you type a command:
1. The terminal emulator captures keystrokes and transmits them to the pseudo-terminal slave (PTS).
2. The PTS delivers the character stream to the interactive shell (typically `/bin/bash` or `/bin/zsh`).
3. The shell parses the line into tokens, performs expansions, searches `$PATH`, and invokes `fork()` and `execve()`.

## 2. Standard Streams & Redirection Mechanics
Every Linux process starts with three default file descriptors:
- **0 (STDIN)**: Standard Input
- **1 (STDOUT)**: Standard Output
- **2 (STDERR)**: Standard Error

### Essential Redirection Operators
```bash
# Redirect stdout to file (overwrite)
echo "production" > config.txt

# Redirect stdout to file (append)
echo "new entry" >> config.txt

# Redirect stderr only
command 2> errors.log

# Combine stdout and stderr into one stream
command > output.log 2>&1
# Modern bash shorthand:
command &> output.log

# Discard all output (black hole)
command > /dev/null 2>&1
```

## 3. The Pipe Operator (`|`)
Pipes create an anonymous unidirectional data channel in kernel memory between two processes:
```bash
cat /var/log/syslog | grep "CRITICAL" | wc -l
```
"""

docs["curriculum/tier1_core_and_bash/02_fhs_filesystem_hierarchy.md"] = """# Tier 1 · Chapter 2: The Linux Filesystem Hierarchy (FHS 3.0)

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
"""

docs["curriculum/tier1_core_and_bash/03_permissions_ownership_acls.md"] = """# Tier 1 · Chapter 3: Permissions, Ownership, and Special Bits

## 1. Traditional POSIX Permission Triplet
Linux file modes consist of 9 permission bits:
- **User (Owner)**: `rwx`
- **Group**: `rwx`
- **Others (World)**: `rwx`

## 2. Octal Numerical Representation
- Read (`r`) = 4
- Write (`w`) = 2
- Execute (`x`) = 1
Common modes: `755` (`rwxr-xr-x`), `644` (`rw-r--r--`), `600` (`rw-------`).

## 3. Special Permissions: SUID, SGID, and Sticky Bit
- **SUID (Octal 4000)**: Executable runs with permissions of the file OWNER (e.g. `/usr/bin/passwd`).
- **SGID (Octal 2000)**: On directories, newly created files inherit the parent directory GID.
- **Sticky Bit (Octal 1000)**: On world-writable directories (`/tmp`), only file owners can delete or rename files.

## 4. POSIX Access Control Lists (ACLs)
```bash
getfacl document.pdf
setfacl -m u:aisha:rw document.pdf
setfacl -x u:aisha document.pdf
```
"""

docs["curriculum/tier1_core_and_bash/04_user_group_management.md"] = """# Tier 1 · Chapter 4: User & Group Management Mastery

Synthesized from *Linux User & Group Management Mastery Guide*.

## 1. Core Identity Database Files
- `/etc/passwd`: `username:password_flag:UID:GID:GECOS:home_dir:shell`
- `/etc/shadow`: Cryptographic salted hashes (mode 0640).
- `/etc/group` & `/etc/gshadow`: Group definitions and memberships.

## 2. Account Lifecycle Commands
```bash
# Create user
useradd -m -s /bin/bash -c "Developer" john

# Set password
passwd john

# Add to supplementary groups
usermod -aG sudo,docker john

# Password aging policy
chage -M 90 john
```
"""

docs["curriculum/tier1_core_and_bash/05_sudo_and_privilege.md"] = """# Tier 1 · Chapter 5: Sudo & Privilege Escalation

Synthesized from *Sudo Mastery Complete*.

## 1. Why sudo Exists
- Granular least privilege.
- Full audit logging (`/var/log/auth.log`).
- Individual accountability (no shared root password).

## 2. Sudoers Syntax Grammar
`WHO  WHERE=(AS_WHOM)  TAGS: WHAT`

```sudoers
aisha ALL=(ALL:ALL) ALL
%sudo ALL=(ALL:ALL) ALL
marcus ALL=(ALL) NOPASSWD: /usr/bin/systemctl restart nginx
```

Always edit with `visudo` to prevent lockouts!
"""

docs["curriculum/tier1_core_and_bash/06_grep_sed_awk_complete_handbook.md"] = """# Tier 1 · Chapter 6: The Text-Processing Trio (Grep, Sed, Awk)

Synthesized from *Grep, Sed & Awk Mastery Complete*.

## 1. Division of Labor
- **grep**: *Search & Filter* - Finds lines matching regular expressions.
- **sed**: *Stream Editor* - Modifies, replaces, and transforms text line-by-line.
- **awk**: *Field & Report Processor* - Complete programming language for columnar data and math.

## 2. Real-World Cheatsheets
### Grep
```bash
grep -i PATTERN file    # Case-insensitive
grep -v PATTERN file    # Invert match
grep -c PATTERN file    # Count matching lines
grep -n PATTERN file    # Line numbers
grep -oE '^[0-9.]+' log # Extract matching segment
grep -C 2 PATTERN file  # Context lines
```

### Sed
```bash
sed 's/old/new/g' file             # Replace all
sed -i.bak 's/8080/9090/' conf     # In-place with backup
sed '/^#/d; /^$/d' conf            # Strip comments & blanks
sed -n '5,10p' file                # Line range
sed -E 's/port ([0-9]+)/\\1 is port/' conf # Backreferences
```

### Awk
```bash
awk '{print $1, $9}' access.log                 # Columns
awk -F: '{print $1, $6}' /etc/passwd            # Custom delimiter
awk '$9 == 500 {print $1}' access.log           # Conditions
awk '{sum += $10} END {print sum}' access.log   # Sum
awk '{c[$1]++} END {for (i in c) print c[i], i}' log | sort -rn # Group-by count
```
"""

# TIER 2
docs["curriculum/tier2_system_administration/01_storage_lvm_raid_luks.md"] = """# Tier 2 · Chapter 1: Storage Subsystems (LVM, RAID, LUKS)

## 1. The Storage Abstraction Stack
```
  [ Filesystem (ext4 / xfs / btrfs) ]
                  ▲
  [ Logical Volume (LV) ]
                  ▲
  [ Volume Group (VG) ]
                  ▲
  [ Physical Volumes (PV: /dev/sda2, /dev/sdb1) ]
                  ▲
  [ Encrypted Layer (LUKS / dm-crypt) ]
                  ▲
  [ Physical Disk or Software RAID (mdadm) ]
```

## 2. LVM Hands-On Commands
```bash
# Initialize Physical Volume
pvcreate /dev/sdb1

# Create Volume Group
vgcreate vg_data /dev/sdb1

# Create Logical Volume (50GB)
lvcreate -L 50G -n lv_app vg_data

# Format with ext4
mkfs.ext4 /dev/vg_data/lv_app

# Grow Logical Volume by 10GB AND resize filesystem live!
lvextend -L +10G -r /dev/vg_data/lv_app
```
"""

docs["curriculum/tier2_system_administration/02_systemd_and_services.md"] = """# Tier 2 · Chapter 2: Systemd Architecture & Unit Management

## 1. Systemd Architecture
Systemd is the PID 1 init system and service manager for modern Linux.
It provides socket activation, parallel service startup, cgroup resource isolation, and declarative dependency graphs.

## 2. Production Unit File Example (`/etc/systemd/system/app.service`)
```ini
[Unit]
Description=Production API Service
After=network.target postgresql.service
Wants=postgresql.service

[Service]
Type=simple
User=appuser
Group=appuser
WorkingDirectory=/opt/app
ExecStart=/usr/bin/python3 -m app.main
Restart=always
RestartSec=5s
Environment=PORT=8000
LimitNOFILE=65535

# Security hardening directives
ProtectSystem=strict
ProtectHome=true
NoNewPrivileges=true
PrivateTmp=true

[Install]
WantedBy=multi-user.target
```

## 3. Service Commands
```bash
sudo systemctl daemon-reload
sudo systemctl enable --now app.service
sudo systemctl status app.service
journalctl -u app.service -f
```
"""

# TIER 3
docs["curriculum/tier3_system_programming_c/01_system_calls_and_file_io.md"] = """# Tier 3 · Chapter 1: Linux System Calls & File I/O Architecture

Synthesized from *The Linux Programming Interface (TLPI)* by Michael Kerrisk.

## 1. User Space vs Kernel Space & The Syscall Boundary
Applications cannot access hardware directly. To perform I/O, they invoke a **System Call** (syscall).
1. Application calls wrapper function in glibc (e.g. `open()`).
2. Wrapper loads syscall number into register (`%rax` on x86_64) and arguments into `%rdi`, `%rsi`, `%rdx`, `%r10`, `%r8`, `%r9`.
3. CPU executes `syscall` instruction, transitioning CPU mode from Ring 3 (User) to Ring 0 (Kernel).
4. Kernel executes `sys_call_table[rax]`.
5. Kernel transitions CPU back to Ring 3 with return code in `%rax`.

## 2. Core Low-Level I/O Calls
```c
int open(const char *pathname, int flags, mode_t mode);
ssize_t read(int fd, void *buf, size_t count);
ssize_t write(int fd, const void *buf, size_t count);
off_t lseek(int fd, off_t offset, int whence);
int close(int fd);
```

### Critical Flags
- `O_RDONLY`, `O_WRONLY`, `O_RDWR`
- `O_CREAT | O_EXCL`: Atomic file creation (fails if file exists, prevents symlink race conditions).
- `O_TRUNC`: Truncate file to 0 bytes.
- `O_APPEND`: Atomic append to end of file on every write.
- `O_NONBLOCK`: Non-blocking mode (returns `EAGAIN` or `EWOULDBLOCK` instead of sleeping).
- `O_DIRECT`: Bypasses the Linux page cache for direct DMA disk transfer.
"""

docs["curriculum/tier3_system_programming_c/02_processes_and_threads.md"] = """# Tier 3 · Chapter 2: Process Lifecycle & POSIX Multithreading

Synthesized from *TLPI* Ch. 24-33.

## 1. Process Lifecycle
- `fork()`: Creates an almost identical clone of the calling process. Uses **Copy-On-Write (COW)**: memory pages are shared read-only until either process writes to a page, which triggers a page fault and duplicates only that page.
- `execve()`: Replaces current process image with a new executable program.
- `waitpid()`: Parent collects child exit status and prevents **Zombie processes** (terminated child whose entry remains in the kernel process table until parent calls wait).

## 2. POSIX Threads (pthreads)
Unlike processes which have independent virtual address spaces, threads in the same process share:
- Memory address space (heap, global variables, code)
- Open file descriptors
- Signal actions

Each thread gets its own private:
- Stack
- Register state
- Thread-Local Storage (TLS)

### Concurrency Primitives
- `pthread_mutex_t`: Mutual exclusion lock.
- `pthread_cond_t`: Signaling mechanism between threads for condition synchronization.
- `pthread_rwlock_t`: Multiple-reader single-writer lock.
"""

docs["curriculum/tier3_system_programming_c/03_epoll_and_event_loops.md"] = """# Tier 3 · Chapter 3: High-Performance I/O Multiplexing & epoll

Synthesized from *TLPI* Ch. 63.

## 1. Why `select` and `poll` Don't Scale: O(N) vs O(1)
- `select` and `poll` require the application to pass all N monitored file descriptors into the kernel on every call, and iterate through the entire set to find active fds. As connections reach 10,000+ (the C10K problem), performance collapses.
- Linux `epoll` maintains an interest list inside kernel memory using a **Red-Black Tree**. When network events arrive, hardware interrupts place ready descriptors into a ready **Doubly Linked List**. `epoll_wait` simply inspects this ready list in **O(1)** time!

## 2. Core epoll Syscalls
```c
// 1. Create epoll instance
int epoll_fd = epoll_create1(0);

// 2. Register / modify / unregister file descriptors
struct epoll_event ev;
ev.events = EPOLLIN | EPOLLET; // Edge-Triggered
ev.data.fd = socket_fd;
epoll_ctl(epoll_fd, EPOLL_CTL_ADD, socket_fd, &ev);

// 3. Wait for events
struct epoll_event events[64];
int nfds = epoll_wait(epoll_fd, events, 64, -1);
```
"""

# TIER 4
docs["curriculum/tier4_kernel_programming/01_kernel_architecture_and_tour.md"] = """# Tier 4 · Chapter 1: Linux Kernel Architecture & Source Tour

Synthesized from Robert Love's *Linux Kernel Development* & Bovet's *Understanding the Linux Kernel*.

## 1. Monolithic Kernel with Modularity
The Linux kernel is a monolithic design: all core subsystems (scheduler, virtual memory, filesystems, network stack, device drivers) execute in a single unified privileged address space (**Ring 0**).
However, it gains microkernel-like flexibility through **Loadable Kernel Modules (LKMs)**, allowing code to be loaded and unloaded dynamically into the running kernel without rebooting.

## 2. Core Kernel Subsystems
1. **Process Scheduler (CFS / EEVDF)**: Manages CPU time allocation among threads.
2. **Memory Management (MM)**: Page tables, TLB management, buddy allocator, SLAB/SLUB cache, virtual memory areas (`vm_area_struct`).
3. **Virtual Filesystem (VFS)**: Abstract layer providing uniform file interface across ext4, btrfs, nfs, procfs, sysfs via `inode`, `dentry`, `file`, and `super_block` objects.
4. **Network Stack**: BSD socket layer, TCP/IP stack, sk_buff packet buffers, netdevice drivers.
5. **Device Drivers**: Character devices, block devices, platform devices.

## 3. Kernel Space vs User Space Rules
- **No glibc**: You cannot use `printf()`, `malloc()`, `exit()`, or `<stdio.h>`. You use `printk()`, `kmalloc()`, etc.
- **Small fixed stack**: Kernel stack is strictly limited (typically 8KB or 16KB per thread). Never allocate large buffers on stack!
- **Floating point forbidden**: FP registers are not saved on kernel entry for performance reasons.
- **Never dereference user pointers directly**: User memory can be swapped out, invalid, or malicious. Always use `copy_to_user()` and `copy_from_user()`.
"""

docs["curriculum/tier4_kernel_programming/02_loadable_kernel_modules.md"] = """# Tier 4 · Chapter 2: Writing Loadable Kernel Modules (LKMs)

Synthesized from *Linux Mastery Complete Library* Volume 8 & Robert Love Ch. 17.

## 1. Anatomy of an LKM
```c
#include <linux/init.h>
#include <linux/module.h>
#include <linux/kernel.h>

MODULE_LICENSE("GPL");
MODULE_AUTHOR("MD Abdur Rahim");
MODULE_DESCRIPTION("Mastery Kernel Module");
MODULE_VERSION("1.0");

static int __init my_module_init(void) {
    pr_info("Module loaded successfully into kernel memory!\n");
    return 0; // Return 0 for success
}

static void __exit my_module_exit(void) {
    pr_info("Module unloaded from kernel memory.\n");
}

module_init(my_module_init);
module_exit(my_module_exit);
```

## 2. Compiling Against Linux Headers
In kernel development, modules are compiled using the kernel's **Kbuild** system:
```makefile
obj-m += my_module.o

KDIR ?= /lib/modules/$(shell uname -r)/build
PWD := $(shell pwd)

default:
\t$(MAKE) -C $(KDIR) M=$(PWD) modules

clean:
\t$(MAKE) -C $(KDIR) M=$(PWD) clean
```

## 3. Module Commands
```bash
sudo insmod my_module.ko    # Load module
lsmod | grep my_module      # Check loaded status
dmesg | tail -n 10          # Read kernel ring buffer
sudo rmmod my_module        # Unload module
modinfo my_module.ko        # Inspect metadata
```
"""

docs["curriculum/tier4_kernel_programming/03_character_device_drivers.md"] = """# Tier 4 · Chapter 3: Character Device Drivers & File Operations

Synthesized from *Linux Mastery* Volume 8 & Robert Love Ch. 13.

## 1. What is a Character Device?
A character device provides a stream of unbuffered, sequential bytes (e.g. serial ports, keyboard, sensors, crypto engines, virtual buffers).
User space accesses them via filesystem nodes in `/dev` (e.g. `/dev/dojo_char`).

## 2. Major and Minor Numbers
- **Major Number**: Identifies the device driver in the kernel.
- **Minor Number**: Identifies the specific physical device instance managed by that driver.

```c
dev_t dev_num;
alloc_chrdev_region(&dev_num, 0, 1, "my_char_device");
int major = MAJOR(dev_num);
int minor = MINOR(dev_num);
```

## 3. The `file_operations` Structure
The bridge between user-space syscalls and kernel driver functions:
```c
static struct file_operations fops = {
    .owner   = THIS_MODULE,
    .open    = device_open,
    .release = device_release,
    .read    = device_read,
    .write   = device_write,
    .unlocked_ioctl = device_ioctl,
};
```

## 4. User-Kernel Data Transfer
```c
// Sending data to user space
copy_to_user(user_buffer, kernel_buffer, count);

// Reading data from user space
copy_from_user(kernel_buffer, user_buffer, count);
```
Returns number of uncopied bytes. 0 means complete success!
"""

docs["curriculum/tier4_kernel_programming/04_kernel_concurrency_and_rcu.md"] = """# Tier 4 · Chapter 4: Kernel Concurrency, Locking & RCU

Synthesized from *Linux Mastery* Volume 9 & Robert Love Ch. 9-10.

## 1. Concurrency Sources in the Kernel
Code in the kernel can be interrupted and interleaved by:
1. Symmetric Multiprocessing (SMP): multiple CPU cores running kernel code simultaneously.
2. Kernel Preemption: a higher priority task preempting running kernel code.
3. Interrupts (IRQs): hardware interrupts firing at any time.
4. Bottom halves: softirqs and tasklets.

## 2. Locking Primitives
- **Spinlocks (`spinlock_t`)**: Busy-waiting lock. Must be used in interrupt context where sleeping is prohibited! NEVER call sleeping functions (like `msleep()` or `copy_to_user()`) while holding a spinlock!
- **Mutexes (`struct mutex`)**: Sleeping lock. Used in process context when critical section may sleep or block on I/O.
- **Atomic Operations (`atomic_t`)**: Hardware atomic read/modify/write instructions without lock overhead.

## 3. Read-Copy-Update (RCU)
RCU is a state-of-the-art synchronization mechanism optimized for read-heavy data structures:
- **Readers**: Zero lock contention! Readers simply call `rcu_read_lock()` and `rcu_read_unlock()`. No atomic bus locks or cache bouncing!
- **Writers**: Allocate a new copy of the data, mutate the copy, update the pointer atomically with `rcu_assign_pointer()`, and defer freeing the old copy until all preexisting readers have finished (grace period via `synchronize_rcu()` or `call_rcu()`).
"""

for path, content in docs.items():
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(content.strip() + "\n")

print(f"Successfully generated all {len(docs)} comprehensive curriculum guides!")
