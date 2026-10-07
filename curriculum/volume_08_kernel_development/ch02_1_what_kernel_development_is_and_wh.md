1. What Kernel Development Is — and What You
Need First
A different kind of programming
Everything in Volumes 1 through 7 lives in user space — the safe, isolated world where a crash kills only
your program. Kernel development means writing code that runs in kernel space, with full hardware access
and no safety net. A bug here does not throw an exception; it can freeze the whole machine (a kernel panic)
or silently corrupt data. This is why kernel code is written with extreme care, and why understanding Volume
4's internals first matters.
User-space program

Kernel code

Runs in

User space (ring 3)

Kernel space (ring 0)

A bug causes

That program crashes

The whole system may panic

Memory

Virtual, protected, generous

Limited, no swap, no protection

Libraries

Full C library, anything

Only kernel APIs — no printf, no
malloc

Floating point

Free to use

Generally forbidden

Debugging

gdb, print, easy

Specialised, harder

What kernel developers actually build
Area

What you write

Who needs it

Device drivers

Code to control hardware (sensors,
cards, USB)

Hardware vendors, embedded, IoT

Filesystems

New ways to store files

Storage companies

Kernel modules

Add features to a running kernel

Everyone extending the kernel

Subsystem work

Networking, scheduling, memory

Core kernel contributors

Embedded/BSP

Board support for custom hardware

Device manufacturers

What you need before starting
Requirement

Why

Your status

C programming

The kernel is written in C

Learn if needed — this volume
assumes basic C

Volume 4 (internals)

You must understand processes,
memory, VFS

You have it

A Linux machine you can crash

You WILL panic the kernel while
learning

Use a VM, never your main machine





Requirement

Why

Your status

Patience

Feedback loops are slower than user
space

The specialist's mindset

PRO INSIGHT: The one rule that saves you: NEVER develop kernel code on a machine you care about. A single
bad pointer can corrupt your filesystem or hang the box. Use a throwaway virtual machine (VirtualBox, QEMU, or a
cheap VPS you can rebuild). Take snapshots before testing. Kernel development is the one place in this entire
library where 'just try it and see' can cost you real data — so isolate ruthlessly.

Setting up your lab
sudo apt install build-essential linux-headers-$(uname -r)
sudo apt install kmod
uname -r
ls /lib/modules/$(uname -r)/build

1. build-essential gives you gcc and make; linux-headers provides the kernel's header files, needed to compile any
module against YOUR running kernel.
2. kmod provides insmod, rmmod, modprobe — the module tools.