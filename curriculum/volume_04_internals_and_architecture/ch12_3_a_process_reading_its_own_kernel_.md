3. A process reading its OWN kernel record: /proc/self is a magic link to the process doing the looking.

Process states and the zombie mystery
State

Letter

Meaning

Running

R

Executing or ready to execute right
now

Sleeping

S

Waiting for something (I/O, a timer,
input) — most processes, most of the
time

Uninterruptible

D

Waiting on hardware, cannot be
killed until it returns (a stuck D
process often means a disk problem)

Stopped

T

Paused (Ctrl+Z or a debugger)

Zombie

Z

Finished, but its exit code has not
been collected by the parent yet

PRO INSIGHT: The zombie explained: when a process dies, it cannot fully vanish until its PARENT reads its exit
status (with wait). Until then it is a 'zombie' — no memory, no CPU, just a name in the table holding its exit code. A
few zombies are normal and momentary. Hundreds mean a buggy parent that forgot to collect its children — a real
bug pattern you can now diagnose on sight.