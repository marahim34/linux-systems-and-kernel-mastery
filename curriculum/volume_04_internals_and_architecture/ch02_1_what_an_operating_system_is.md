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