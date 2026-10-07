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