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