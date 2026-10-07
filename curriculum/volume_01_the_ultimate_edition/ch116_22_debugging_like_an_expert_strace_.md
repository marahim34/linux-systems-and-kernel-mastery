22. Debugging Like an Expert — strace, lsof, /proc
The principle: stop guessing, start observing
Experts don't guess why a program misbehaves — they watch it talk to the kernel. Every meaningful action a
process takes (open a file, connect a socket, read config) is a system call, and Linux lets you watch them all.

strace — the truth serum
strace -f -e trace=openat,connect python3 app.py 2>&1 | grep -v ENOENT | head
strace -f -e openat python3 app.py 2>&1 | grep -E "\.conf|\.env|\.yaml"
strace -p 1123 -e trace=network -f
strace -c ls /usr/bin