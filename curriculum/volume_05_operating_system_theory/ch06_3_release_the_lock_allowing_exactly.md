3. Release the lock, allowing exactly one waiting thread to enter. The race is gone.

The semaphore — counting permits
A semaphore generalises the mutex to allow up to N threads at once. It holds an integer and two atomic
operations, traditionally called down (wait: if the value is above zero, decrement and proceed; else block)
and up (signal: increment, waking a waiter). A semaphore initialised to 1 behaves like a mutex; initialised to
N, it lets N threads share a resource (say, N database connections).
Semaphore type

Initial value

Use

Binary (mutex-like)

1

One-at-a-time access to a critical
region

Counting

N

Allow up to N simultaneous users of
a limited resource

Signalling

0

One thread WAITS (down) until
another SIGNALS (up)

PRO INSIGHT: The deep idea: down and up must be ATOMIC — indivisible. If two threads could run down at the
same instant, the semaphore itself would have a race condition, and we would be back where we started. The
kernel (or hardware) guarantees atomicity for these operations, and everything else builds on that foundation.
Synchronization is atomic primitives all the way down.

Seeing semaphores in Linux





ipcs -s
cat /proc/sys/kernel/sem
man 7 sem_overview