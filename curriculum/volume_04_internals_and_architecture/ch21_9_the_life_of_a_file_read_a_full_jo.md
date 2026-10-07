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