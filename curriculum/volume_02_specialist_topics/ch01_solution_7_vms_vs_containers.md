Solution 7 — VMs vs containers
Aspect

Virtual Machine

Container

Virtualization layer

Hardware (own kernel)

Operating system (shared kernel)

Isolation

Strong

Lighter

Startup / size

Minutes / gigabytes

Milliseconds / megabytes

Best for

Different OSes, strong isolation

Dense, many small services

Solution 8 — A process stuck in state D
State D is uninterruptible sleep — the process is blocked in a system call waiting on hardware, usually disk
or network I/O, and cannot even be killed until it returns. Theoretical causes: slow or failing disk, a stuck
NFS mount, a device not responding. Practical investigation: check what it waits on with cat
/proc/PID/stack and cat /proc/PID/wchan; check disk health with iostat -xz 1 (high await, %util near 100
confirms disk); check dmesg for I/O errors; for NFS, check the server and network. The fix addresses the
hardware or mount, not the process — you usually cannot kill a D-state process; you must clear what it is
waiting on.
cat /proc/<pid>/wchan; echo
cat /proc/<pid>/stack 2>/dev/null
iostat -xz 1 3
dmesg -T | grep -iE "i/o error|nfs|timeout" | tail

1. wchan names the kernel function the process is sleeping in — often reveals the subsystem (disk, nfs).