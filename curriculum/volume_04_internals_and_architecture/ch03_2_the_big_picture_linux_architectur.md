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