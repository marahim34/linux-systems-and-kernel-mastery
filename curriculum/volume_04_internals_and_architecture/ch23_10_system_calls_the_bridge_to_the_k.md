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