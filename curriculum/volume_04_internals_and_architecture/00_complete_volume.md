# Volume 4: Internals & Architecture

package on the system. Combined with Volume 1's foundations and Volume 4's understanding of WHY the
filesystem is shaped this way, nothing about installing or finding software on Linux should ever again feel like
a mystery.

Install with intention, know where it lives, and you can always find it again.
— End of Volume 6, Installing Software & Finding Things —

LINUX MASTERY
VOLUME 4 — INTERNALS &
ARCHITECTURE
How Linux Actually Works, From Silicon to Shell — The Operating System,
the Kernel, Processes, Memory, the Filesystem, System Calls, Boot, History
and a Complete Career Roadmap

The 'why it works' layer · Prepared for MD Abdur Rahim · Tampere, Finland · 2026





Table of Contents — Volume 4
1. What an Operating System Is — and Why It Exists
2. The Big Picture — Linux Architecture in Layers
3. The Kernel — the Heart of the System
4. Processes — How Programs Come Alive
5. The CPU Scheduler — Sharing One Processor Among Many
6. Memory — Virtual Memory, Paging & the Great Illusion
7. The Filesystem — Inodes, VFS & the Tree Explained
8. The Folder System — Every Directory and Why It Exists
9. The Life of a File Read — a Full Journey Through the Stack
10. System Calls — the Bridge Between Your Code and the Kernel
11. The Boot Process — From Power Button to Login
12. Devices & Drivers — Everything Is a File, Explained
13. How Linux Came to Be — Unix, GNU & the Distributions
14. What Makes Linux Unique — the Design Ideas That Won
15. Career Roadmap — What to Learn, in What Order, for Which Job





1. What an Operating System Is
The problem an OS solves
Imagine a computer with no operating system. You have a CPU, some RAM, a disk, a keyboard and a
screen. To write even one character to the screen, your program would need to know the exact hardware
model, its memory addresses, and its electrical signalling. Every program would have to include drivers for
every possible device. Two programs running at once would overwrite each other's memory and crash. This
was the reality of early computing.
An operating system is the layer that sits between raw hardware and your programs, and solves four hard
problems so that no application has to:
Job of the OS

What it means

Without it...

Abstraction

Hides hardware behind simple,
uniform interfaces

Every app needs drivers for every
device

Resource management

Shares CPU, RAM, disk among
many programs fairly

One program hogs everything; others
starve

Isolation &amp; protection

Stops programs harming each other
or the system

One bug crashes the whole machine

Convenience

Provides files, processes, networking
as ready services

Everyone reinvents the same
plumbing

The two worlds: kernel space and user space
This single distinction is the foundation of everything in this volume. The CPU itself can run in (at least) two
privilege levels, and the OS uses them to draw a hard security boundary:
Kernel space

User space

Who runs here

The kernel only

All your programs: bash, Python,
nginx, Firefox

Privilege

Full: can touch any hardware, any
memory

Restricted: cannot touch hardware
directly

CPU mode

Supervisor / ring 0

User / ring 3

If it crashes

The whole system halts (kernel
panic)

Just that one program dies

PRO INSIGHT: This is why Linux is stable. A misbehaving app (user space) cannot bring down the machine,
because the hardware itself forbids it from touching protected memory or devices. Only the small, carefully-written
kernel has that power. A crash in your Python script is a rounding error in the universe; a crash in the kernel is the
end of the world. That is why the kernel is kept small and everything else is pushed to user space.

How a program crosses the boundary — a preview





Your program lives in user space and cannot, for example, read a file directly, because the disk is hardware.
So it asks the kernel to do it, through a system call — a controlled doorway into kernel space. The program
says 'please read this file', the CPU switches to kernel mode, the kernel does the privileged work, and control
returns to your program with the result. Chapter 10 covers this in full; for now, hold the image of a guarded
doorway between two worlds.
Every meaningful thing a program does — open a file, send a network packet, create another process,
allocate memory — is ultimately a request across this boundary. Understanding Linux deeply is, to a large
degree, understanding this conversation between user space and the kernel.
PRO INSIGHT: Unique Linux point: the boundary is real but the SAME kernel serves a tiny embedded router, a
phone (Android), a laptop, and a supercomputer. One codebase scales across a billion-fold range of hardware
because the abstraction layer is so clean. No other operating system spans that range.





2. The Big Picture — Linux Architecture in Layers
The stack, top to bottom
Everything in Linux can be placed in one of these layers. When you debug or design, knowing which layer
you are in tells you which tools apply and what can go wrong.
Layer

Lives in

Examples

You meet it as

Applications

User space

Firefox, nginx, your
FastAPI app

The programs you run

Shell &amp; utilities

User space

bash, ls, grep, systemctl

The command line

System libraries

User space

glibc (the C library)

What programs link against

System call interface

The boundary

read(), write(), fork()

The doorway to the kernel

The kernel

Kernel space

scheduler, memory mgr,
VFS, drivers

The invisible manager

Hardware

Physical

CPU, RAM, disk, network
card

The metal

Walking the layers with one command
When you run cat notes.txt, you touch every layer:
Step

Layer

What happens

1

Shell

bash finds the cat program and starts
it

2

Application

cat wants to read notes.txt

3

Library

cat calls the C library's fopen/read
wrappers

4

System call

the library invokes the open() and
read() syscalls

5

Kernel (VFS)

the kernel's filesystem layer locates
the file

6

Kernel (driver)

the disk driver fetches the actual
bytes

7

Hardware

the SSD returns the data over the
bus

8

back up

bytes travel back up to cat, which
writes them to your screen (another
syscall)





PRO INSIGHT: This layered design is why you can replace one layer without touching the others. Swap the SSD
for a network disk — only the driver changes; cat is untouched. Swap bash for zsh — the kernel neither knows nor
cares. Each layer speaks only to its neighbours through a stable contract. This is the single most important
architectural idea in the whole system.

The kernel is monolithic — but modular
Linux is a monolithic kernel: the scheduler, memory manager, filesystems and drivers all run together in
kernel space as one program. The alternative design, a microkernel, keeps only the bare minimum in kernel
space and pushes drivers into user space. Linux chose monolithic for speed (no boundary-crossing between
kernel components) but softened the downside with loadable kernel modules: drivers can be added and
removed from the running kernel on demand.
lsmod | head
sudo modprobe uvcvideo
sudo rmmod uvcvideo

1. List modules currently plugged into the running kernel — each is a driver or feature loaded on demand.
2. Load a module (here, the USB webcam driver) into the live kernel without rebooting.
3. Remove it again. This modularity is how one kernel supports thousands of devices without being one giant fixed blob.

PRO INSIGHT: Unique point: Linux gets the performance of a monolithic kernel AND much of the flexibility of a
microkernel, through modules. Windows and macOS kernels are hybrids that made different trade-offs. Linux's
choice — fast core, hot-swappable drivers — is a big reason it dominates servers, where you load exactly the
drivers you need and nothing more.





3. The Kernel — the Heart of the System
What the kernel actually is
The kernel is a single program — a large C program of about 30 million lines — that loads into protected
memory at boot and stays running until shutdown. It is not a process you can see in your process list,
because it IS the thing that runs processes. Everything else on the machine exists at its pleasure. Its job is to
be the sole manager of four things:
Subsystem

Manages

Covered in

Process management

Creating, running, ending programs

Chapters 4–5

Memory management

Who gets which RAM, the
virtual-memory illusion

Chapter 6

The Virtual File System

All files and filesystems behind one
interface

Chapter 7

Device drivers &amp; networking

Talking to hardware and the network

Chapter 12

Where the kernel lives
uname -r
ls /boot/vmlinuz-*
ls /lib/modules/$(uname -r)/kernel | head
cat /proc/version

1. The running kernel's version string.
2. The kernel image itself — the compressed file loaded at boot (vmlinuz = 'virtual memory linux, gzipped').
3. The loadable modules for this exact kernel version, organised by category (fs, net, drivers).
4. Full build details: compiler version, build date. /proc is a live window INTO the kernel, which is itself a fascinating idea
(see below).

The /proc and /sys illusion — the kernel as files
Here is one of Linux's most elegant tricks. The kernel exposes its own internal state as if it were files, under
/proc and /sys. These are not real files on disk; reading them makes the kernel generate the answer on the
spot. This means you can inspect and even reconfigure the running kernel with ordinary commands like cat
and echo.





cat /proc/cpuinfo | grep "model name" | head -1
cat /proc/meminfo | head -3
cat /proc/loadavg
cat /sys/class/thermal/thermal_zone0/temp
echo 1 | sudo tee /proc/sys/net/ipv4/ip_forward

1. The kernel reports your CPU model — generated live when you read the file.
2. Live memory statistics, straight from the memory manager.
3. The load averages, computed by the scheduler.
4. Your CPU temperature in millidegrees — the kernel reading a hardware sensor for you.
5. Writing a file CHANGES kernel behaviour: this switches on packet forwarding. The filesystem interface is read AND
write.

PRO INSIGHT: Unique point: /proc and /sys turn kernel introspection into text manipulation. On most operating
systems, inspecting kernel state requires special APIs and programming. On Linux, cat and echo are enough. This
is the 'everything is a file' philosophy applied to the kernel itself — and it is why Linux is the OS you can fully
understand from the command line.

What the kernel does NOT do
A crucial clarification. The kernel does not include the shell, the desktop, the compiler, or the utilities like ls
and grep. Those are user-space programs, mostly from the GNU project, which is why purists call the
system 'GNU/Linux'. The kernel provides mechanism (the ability to run programs, access files); user space
provides the actual programs. Keeping this line clear resolves endless confusion.





4. Processes — How Programs Come Alive
Program versus process
A program is a passive file on disk — the /usr/bin/python3 binary just sitting there. A process is a program in
motion: loaded into memory, given a slice of CPU time, with its own state. The same program can run as
many separate processes at once. The kernel's job is to breathe life into programs and keep every resulting
process isolated from the others.
Each process gets, from the kernel:
Resource

What it is

A PID

A unique process ID number

Virtual address space

Its own private view of memory (Chapter 6)

File descriptors

Numbered handles to its open files and sockets

Credentials

The user and group it runs as (permissions)

A parent (PPID)

The process that created it

State

Running, sleeping, stopped, or zombie

How a process is born: fork and exec
This is one of Unix's most beautiful and unusual design choices. To start a new program, Linux uses TWO
steps, not one:
Step

Syscall

What happens

1. Clone

fork()

The process makes a near-identical
COPY of itself. Now there are two.

2. Transform

execve()

The copy REPLACES its own
program with the new one it wants to
run.

# conceptually, when bash runs 'ls':
pid = fork(); # bash duplicates itself
if (pid == 0) { # in the child copy:
execve("/usr/bin/ls", ...); # become ls
} else { # in the parent (bash):
wait(pid); # wait for ls to finish
}

1. bash clones itself with fork; now two bash processes exist, parent and child.
2. The child branch (fork returns 0 in the child)...
3. ...calls execve, which discards the bash program and loads ls in its place. Same process, new identity.
4. Meanwhile the parent (fork returns the child's PID)...
5. ...waits for the child (now ls) to finish, then continues. This fork-then-exec dance starts EVERY program on the
system.





PRO INSIGHT: Unique point: separating fork (copy) from exec (transform) seems wasteful but is genius. It means
the brief moment BETWEEN them is where the shell sets up redirections and pipes (Volume 3). The child can
rearrange its own file descriptors before becoming the new program. This is exactly how command > file.txt and
pipelines work under the hood — the plumbing is done in the gap between fork and exec. No other design makes
I/O redirection so clean.

The process tree — everything has a parent
Because every process is forked from another, all processes form one giant family tree. At the root sits PID 1,
systemd, started directly by the kernel at boot. Kill a parent and its orphaned children are adopted by PID 1.
This tree structure is why signals, permissions and cleanup all cascade predictably.
pstree -p | head -20
ps -ef --forest | head -20
cat /proc/self/status | grep -E "^(Name|Pid|PPid)"

1. The whole family tree with PIDs — see how systemd(1) spawns everything, sshd spawns your shell, your shell
spawns your commands.
2. The same relationships in ps, with indentation showing parentage.
3. A process reading its OWN kernel record: /proc/self is a magic link to the process doing the looking.

Process states and the zombie mystery
State

Letter

Meaning

Running

R

Executing or ready to execute right
now

Sleeping

S

Waiting for something (I/O, a timer,
input) — most processes, most of the
time

Uninterruptible

D

Waiting on hardware, cannot be
killed until it returns (a stuck D
process often means a disk problem)

Stopped

T

Paused (Ctrl+Z or a debugger)

Zombie

Z

Finished, but its exit code has not
been collected by the parent yet

PRO INSIGHT: The zombie explained: when a process dies, it cannot fully vanish until its PARENT reads its exit
status (with wait). Until then it is a 'zombie' — no memory, no CPU, just a name in the table holding its exit code. A
few zombies are normal and momentary. Hundreds mean a buggy parent that forgot to collect its children — a real
bug pattern you can now diagnose on sight.





5. The CPU Scheduler — Sharing One Processor
Among Many
The illusion of simultaneity
Your machine runs hundreds of processes but has only a handful of CPU cores. How do they all seem to run
at once? The kernel's scheduler gives each process a tiny slice of CPU time — a few milliseconds — then
switches to the next, hundreds of times per second. The switching is so fast that everything APPEARS
simultaneous. This is time-sharing, and it is the scheduler's entire purpose.

The context switch
Each time the scheduler moves from one process to another, it performs a context switch: it saves the exact
state of the outgoing process (all CPU register values, the program counter) into memory, and loads the state
of the incoming one. The process being paused never notices; when its turn comes again, it resumes exactly
where it stopped, as if time had not passed.
vmstat 1 5
# the 'cs' column = context switches per second
cat /proc/interrupts | head
grep ctxt /proc/stat

1. Watch the system live; the 'cs' column counts context switches every second — often tens of thousands, invisible to
you.
2. Hardware interrupts that trigger the kernel to take control and possibly reschedule.
3. Total context switches since boot — the sheer scale of the juggling act.

Fairness and priority
The modern Linux scheduler (the Completely Fair Scheduler, and its successor) tries to give every process a
FAIR share of CPU, weighted by priority. Priority is set by niceness: a value from -20 (greedy, high priority)
to +19 (nice to others, low priority). A 'nicer' process yields more readily to others.
nice -n 10 ./heavy_job.sh
sudo renice -5 -p 1234
ps -eo pid,ni,comm --sort=ni | head

1. Start a job at low priority (+10) so it does not slow down interactive work — ideal for backups and builds.
2. Raise a running process's priority (negative needs root). Lower numbers win more CPU.
3. List processes by niceness — see which are being greedy and which are yielding.

PRO INSIGHT: Unique point: because the scheduler is preemptive and fair, a single runaway process cannot
freeze a well-configured Linux server — it just gets its fair slice while everything else keeps running. This is why a
Linux box under 100% CPU load still responds to your SSH session, where a lesser system would lock up. The
scheduler is quietly the reason Linux feels rock-solid under pressure.

Why this matters for your work





When your GoOdo backend feels slow under load, the question becomes precise: is it waiting for CPU
(scheduler saturation — check load average against core count), waiting for disk (state D, check iostat), or
waiting for the database (sleeping on a network reply)? The scheduler's vocabulary — running, ready, waiting
— turns a vague 'it's slow' into a diagnosable condition. This is the difference between guessing and
knowing.





6. Memory — Virtual Memory & the Great Illusion
The problem
Many processes run at once, each needing memory. If they all shared the same physical RAM addresses
directly, they would constantly overwrite each other, and a program written for one machine's memory layout
would not run on another. The solution is one of the deepest ideas in computing: virtual memory.

The illusion each process is given
The kernel gives EVERY process its own private, enormous, continuous view of memory — its virtual
address space — as if it alone owned the whole machine. Process A's address 0x400000 and process B's
address 0x400000 are completely different physical locations. Neither can see or touch the other's memory.
Each process lives in a perfect private bubble.
PRO INSIGHT: This is the illusion that makes modern computing possible. Each process THINKS it has the whole
machine to itself, in one clean continuous stretch of memory starting from zero. In reality the kernel and the CPU's
memory-management unit (MMU) translate these fake addresses to scattered real ones, invisibly, billions of times
per second. Isolation, security, and simplicity all flow from this one trick.

How the translation works — pages
Memory is managed in fixed chunks called pages, usually 4 kilobytes each. The kernel keeps a page table
for every process, mapping its virtual pages to physical frames in RAM. When a process reads a virtual
address, the MMU consults this table to find the real location. If the page is not currently in RAM, a page
fault occurs and the kernel fetches it.
Term

Meaning

Page

A fixed-size chunk of virtual memory (typically 4 KB)

Frame

A physical chunk of RAM the same size as a page

Page table

Per-process map from virtual pages to physical frames

Page fault

A needed page is not in RAM; the kernel must load it

MMU

Hardware that performs the translation on every access

Swapping — using disk as overflow RAM
When RAM fills up, the kernel moves less-used pages out to disk (the swap area), freeing frames for active
work. If a swapped-out page is needed again, a page fault brings it back. Swap makes the machine survive
memory pressure — slowly, but without crashing. This is exactly why Volume 1 insisted you add swap to a
small VPS.





cat /proc/meminfo | grep -E "MemTotal|MemAvailable|SwapTotal"
free -h
cat /proc/self/maps | head
sudo cat /proc/1234/smaps_rollup 2>/dev/null | head

1. The headline numbers: total RAM, genuinely available RAM, and swap size.
2. The human-readable summary. Remember: 'available' is the true figure, because Linux deliberately uses spare RAM
as disk cache.
3. A process's actual memory map — every region of its virtual address space (code, heap, stack, libraries) laid out.
4. A rolled-up memory summary for one process — real physical memory it occupies.

PRO INSIGHT: Unique point: Linux treats free RAM as WASTED RAM. Spare memory is filled with disk cache to
speed everything up, and instantly released when a program needs it. This is why new users panic at 'only 200MB
free' — they are reading the wrong number. The 'available' figure is what matters. This aggressive caching is a big
reason Linux file operations feel fast.

The out-of-memory killer
If RAM and swap are both exhausted and a process still demands more, the kernel must act or the whole
system freezes. It invokes the OOM killer, which selects and terminates the process judged 'least valuable
but most memory-hungry' to save the system. This is the 3 AM 'my backend mysteriously died' from Volume
1 — now you know the exact mechanism, and why swap and MemoryMax limits tame it.





7. The Filesystem — Inodes, VFS & the Tree
Explained
The Virtual File System — one interface for all
Linux supports dozens of filesystems (ext4, xfs, btrfs, NTFS, network filesystems, even /proc which is not a
disk at all). Yet you use the same commands — cd, ls, cat — on all of them. This works because of the
Virtual File System (VFS), a kernel layer that presents every filesystem behind one uniform interface. Your
commands talk to VFS; VFS translates to the specific filesystem underneath.
PRO INSIGHT: The VFS is why 'everything is a file' can be true. A real file on ext4, a process in /proc, a device in
/dev, a remote NFS share, a socket — all are presented through the SAME open/read/write/close interface. One set
of tools, one mental model, infinite backends. This uniformity is arguably Linux's single most powerful idea, and the
VFS is the machinery that delivers it.

The inode — a file's true identity
Here is a surprise for most people: a filename is not the file. The real file is an inode — a numbered record
holding all the file's metadata (permissions, owner, size, timestamps, and pointers to the actual data blocks
on disk). The filename is merely a link: an entry in a directory that points to an inode number. This separation
explains many otherwise-baffling behaviours.
ls -i notes.txt
stat notes.txt
df -i

1. Show the inode NUMBER of a file — its true on-disk identity.
2. The full inode contents: size, permissions, owner, all three timestamps, block count. Everything about the file
EXCEPT its name and data.
3. Show inode USAGE per filesystem. A disk can run out of inodes (too many tiny files) even with free space left — a
classic puzzling failure this explains.

Why the inode model explains everything
Puzzle

Explanation via inodes

Hard links

Two names pointing to the SAME inode — same file, two
labels

Deleting a file

You remove a NAME (link). The inode and data survive
until the LAST name is gone

A deleted file still using space

A process still holds the inode open; the name is gone but
the inode is not freed yet (Volume 1's lsof +L1 mystery)

Renaming is instant

Only the directory entry changes; the inode and gigabytes
of data never move

Permissions belong to the file, not the name

Because they live in the inode, shared by all its links





PRO INSIGHT: Unique point: because names and data are separate, moving a 100 GB file within one filesystem is
INSTANT — only the directory entry changes, the inode stays put. Across filesystems it is slow, because the data
must actually be copied to a new inode. This is why mv is sometimes instant and sometimes not — and now you
know precisely why.

Journaling — surviving a power cut
Modern filesystems like ext4 keep a journal: before making a change, they write their intention to a log. If
power fails mid-write, the journal lets the system finish or undo the half-done operation on reboot, preventing
corruption. This is why a Linux server survives an unclean shutdown far better than older systems that could
be left in a broken state.





8. The Folder System — Every Directory and Why It
Exists
One tree, and the logic behind its shape
The Linux directory layout is not arbitrary. It follows the Filesystem Hierarchy Standard (FHS), which
assigns every directory a clear purpose. The guiding principle is separation by rate of change and by
shareability: things that change often are kept apart from things that do not; machine-specific data is kept
apart from shareable data. Once you see this logic, the whole tree becomes memorable rather than a list to
cram.

The complete map
Directory

Full meaning

Why it exists / when you go there

/

root of everything

The single starting point; every path descends from here

/bin

essential binaries

Core commands (ls, cp) needed even in single-user repair mode

/sbin

system binaries

Admin commands (fdisk, ip) for root

/usr

Unix system resources

The bulk of installed software; shareable, read-mostly

/usr/bin

user binaries

Most commands you run live here

/usr/local

locally installed

Software YOU compiled/installed, kept apart from the package manager's files

/etc

et cetera (config)

ALL system configuration, as text. Your most-edited directory as an admin

/home

user homes

One private directory per human user

/root

root's home

The admin's home — deliberately NOT in /home

/var

variable data

Data that grows and changes: logs, mail, databases, caches

/var/log

logs

The first place you look when anything misbehaves

/tmp

temporary

Scratch space wiped on reboot; world-writable

/dev

devices

Hardware as files (Chapter 12)

/proc

processes

Live kernel and process state as virtual files (Chapter 3)

/sys

system

Kernel's view of devices and drivers, as files

/boot

boot files

The kernel image and bootloader — used only at startup

/lib, /lib64

libraries

Shared code that binaries in /bin and /sbin depend on

/opt

optional

Self-contained third-party applications

/mnt, /media

mount points

Where extra disks and removable drives attach

/srv

service data

Data served by the machine (web roots, ftp)

/run

runtime

Volatile runtime data (PIDs, sockets) since last boot





The organising principles, made explicit
Principle

Which directories embody it

Repairable without the main disk

/bin /sbin /lib must work when /usr is unavailable

Config separate from programs

/etc (config) vs /usr (programs) — back up /etc, reinstall
/usr

Changing data isolated

/var holds everything that grows, so the rest can be
read-only

Your stuff vs the system's stuff

/usr/local and /opt for you; /usr for the package manager

Virtual vs real

/proc /sys /run are generated live; the rest is on disk

PRO INSIGHT: Unique point: the FHS split lets a Linux system mount /usr read-only, or share ONE /usr across
many machines over a network, or keep /home on a separate encrypted disk — all because the tree cleanly
separates concerns. This modularity is why the same layout scales from a Raspberry Pi to a data-centre cluster.
The folder system is not bureaucracy; it is architecture.

A memory aid
Group them: programs (/bin /sbin /usr /opt), configuration (/etc), your data (/home /root), changing data
(/var /tmp /run), the kernel's windows (/proc /sys /dev), and attachment points (/mnt /media /boot). Six
groups, and the whole tree fits in your head.





9. The Life of a File Read — a Full Journey
Let us trace exactly what happens, layer by layer, when a program reads one line from a file. This single
walkthrough ties together every concept in this volume. Suppose your Python code runs:
open('data.txt').read().
#

Layer

What happens in detail

1

Application

Python asks to open data.txt

2

C library

Python's runtime calls the C library, which invokes the open() system call

3

Boundary

The CPU switches from user mode to kernel mode — the guarded doorway

4

Kernel: VFS

The Virtual File System receives the request and resolves the path

5

Kernel: inode

VFS walks directory entries to find data.txt's inode number, then loads the inode

6

Kernel:
permissions

The inode's permissions are checked against your process's credentials

7

Kernel: fd table

A file descriptor (say, 3) is created and returned to Python

8

Application

Python now calls read() on descriptor 3

9

Kernel: cache

The kernel checks the page cache — is this data already in RAM from a previous read?

1
0

Kernel: driver

If not cached, the block-device driver is asked for the data

1
1

Hardware

The SSD retrieves the bytes and places them in RAM via DMA

1
2

Kernel: cache

The data is cached (so the next read is instant) and copied to Python's buffer

1
3

Boundary

The CPU switches back to user mode; read() returns

1
4

Application

Python receives the bytes and hands them to your code

PRO INSIGHT: Look at what just happened: your one line of Python triggered a mode switch, a path resolution
through the VFS, an inode lookup, a permission check, a cache consultation, possibly a hardware fetch, and a
mode switch back — in microseconds, every time. Understanding this chain is what lets you reason about
performance (step 9's cache), permissions (step 6), and 'why is this slow' (steps 10–11 hitting real disk). This is the
whole volume in one journey.

Seeing the journey yourself





strace -e trace=openat,read,close python3 -c "open('data.txt').read()"
sudo cat /proc/self/io
vmtouch data.txt

1. strace shows the ACTUAL system calls your program makes — openat, read, close appear in order, exactly as steps
2–13 describe. This is theory made visible.
2. A process's I/O counters: bytes actually read from disk versus served from cache.
3. vmtouch (if installed) shows how much of a file is currently cached in RAM — step 9 made concrete.





10. System Calls — the Bridge to the Kernel
The only way in
A user-space program cannot touch hardware, cannot read a file, cannot create a process, cannot send a
network packet — not by itself. Every one of these requires kernel privilege. The system call is the sole,
controlled mechanism by which a program requests the kernel to perform a privileged action on its behalf.
There are a few hundred system calls, and astonishingly, everything a computer does reduces to them.

The essential system calls
Syscall

What it does

You know it as

open / openat

Open a file, get a descriptor

opening any file

read / write

Move bytes to/from a descriptor

all file and network I/O

close

Release a descriptor

closing a file

fork / clone

Create a new process

starting anything (Chapter 4)

execve

Replace the program in a process

running a command

wait

Collect a finished child's status

shells waiting for commands

mmap

Map memory or a file into address
space

memory allocation, loading libraries

socket / connect

Create and open network
connections

all networking

ioctl

Device-specific control

talking to hardware quirks

Watching the conversation
The strace tool from Volume 1 now reveals its true meaning: it shows the ENTIRE conversation between a
program and the kernel. Every line strace prints is one request across the user/kernel boundary. A program
IS its sequence of system calls.
strace -c ls /usr/bin
strace -f -e trace=network curl -s https://example.com -o /dev/null 2>&1 | head
strace echo hello 2>&1 | wc -l

1. A statistical summary: which system calls ls made and how many times. Even 'ls' makes hundreds — openat, read,
write, close, in loops.
2. Watch curl's network system calls: socket, connect, sendto, recvfrom — a web request laid bare as kernel requests.
3. Even a trivial 'echo hello' makes dozens of system calls just to start up, load libraries, and print. Nothing happens
without the kernel.

PRO INSIGHT: Unique point: the system-call interface is a STABLE CONTRACT that almost never breaks. A
program compiled for Linux in 1995 can often still run today because the kernel keeps its promise: 'these calls will
keep working.' Linus Torvalds enforces one rule above all — 'we do not break user space.' This
backward-compatibility discipline is a major reason Linux dominates: businesses trust that their software will keep
running for decades.









11. The Boot Process — From Power Button to Login
Booting is the reverse of everything else: instead of programs asking the kernel for services, we watch the
machine assemble itself layer by layer until it can offer those services. Each stage's only job is to start the
next.
Stage

What runs

What it does

1. Firmware

UEFI / BIOS (on the motherboard
chip)

Powers on, tests hardware, finds a bootable disk

2. Bootloader

GRUB (on the disk)

Shows the boot menu, loads the kernel and initramfs into RAM

3. Kernel init

The Linux kernel

Initialises itself, detects CPU and memory, mounts a temporary root

4. initramfs

A tiny in-RAM filesystem

Loads the drivers needed to reach the REAL root disk (e.g. LVM,
encryption)

5. Real root

The kernel again

Mounts the true root filesystem, hands control to PID 1

6. systemd

PID 1

Starts all services in dependency order, reaches the target state

7. Login

getty / display manager

Presents the login prompt or desktop

Why initramfs exists — a chicken-and-egg puzzle
Here is a subtle problem the design elegantly solves. To mount your root filesystem, the kernel needs the
right driver — but if your root disk uses LVM or encryption, that driver's config lives ON the root disk you
cannot yet mount. The initramfs breaks the deadlock: it is a small, self-contained filesystem loaded into
RAM alongside the kernel, carrying just enough drivers to reach and unlock the real root. Once the real root
is mounted, initramfs has done its job and is discarded.
systemd-analyze
systemd-analyze critical-chain
systemctl get-default
journalctl -b | head -30

1. How long each boot stage took — firmware, loader, kernel, userspace.
2. The dependency chain of the slowest path to boot completion — what held things up.
3. The target the system boots to (multi-user.target for a server, graphical.target for a desktop).
4. This boot's log from the very first message — watch the machine assemble itself in real time.

PRO INSIGHT: Unique point: each boot stage is deliberately minimal and does ONE thing — hand off to the next.
This staged design is why you can repair a broken system at any layer (Volume 1's rescue and emergency modes
drop you in BETWEEN stages). It is also why the same kernel boots identically on wildly different hardware: the
firmware and initramfs absorb the hardware differences, and by stage 6 everything looks the same.





12. Devices & Drivers — 'Everything Is a File'
Explained
Hardware as files
You have heard 'everything is a file' throughout these volumes. Chapter 12 shows the machinery. In /dev,
physical and virtual devices appear as special files. Reading or writing these files sends data to or from the
actual hardware, through its driver. This means the same read/write tools work on a disk, a serial port, or a
random-number generator.
Device file

What it is

Try it (carefully)

/dev/sda

First whole disk

sudo fdisk -l /dev/sda (inspect only)

/dev/null

The black hole — discards all input

command > /dev/null (silence output)

/dev/zero

Infinite stream of zero bytes

used to create blank files

/dev/urandom

Endless cryptographic randomness

head -c 16 /dev/urandom | base64 (a
random string)

/dev/tty

Your current terminal

echo hi > /dev/tty

/dev/loop0

A file pretending to be a disk

how disk images are mounted

Type

Character (c)

Block (b)

Data flow

One byte at a time, like a stream

In fixed-size blocks, randomly
addressable

Examples

keyboards, serial ports, /dev/random

disks, SSDs, USB drives

Seen in ls -l

first letter c

first letter b

Two kinds of device

ls -l /dev/sda /dev/null /dev/tty
head -c 20 /dev/urandom | base64
dd if=/dev/zero of=blank.img bs=1M count=10

1. The first character of each line reveals the type: b for the block-device disk, c for the character devices null and tty.
2. Pull 20 random bytes from the kernel's randomness device and encode them — instant secure password.
3. Read zeros from /dev/zero and write a 10 MB blank file — creating storage from a virtual device. dd is the low-level
copy tool.

PRO INSIGHT: Unique point: because devices are files, the ENTIRE toolset you learned — cat, dd, redirection,
permissions — works on hardware. Backing up a whole disk is cat /dev/sda > backup.img. Wiping one is cat
/dev/zero > /dev/sda. Controlling access to a device is chmod on its file. No other design gives you the whole
operating system's vocabulary for talking to hardware. This is the deepest meaning of 'everything is a file', and it is
uniquely Linux/Unix.





13. How Linux Came to Be
The lineage in one page
Understanding where Linux came from explains WHY it is shaped as it is. The story has three threads that
braid together.
Year

Event

Why it matters

1969

Unix created at Bell Labs

Established the core ideas:
everything is a file, small composable
tools, a hierarchical filesystem

1983

Richard Stallman starts GNU

A project to build a free Unix-like
system; produced bash, gcc,
coreutils (ls, cp, grep) — but lacked a
kernel

1991

Linus Torvalds writes the Linux
kernel

A Finnish student builds a free kernel
as a hobby; the missing piece GNU
needed

1992

Linux + GNU combine

The GNU tools plus the Linux kernel
form a complete free OS — properly
'GNU/Linux'

1993+

Distributions appear

Debian, Slackware, later Red Hat
and Ubuntu package it for real use

2000s

Servers and Android

Linux quietly takes over servers;
Android puts the Linux kernel in
billions of phones

Today

Runs the world

Most of the cloud, all top
supercomputers, most web servers,
and Android

PRO INSIGHT: A point of local pride: Linus Torvalds began Linux as a student in Helsinki. He famously announced
it as 'just a hobby, won't be big and professional.' It became the most widely deployed operating system in human
history. The Finnish connection is real, and you are learning it in Tampere.

Why 'free' changed everything
Linux is released under the GPL licence: anyone may use, study, modify and share it, provided they share
their changes under the same terms. This meant companies could build on it without permission or fees,
students could read every line to learn, and thousands of contributors could improve it together. The result is
a kernel developed by more people, running on more devices, than any proprietary system could match.
Openness was not charity; it was a superior development model.





14. What Makes Linux Unique — the Ideas That Won
Gathering the threads of this volume, here are the design decisions that set Linux apart. These are the
'unique points' worth being able to explain in an interview or to a colleague.

The defining ideas
Idea

What it means

Why it wins

Everything is a file

Devices, processes, kernel state, sockets — all
use the file interface

One toolset controls the entire system

Small tools, composed

Each program does one thing; pipes combine them

Infinite capability from simple parts

Text as the universal
interface

Config and data are human-readable text

Everything is scriptable, greppable,
diffable

Monolithic but modular
kernel

Fast unified core, hot-swappable drivers

Server speed with flexible hardware
support

Do not break user space

The syscall contract is kept for decades

Businesses trust software will keep
running

Open source (GPL)

Anyone can read, modify, share

Developed by more people than any
rival

Virtual memory isolation

Each process gets a private memory bubble

Security and stability by design

Fair preemptive scheduling

No process can monopolise the CPU

Stays responsive under heavy load

The /proc &amp; /sys
windows

Kernel state exposed as readable/writable files

The OS you can fully understand from
the shell

One kernel, all scales

Same code from routers to supercomputers

Learn once, apply everywhere

PRO INSIGHT: The unifying thread: Linux consistently chose SIMPLE, UNIFORM, OPEN mechanisms over clever
special cases. A file interface for everything. Text for everything. One kernel for everything. This relentless
uniformity is why a person who truly understands Linux understands the whole machine — and why your effort to
master it, rather than memorise it, is the right investment.

How this volume changes your daily work
You no longer run commands on faith. When a process hangs in state D, you know it is blocked on hardware
I/O. When free shows little 'free' memory, you know the rest is cache and you read 'available' instead. When
mv is instant, you know only the inode's directory entry changed. When a service dies at 3 AM, you know to
check the OOM killer. When something is slow, you know to ask which layer — scheduler, memory, disk, or
network. Depth turns guessing into diagnosis. That is the whole point.





15. Career Roadmap — Mastering Linux for a Living
The jobs Linux opens
Role

What you do

Linux is...

EU salary
(rough)

Linux System Administrator

Run and maintain servers, users, services,
backups

The entire job

40–60k EUR

DevOps Engineer

Automate deployment: Linux + Docker +
CI/CD + cloud + Ansible

The foundation

55–85k EUR

Site Reliability Engineer

Keep large systems fast and up; deep
debugging

The core skill

65–95k EUR

Cloud Engineer

Build on AWS / Azure / GCP

What runs underneath
all of it

55–85k EUR

Backend Engineer

Build server software (like your FastAPI work)

The deploy &amp;
debug platform

50–80k EUR

Security Engineer

Harden systems, test defences, respond to
incidents

The battleground OS

55–90k EUR

Platform / Infra Engineer

Build the internal tools other engineers deploy
on

The whole platform

60–90k EUR

The recommended path for YOU
You already have the developer half: Flutter, FastAPI, real products (GoOdo, eQuorum, Khata). Adding deep
Linux and operations makes you a full-stack-plus-infrastructure engineer — a genuinely rare and valuable
combination. The natural target is DevOps or SRE, roles that reward exactly the developer-plus-operator
profile you are building.

Learning order — from where you are to employable
Phase

Focus

Source

1. Core Linux

Command line, admin, scripting, a
real deployed server

Volumes 1–3 + capstone

2. Internals

How it works — this volume — so
you can DEBUG, not just operate

Volume 4

3. Containers

Docker deeply, then docker-compose
for real stacks

Vol. 1 Ch. 19, Vol. 2 Ch. 14

4. Automation

Ansible: turn your runbooks into
code; Git workflows

Vol. 2 Ch. 1, 13

5. Cloud

One provider (AWS or Azure); deploy
your own projects there

Provider free tier + your apps





Phase

Focus

Source

6. CI/CD

GitHub Actions: auto-test and
auto-deploy on push

Build for GoOdo / eQuorum

7. Orchestration

Kubernetes basics (k3s), monitoring
(Prometheus/Grafana)

Vol. 2 Ch. 14

Certifications — proof for employers
Cert

Level

Worth it when

LPIC-1 / CompTIA Linux+

Foundational

Your first Linux job application —
Volumes 1&amp;4 cover ~85%

RHCSA

Professional

Serious sysadmin roles; hands-on,
highly respected

AWS Solutions Architect Assoc.

Cloud

Any cloud/DevOps role — the
most-requested cloud cert

Certified Kubernetes Admin (CKA)

Advanced

Once you target senior
DevOps/platform roles

Building the portfolio that gets interviews
Certificates open doors; a portfolio gets offers. Concretely: 1) Put your deployed GoOdo backend on a real
VPS with systemd, nginx, HTTPS, backups and monitoring — then write a short blog post explaining the
setup. 2) Publish your Ansible playbook and a docker-compose stack on GitHub. 3) Keep the incident journal
from Volume 1 — real debugging stories impress interviewers more than any cert. 4) Contribute one small fix
to an open-source project to show you can work in a shared codebase. Your Aisora projects ARE your
portfolio; deploying and operating them professionally is the differentiator.
PRO INSIGHT: Your specific edge: most developers cannot operate what they build, and most sysadmins cannot
build. You are training to do both, with real products to show for it. In Finland's market and remotely across the EU,
the developer-who-can-run-production profile is in high demand and short supply. Master these four volumes,
deploy your own work on them, and you are not job-hunting — you are choosing.

The final principle
Mastery is not finishing these volumes. It is operating real systems long enough that the concepts become
instinct. Run your projects on your own servers. Break things in a VM on purpose and fix them. Write down
every incident. Teach one concept to someone else each week — teaching is the test of understanding. Do
this for a year and you will not just know Linux. You will think in it.

From silicon to shell, you now see the whole machine.
— End of Volume 4, Internals & Architecture —