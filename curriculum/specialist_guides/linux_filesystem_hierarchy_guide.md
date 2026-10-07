# Linux Filesystem Hierarchy Guide

$ ls -l /etc | head
$ file /bin/bash
$ df -h /var /tmp /home
$ cat /proc/cpuinfo
$ ls /dev | grep sd

The Linux Filesystem
Hierarchy Explained
What Every Directory Means and When You Actually Need It
Prepared for: MD Abdur -- Linux / DevOps Study Series
/etc - /var - /bin - /usr - /lib - /home - /proc - /dev - /boot - /opt

Table of Contents
Chapter 1

The Big Picture -- The Filesystem Hierarchy Standard

Chapter 2

/etc -- Configuration, the Control Room

Chapter 3

/var -- Data That Changes While the System Runs

Chapter 4

/bin, /sbin and the Great usr-merge

Chapter 5

/usr -- The Second Root

Chapter 6

/lib and /lib64 -- Shared Libraries

Chapter 7

/home and /root -- Where People Live

Chapter 8

/tmp and /var/tmp -- Temporary Storage

Chapter 9

/proc and /sys -- Windows Into the Kernel

Chapter 10

/dev -- Everything Is a File

Chapter 11

/boot -- Getting the Machine Started

Chapter 12

/opt, /srv, /media, /mnt, /run

Chapter 13

Decision Guide -- Which Directory Do I Open?

Chapter 14

Full Directory Cheat Sheet

Chapter 15

Practice Exercises

How to use this guide: think of the root filesystem as a small city. Chapters 2-12 walk through each
district in order of how often you will actually visit it. Chapter 13 is the one to bookmark -- a decision
guide for 'I need to find X, where do I look?' moments. Teal boxes are tips, amber boxes are warnings.

LINUX FILESYSTEM HIERARCHY

Mastery Guide

CHAPTER 1 -- THE BIG PICTURE

The Filesystem Hierarchy Standard
Every major Linux distribution follows the same basic map, called the Filesystem Hierarchy Standard (FHS).
Once you know what each top-level directory is FOR, you can find your way around any Linux system -Ubuntu, Fedora, Arch, or a minimal Docker container -- without relearning everything from scratch.

1.1 See it for yourself
$ ls -l /
drwxr-xr-x 2 root root 4096 bin -> usr/bin
drwxr-xr-x 10 root root 4096 boot
drwxr-xr-x 20 root root 4020 dev
drwxr-xr-x 140 root root 12288 etc
drwxr-xr-x 4 root root 4096 home
lrwxrwxrwx 1 root root 7 lib -> usr/lib
drwxr-xr-x 2 root root 4096 media
drwxr-xr-x 2 root root 4096 mnt
drwxr-xr-x 3 root root 4096 opt
dr-xr-xr-x 245 root root 0 proc
drwx------ 5 root root 4096 root
drwxr-xr-x 25 root root 820 run
drwxr-xr-x 2 root root 12288 sbin -> usr/sbin
drwxr-xr-x 8 root root 4096 srv
dr-xr-xr-x 13 root root 0 sys
drwxrwxrwt 18 root root 4096 tmp
drwxr-xr-x 14 root root 4096 usr
drwxr-xr-x 13 root root 4096 var

1.2 The one-line meaning of every top directory
Directory

One-line meaning

/etc

System-wide configuration files -- almost always plain text

/var

Data that changes while the system runs: logs, caches, spools, databases

/bin, /sbin

Essential command binaries (now symlinked into /usr)

MD Abdur -- Linux / DevOps Study Series

Page 3

Directory

One-line meaning

/usr

The bulk of installed software: programs, libraries, docs, icons

/lib, /lib64

Shared libraries needed by /bin and /sbin binaries

/home

Personal directories for every regular user

/root

Home directory for the root user specifically

/tmp

Temporary files, usually cleared on reboot

/proc

Virtual filesystem exposing live kernel and process information

/sys

Virtual filesystem exposing kernel devices and drivers

/dev

Device files -- disks, terminals, USB, random number generator

/boot

Kernel image, initramfs, and bootloader configuration

/opt

Optional, self-contained third-party software packages

/srv

Data served by this system, e.g. web or FTP content

/media, /mnt

Mount points for removable and manually mounted filesystems

/run

Runtime data since last boot -- PIDs, sockets, locks

TIP
You do not need to memorize this table today. Read it once now, then use Chapter 13's decision guide
whenever you are unsure -- the table will make more sense every time you come back to it.

1.3 Two different kinds of directories
It helps to sort the table above into two mental buckets:
• Real, persistent data -- /etc, /var, /usr, /home, /boot, /opt, /srv. This is actual content stored on disk.
• Virtual, kernel-generated views -- /proc, /sys, and (mostly) /dev, /run. These do not hold real files on
disk; the kernel builds their contents live, in memory, every time you look.
WARNING
Never try to 'clean up' /proc or /sys like a normal directory, and never cp -r them anywhere. Their
apparent size is meaningless -- they are windows into kernel memory, not real files.

CHAPTER 2 -- /etc

Configuration, the Control Room
/etc holds almost every system-wide configuration file on the machine. If you need to change how a service
behaves, /etc is nearly always where you start looking.

2.1 Why the name 'etc'
Historically 'et cetera' -- a catch-all for anything that wasn't a program or a user's own data. Today it has a
very specific meaning: static, host-specific configuration, almost always human-readable text.

2.2 Files you already know from Chapter-level user management
/etc/passwd # user accounts
/etc/shadow # password hashes
/etc/group # groups
/etc/sudoers # sudo rules

2.3 Other essentials inside /etc
Path

What it configures

/etc/hostname

The machine's hostname

/etc/hosts

Manual hostname-to-IP mappings, checked before DNS

/etc/fstab

Which filesystems get mounted automatically at boot, and where

/etc/resolv.conf

DNS resolver settings (often auto-generated, do not hand-edit on most
distros)

/etc/network/ or
/etc/netplan/

Network interface configuration (Debian/Ubuntu variants)

/etc/ssh/sshd_config

SSH server behavior -- ports, root login, key auth

/etc/systemd/system/

Custom and overridden systemd service unit files

/etc/apt/sources.list

Package repository sources (Debian/Ubuntu)

/etc/yum.repos.d/

Package repository sources (RHEL/Fedora)

Path

What it configures

/etc/crontab,
/etc/cron.d/

System-wide scheduled jobs

/etc/environment

System-wide environment variables

/etc/nginx/,
/etc/apache2/

Web server configuration, per package

/etc/skel/

Template files copied into every new user's home directory by useradd
-m

2.4 A pattern worth noticing: PROGRAM.conf vs PROGRAM.d/
Many packages ship a single file (e.g. nginx.conf) plus a matching directory ending in .d (e.g.
/etc/nginx/conf.d/) where you drop extra snippet files instead of editing the main one. You already
saw this exact pattern with /etc/sudoers.d/ in the user management guide.
TIP
Before editing any file in /etc, make a quick backup: sudo cp /etc/nginx/nginx.conf{,.bak}.
Most config-heavy tools also ship a syntax checker -- e.g. nginx -t, visudo -c, sshd -t -- run it
before restarting the service.

2.5 Try it
$ ls /etc | wc -l # how many top-level config items exist
$ cat /etc/os-release # which distro and version am I on
$ cat /etc/hostname
$ grep -v '^#' /etc/fstab | grep -v '^$' # active mount rules, comments stripped

CHAPTER 3 -- /var

Data That Changes While the System Runs
If /etc is the control room, /var is the machine's diary and inbox -- logs, mail, print queues, databases, and
package caches. The name means 'variable': content here is expected to grow and change constantly,
unlike /etc or /usr.

3.1 The main subdirectories
Path

Contents

/var/log/

System and application logs -- your first stop when something breaks

/var/spool/

Queued work waiting to be processed: mail, print jobs, cron

/var/cache/

Regenerable cached data, e.g. downloaded package files (apt/dnf cache)

/var/lib/

Persistent state for applications -- databases, package manager state

/var/tmp/

Temporary files that should survive a reboot (unlike /tmp)

/var/www/

Common convention for web server document roots (not FHS-mandated)

/var/mail/

Local user mailboxes

/var/run/

Legacy path, now usually a symlink to /run

3.2 /var/log -- your first debugging stop
$ ls /var/log
auth.log syslog nginx/ apt/ dpkg.log kern.log
$ sudo tail -f /var/log/syslog # live system log stream
$ sudo journalctl -u nginx -f # live logs for a specific systemd service
$ sudo journalctl -b # everything logged since last boot
$ sudo grep 'Failed password' /var/log/auth.log # failed SSH login attempts

TIP
Modern systemd systems keep most logs in a binary journal, viewed with journalctl, in addition to
(or instead of) the plain-text files under /var/log. Use both -- journalctl for filtering by service and time,
/var/log files for grep-friendly searching.

3.3 /var/lib -- where applications keep their state
/var/lib/mysql/ # MySQL/MariaDB database files
/var/lib/postgresql/ # PostgreSQL database files
/var/lib/docker/ # Docker images, containers, volumes
/var/lib/apt/ # APT package manager's local database
/var/lib/dpkg/ # Debian package installation records

WARNING
Never manually delete files inside /var/lib// to 'free up space' -- these directories hold live application
state, and deleting the wrong file can corrupt a database or break the package manager. Use each
application's own cleanup tools instead.

3.4 Watching /var grow
$ du -sh /var/log /var/cache /var/lib/docker 2>/dev/null
$ df -h /var # is /var on its own partition and how full is it

TIP
On servers you manage long-term (like a VPS running eQuorum or PinePeak's backend), an
unrotated log file is a classic cause of a full disk. Check /etc/logrotate.d/ to confirm logs are
being rotated and compressed automatically.

CHAPTER 4 -- /bin, /sbin

and the Great usr-merge
These directories hold the actual command-line programs you run every day. Modern distributions have
quietly restructured them -- worth understanding so 'ls -l /bin' doesn't confuse you.

4.1 The traditional split
Path

Historically held

/bin

Essential commands for ALL users: ls, cp, mv, cat, bash

/sbin

Essential commands mainly for the ADMINISTRATOR: fdisk, reboot, ifconfig

/usr/bin

Non-essential commands for all users -- most installed software

/usr/sbin

Non-essential admin commands

The idea was that /bin and /sbin had to work even if /usr was a separate partition that failed to mount -- so
the bare minimum to repair the system lived outside /usr.

4.2 The usr-merge
Most modern distributions (Ubuntu, Fedora, Arch, Debian since Bullseye) have merged these: /bin, /sbin,
and /lib are now just symlinks pointing into /usr/bin, /usr/sbin, and /usr/lib. The historical split no longer
reflects where files actually live -- only where compatibility expects to find them.
$ ls -l /bin
lrwxrwxrwx 1 root root 7 Jul 1 10:02 /bin -> usr/bin
$ ls -l /sbin
lrwxrwxrwx 1 root root 8 Jul 1 10:02 /sbin -> usr/sbin

TIP
This means /bin/bash and /usr/bin/bash are literally the same file today on most systems -- the
distinction is legacy. Scripts using either path still work everywhere.

4.3 Finding out what a command actually is
$ which passwd
/usr/bin/passwd

$ file /usr/bin/passwd
/usr/bin/passwd: ELF 64-bit LSB pie executable, x86-64...
$ type cd
cd is a shell builtin

type is worth knowing separately from which: some commands like cd, echo, and export are shell builtins
with no file on disk at all -- which will not find them, but type will.

CHAPTER 5 -- /usr

The Second Root
/usr ('Unix System Resources', not 'user') is where the majority of installed software actually lives -- it is
effectively a second, larger root directory nested inside the first.

5.1 /usr's own internal structure
Path

Contents

/usr/bin

Almost every command-line program on the system (post usr-merge)

/usr/sbin

Admin-focused commands

/usr/lib

Libraries and internal support files for programs in /usr/bin

/usr/share

Architecture-independent shared data: man pages, icons, documentation, locale
data

/usr/include

C/C++ header files, needed when compiling software from source

/usr/local

Software installed manually/outside the package manager -- see below

/usr/src

Kernel and other source trees

5.2 /usr/local -- the 'not managed by the package manager' zone
When you compile something from source, or manually download a binary that isn't packaged for your
distro, convention says it belongs under /usr/local, not directly in /usr. This keeps hand-installed software
clearly separated from what apt/dnf manages, so a package upgrade never silently overwrites it.
/usr/local/bin/ # manually installed executables
/usr/local/lib/ # manually installed libraries
/usr/local/share/ # manually installed shared data

TIP
Many 'curl | bash' install scripts for developer tools drop their binary into /usr/local/bin -- that's exactly
why it exists.

5.3 man pages live in /usr/share/man

$ man useradd # reads from /usr/share/man/man8/useradd.8.gz
$ whatis useradd # one-line summary
$ man -k password # search man page descriptions for 'password'

5.4 Why /usr matters for containers
In minimal Docker images you will often see /usr holding almost everything, with /bin and /sbin as thin
symlinks, exactly as described in Chapter 4. Recognizing this layout instantly in a stripped-down container
image is a useful skill on its own.

CHAPTER 6 -- /lib, /lib64

Shared Libraries
Programs rarely contain everything they need in a single file. Instead, they link against shared libraries at
runtime -- and this is where those libraries live.

6.1 What a shared library is
A shared library (.so file, 'shared object') holds reusable code that many different programs link against
instead of each bundling its own copy. This keeps binaries small and lets a security fix in one library patch
every program that uses it, with a single update.

6.2 Inspecting a binary's dependencies
$ ldd /usr/bin/passwd
linux-vdso.so.1
libpam.so.0 => /usr/lib/x86_64-linux-gnu/libpam.so.0
libc.so.6 => /usr/lib/x86_64-linux-gnu/libc.so.6
/lib64/ld-linux-x86-64.so.2

If ldd reports 'not found' for any library, the program will fail to start -- this is the single most common cause
of a mysterious 'command not found'-looking error that is actually a missing dependency, not a missing
command.

6.3 /lib64 specifically
On 64-bit systems, /lib64 traditionally held 64-bit libraries while /lib held 32-bit compatibility libraries (or vice
versa depending on distro convention). Like /bin and /sbin, both are now typically symlinks into /usr/lib and
/usr/lib64 after the usr-merge.
$ ls -l /lib64
lrwxrwxrwx 1 root root 10 Jul 1 10:02 /lib64 -> usr/lib64

6.4 ldconfig and the library cache
The dynamic linker doesn't search every library directory on every program launch -- it uses a cache built by
ldconfig. If you manually install a library in a non-standard path, you may need to register it:
$ sudo ldconfig # rebuild the library cache

$ ldconfig -p | grep libssl # is a given library registered
$ cat /etc/ld.so.conf.d/*.conf # extra directories ldconfig also scans

CHAPTER 7 -- /home, /root

Where People Live
Every account's personal files, settings, and downloads live in one of these two places.

7.1 /home -- regular users
Every regular user (UID 1000+, as covered in the user management guide) gets a subdirectory under /home
by default, created from the /etc/skel template when useradd -m runs.
$ ls /home
abdur
$ ls -la ~
.bashrc .profile .ssh/ .config/ .cache/ Documents/ Downloads/

Typical dotfile / dir

Purpose

~/.bashrc

Per-user shell configuration, aliases, prompt customization

~/.profile

Environment setup, sourced by login shells

~/.ssh/

SSH keys and known_hosts -- must stay mode 700

~/.config/

Modern convention for per-application configuration

~/.cache/

Modern convention for per-application cache data

~/.local/share/

Modern convention for per-application persistent data

7.2 /root -- the superuser's home
root's home directory is deliberately kept OUTSIDE /home, at /root, for one very practical reason: if /home is
a separate partition or network mount and fails to mount, root still needs a working home directory to log in
and fix the problem.
$ ls -ld /root
drwx------ 5 root root 4096 Jul 10 08:00 /root

WARNING

/root is mode 700 -- only root can even list its contents. This is intentional and should never be
widened.

7.3 XDG Base Directory convention
The .config / .cache / .local/share split you see under a user's home follows the XDG Base Directory spec,
which most modern desktop and CLI tools now respect instead of scattering dozens of dotfiles directly in the
home directory root.

CHAPTER 8 -- /tmp, /var/tmp

Temporary Storage
Two directories for short-lived files, with one crucial difference: how long they last.

8.1 /tmp
World-writable scratch space for any program or user. On many modern systems /tmp is mounted as tmpfs
-- backed by RAM, not disk -- and is always cleared on reboot.
$ ls -ld /tmp
drwxrwxrwt 18 root root 4096 Jul 13 10:00 /tmp
# note the sticky bit 't' at the end -- see below

8.2 The sticky bit, explained
/tmp is writable by everyone, which would normally let any user delete any other user's files in it. The sticky
bit (that trailing t in the permission string) changes the rule: in a sticky directory, you may only delete or
rename a file if you own it (or you are root), regardless of directory write permission.
$ chmod +t /some/shared/dir # set the sticky bit manually
$ chmod 1777 /some/shared/dir # same thing, numeric form (leading 1)

8.3 /var/tmp -- the one that survives reboot
/var/tmp exists for temporary files that need to persist across a reboot, unlike /tmp. Package managers and
some installers use it for exactly that reason -- files there are only expected to be cleaned up after a longer
period (commonly 30 days), not on every restart.
/tmp

/var/tmp

Survives reboot?

Usually not (often tmpfs/RAM)

Yes

Typical cleanup

On boot, or via systemd-tmpfiles

Periodic, e.g. every 30 days

Good for

Short-lived scratch files, sockets, lock
files

Downloads/installers that span a
reboot

TIP

Check current tmp cleanup policy with cat /etc/systemd/tmpfiles.d/tmp.conf or
systemd-tmpfiles --cat-config.

CHAPTER 9 -- /proc, /sys

Windows Into the Kernel
These two directories look like ordinary folders full of files, but nothing in them is stored on disk. The kernel
generates their contents on demand, live, purely in memory.

9.1 /proc -- process and kernel information
$ cat /proc/cpuinfo | grep 'model name' | head -1
$ cat /proc/meminfo | head -5
$ cat /proc/version
$ ls /proc | grep -E '^[0-9]+$' | head # every currently running process, by PID
$ cat /proc/1/status | head # detailed info about PID 1 (init/systemd)
$ cat /proc/uptime

Every running process gets a numbered subdirectory under /proc for the duration of its life. Tools like ps,
top, and free are not magic -- they are simply reading and formatting files from /proc.

9.2 Tuning the kernel live through /proc/sys
$ cat /proc/sys/net/ipv4/ip_forward # is IP forwarding on (0 or 1)
$ sudo sysctl -w net.ipv4.ip_forward=1 # the safe, documented way to change it
$ sysctl -a | head # list every tunable kernel parameter

WARNING
You CAN write directly to files under /proc/sys with sudo tee, but changes made that way vanish on
reboot. Use sysctl with a file in /etc/sysctl.d/ for anything that should persist.

9.3 /sys -- devices and drivers
/sys exposes the kernel's internal model of every device, bus, and driver on the system -- a more structured,
modern counterpart to some of what /proc historically covered.
$ ls /sys/class/net/ # every network interface the kernel knows about
$ cat /sys/class/power_supply/BAT0/capacity # battery percentage, on a laptop
$ cat /sys/block/sda/size # size of a block device, in 512-byte sectors

9.4 Why this matters day to day
• Diagnosing hardware: what CPU, memory, disks, and network interfaces does this box actually have
• Debugging a stuck process: reading /proc/PID/status and /proc/PID/fd without extra tools
• Tuning performance and network behavior via sysctl-managed kernel parameters
• Understanding what commands like free, lscpu, and lsblk are reading under the hood

CHAPTER 10 -- /dev

Everything Is a File
One of Unix's defining ideas: hardware devices are represented as files, so you can often interact with them
using the exact same tools you use for ordinary files.

10.1 What lives in /dev
$ ls /dev | head -15
sda sda1 sr0 tty0 tty1 null zero
random urandom loop0 fuse stdin stdout stderr

Device file

What it represents

/dev/sda, /dev/nvme0n1

Whole physical disks (SATA/SCSI, NVMe)

/dev/sda1, /dev/sda2

Individual partitions on a disk

/dev/tty1, /dev/pts/0

Terminals -- physical console and pseudo-terminals (SSH sessions)

/dev/null

Discards everything written to it; reading it returns end-of-file instantly

/dev/zero

Reading it produces an endless stream of zero bytes

/dev/random,
/dev/urandom

Sources of random bytes for cryptography and scripts

/dev/loop0

Loop devices -- lets you mount a file (like an .iso) as if it were a disk

10.2 Practical uses you'll actually run into
$ command > /dev/null 2>&1 # silence a command's output entirely
$ sudo dd if=/dev/zero of=testfile bs=1M count=100 # create a 100MB test file
$ lsblk # friendlier view of /dev block devices
$ sudo fdisk -l /dev/sda # partition table of a specific disk

10.3 udev -- how /dev populates itself
Like /proc and /sys, /dev is dynamically managed by the kernel and the udev daemon -- plug in a USB drive
and a new /dev/sdb entry appears within milliseconds, no reboot needed. udev rules (in /etc/udev/rules.d/)

can assign consistent, friendly names to devices instead of relying on the assignment order, which can
change between boots.

CHAPTER 11 -- /boot

Getting the Machine Started
The small set of files needed before the rest of the filesystem is even usable: the kernel itself, and the
bootloader that finds and launches it.

11.1 What's inside
$ ls /boot
vmlinuz-6.8.0-generic # the compressed Linux kernel image
initrd.img-6.8.0-generic # initial RAM disk -- drivers needed before real root
mounts
grub/ # GRUB bootloader configuration and files
config-6.8.0-generic # the exact kernel build configuration
System.map-6.8.0-generic # kernel symbol table, used for debugging

11.2 The boot sequence, briefly
• 1. Firmware (BIOS or UEFI) runs a power-on self test, then hands control to the bootloader
• 2. GRUB (or systemd-boot) reads its config from /boot/grub/, shows the boot menu, loads the chosen
kernel (vmlinuz) and initramfs into memory
• 3. The kernel unpacks, uses the initramfs to load the drivers it needs to find the real root filesystem, then
mounts it
• 4. Control passes to PID 1 -- systemd on most modern distributions -- which starts every other service

11.3 Checking your current kernel
$ uname -r
6.8.0-generic
$ ls /boot/vmlinuz-* # every kernel version currently installed

WARNING
Never delete files from /boot by hand unless you are certain they belong to an old, unused kernel
version, and never delete the one matching uname -r. Use your package manager's own autoremove
function to clean up old kernels safely.

TIP -- WSL note

Inside WSL, /boot is mostly a formality -- WSL uses its own lightweight boot process managed by
Windows, not GRUB. Don't be surprised if /boot looks nearly empty there.

CHAPTER 12 -- THE REST

/opt, /srv, /media, /mnt, /run
Five smaller directories, each with one clear, narrow job.

12.1 /opt -- self-contained third-party software
For large, self-contained packages that don't want to scatter files across /usr's shared directories.
Convention: each package gets its own subdirectory, e.g. /opt/google/chrome/.
$ ls /opt
google/ microsoft/ vendor-app/

12.2 /srv -- data this machine serves to others
Meant for the actual content a server hosts -- website files, FTP data. Less universally used than /opt or
/var/www in practice, but you'll see it on servers that follow FHS strictly.
/srv/www/example.com/ # a virtual host's document root
/srv/ftp/ # anonymous FTP content

12.3 /media vs /mnt -- two kinds of mounting
Directory

Used for

/media

Automatic mounts -- USB drives, CDs, SD cards, typically handled by the desktop
or udisks

/mnt

Manual, temporary mounts -- an admin running mount by hand for a one-off task

$ lsblk # see available disks/partitions
$ sudo mount /dev/sdb1 /mnt # manually mount a partition
$ sudo umount /mnt # unmount it when done

12.4 /run -- data since the last boot

A tmpfs (RAM-backed) directory for runtime state that only makes sense for the current boot: process ID
files, Unix sockets, and locks. It replaced the older /var/run, which is now usually just a symlink to it.
$ ls /run
systemd/ lock/ sudo/ sshd.pid utmp

TIP
If a service refuses to start complaining about a stale PID or lock file, /run is usually where to look -and since it's tmpfs, a reboot always clears it completely.

CHAPTER 13 -- DECISION GUIDE

Which Directory Do I Open?
The question you asked at the start of this: 'which one do I open when'. Here is a practical lookup, organized
by the QUESTION you actually have, not by directory name.
I need to...

Look in...

A service won't start, why?

/var/log or journalctl -u <service>, then check its config
in /etc/<service>/

I need to change how a program behaves

/etc -- look for /etc/<program>/ or /etc/<program>.conf

The disk is full, what's using space?

/var/log, /var/cache, /var/lib/docker are the usual
suspects

Where is my personal data / downloads?

/home/<you>/

I need to check CPU, memory, or a running
process

/proc -- or the friendlier top, free, ps wrapping it

Is a USB drive or disk recognized?

/dev (lsblk), then mount under /media or /mnt

Which kernel am I running?

/boot, or uname -r

Where did apt/dnf install this program's binary?

/usr/bin or /usr/sbin (check with which)

Where are this program's libraries?

/usr/lib, verify with ldd on the binary

I compiled something from source, where does
it go?

/usr/local/bin, /usr/local/lib

A cron job or print job is queued, where is it?

/var/spool/

I need scratch space for a script

/tmp for short-lived, /var/tmp if it must survive reboot

Where does a systemd service store its
runtime PID/socket?

/run

A large third-party app I installed manually

/opt

13.1 A 3-question mental checklist
• Is it configuration? -> /etc
• Is it changing/growing data (logs, cache, queue, database)? -> /var
• Is it a program or its supporting files? -> /usr (or /opt if it's a large standalone app)

Most files on a Linux system fall into one of those three buckets. /home, /proc, /dev, and /boot cover the
remaining special cases, and each has exactly one job as shown in the earlier chapters.

CHAPTER 14 -- CHEAT SHEET

Full Directory Cheat Sheet
A single-page reference of every directory covered, for quick lookup.
Directory

Contains

Change often?

/etc

System configuration files

Rarely, by hand

/var/log

Logs

Constantly

/var/spool

Queued jobs (mail, print, cron)

Constantly

/var/cache

Regenerable cached data

Constantly

/var/lib

Application/database state

Constantly

/usr/bin, /usr/sbin

Installed program binaries

On install/update

/usr/lib

Shared libraries

On install/update

/usr/share

Docs, man pages, icons, locale data

On install/update

/usr/local

Manually/source-installed software

Occasionally, by
hand

/home/<user>

Personal files and settings

Constantly

/root

root's home directory

Rarely

/tmp

Short-lived scratch files

Constantly, cleared
on reboot

/var/tmp

Scratch files surviving reboot

Occasionally

/proc

Live kernel/process info (virtual)

Always, in real time

/sys

Live kernel/device info (virtual)

Always, in real time

/dev

Device files

As hardware is
plugged/unplugged

/boot

Kernel, initramfs, bootloader

Only on kernel
updates

/opt

Large standalone third-party apps

On install

/srv

Data this machine serves

As content updates

Directory

Contains

Change often?

/media

Auto-mounted removable media

As devices are
inserted

/mnt

Manual temporary mounts

As you mount things

/run

Runtime state since last boot

Constantly, cleared
on reboot

CHAPTER 15 -- PRACTICE

Practice Exercises
Work through these on your own machine, WSL, or a disposable VM. They are designed to build the instinct
of 'where do I look' rather than just testing memorization.
1. Map the root
Run ls -l / and identify which top-level entries are real directories and which are symlinks (look for the ->
arrow). Note which ones point into /usr.
2. Find a config file
Pick any installed service (nginx, ssh, or cron) and locate its main configuration file under /etc. Open it and
identify at least 3 settings.
3. Read a log
Use journalctl -u ssh (or sshd) to view recent SSH activity. Then find the equivalent plain-text log file under
/var/log and compare.
4. Track down disk usage
Run du -sh /var/* 2>/dev/null | sort -h and identify the largest subdirectory. Explain in one sentence what it's
used for, using Chapter 3.
5. Binary or builtin?
Run type cd, type ls, and type echo. Explain why some show a path and others say 'shell builtin'.
6. Library dependencies
Run ldd /bin/ls and identify at least 2 libraries it depends on. Locate one of those library files on disk.
7. /proc exploration
Find your shell's own PID with echo $$, then read /proc//status and report its VmRSS (memory usage)
value.
8. Device files
Run lsblk, then find the matching device file for your main disk under /dev. What partition is mounted as /?
9. Kernel check
Run uname -r, then confirm a matching vmlinuz file exists under /boot.
10. Decision drill
Without looking at Chapter 13, write down where you'd look to answer: 'a cron job seems stuck', 'a program I
built from source isn't found by which', and 'the root partition is almost full'. Then check your answers against
Chapter 13.

CLOSING NOTE
The filesystem hierarchy stops feeling arbitrary once you see it as three questions: is this
configuration, changing data, or a program? Every directory in this guide answers one of those
questions, and that's the whole system.

