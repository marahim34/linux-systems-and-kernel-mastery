1. Threads — Many Workers in One Process
Process versus thread
A process, you know from Volume 4, has its own private memory. Creating one is expensive, and two
processes cannot easily share data because their memory is isolated. Often you want the opposite: several
tasks running at once that DO share data — a web server handling many requests, each needing the same
in-memory cache. This is what threads provide.
A thread is a single flow of execution inside a process. One process can have many threads, and they all
share the same memory (the same heap, the same global variables, the same open files) while each keeps
its own stack and registers (its own place in the code, its own local variables).
Aspect

Process

Thread

Memory

Private, isolated

Shared with sibling threads

Creation cost

Heavy (copy address space)

Light (just a new stack)

Communication

Hard (pipes, sockets, shared mem)

Easy (shared variables)

Crash impact

Contained to that process

Can corrupt the whole process

Switching cost

Higher (change address space)

Lower (same address space)

PRO INSIGHT: The trade-off in one line: threads are fast and share easily, but that shared memory is exactly what
makes them dangerous. When two threads touch the same variable at the same time, you get the bugs that
Chapters 2 and 3 exist to prevent. Processes are safe but heavy; threads are light but sharp. Choosing between
them is a core design decision.

Why use threads at all
Reason

Example

Responsiveness

A UI thread stays responsive while a worker thread loads
data

Parallelism

Four threads on four CPU cores do four times the work

Shared state

All request-handlers see the same in-memory cache
without copying

Efficiency

Creating a thread is far cheaper than a whole process

User-level versus kernel-level threads
Threads can be managed two ways. Kernel-level threads are known to and scheduled by the kernel — a
blocked thread does not stop its siblings, and threads can run on different cores truly in parallel. User-level
threads are managed by a library inside the process, invisible to the kernel — very fast to switch, but if one
blocks on a system call, ALL of them block, and they cannot use multiple cores. Modern Linux uses kernel
threads (each is a schedulable entity), which is why your multithreaded server can use every core.





ps -eLf | head
cat /proc/$(pgrep -n python3)/status | grep Threads
top -H

1. -L shows THREADS, not just processes; the LWP column is the thread ID. One process, many rows = many threads.