# Volume 5: Operating System Theory

LINUX MASTERY
VOLUME 5 — OPERATING
SYSTEM THEORY
The Deep Concepts Every Computer Scientist Must Know — Threads,
Synchronization,
Deadlocks, Scheduling Algorithms, Classic Problems, Virtualization & I/O —
Explained from First Principles and Connected to Real Linux

Bridging Tanenbaum-level theory with hands-on Linux · TAMK Operating Systems
companion
Prepared for MD Abdur Rahim · Tampere, Finland · 2026





Table of Contents — Volume 5
1. Threads — Many Workers in One Process
2. The Synchronization Problem — Race Conditions
3. Mutual Exclusion — Locks, Mutexes & Semaphores
4. Higher-Level Tools — Monitors, Condition Variables & Message Passing
5. Classic Synchronization Problems
6. Deadlocks — When Everyone Waits Forever
7. CPU Scheduling Algorithms — the Full Catalogue
8. Memory Management Theory — Paging & Replacement
9. File System Design — How It's Built Underneath
10. Input / Output — How the Kernel Talks to Devices
11. Virtualization & the Cloud — the Theory
12. OS Design Principles & Exam-Style Problems
13. Worked Examples — Every Concept Solved Step by Step
14. Full Solutions to the Exam-Style Problems





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
2. How many threads a given process currently has, straight from its kernel record.
3. top in thread mode (-H) shows individual threads and their CPU use — see a multithreaded program spread across
cores.

PRO INSIGHT: Linux detail worth knowing: to the Linux kernel a thread and a process are almost the same thing —
both are 'tasks' created by clone(). A process is just a task with its own memory; a thread is a task that SHARES
memory with its creator. This unified model (unusual among operating systems) is why Linux threading is efficient
and why fork and thread-creation share machinery. It is a recurring Linux theme: one clean mechanism instead of
two special cases.
PRACTICE EXERCISES
1. Run a multithreaded program (even python3 -c 'import threading...'), then watch it with ps -eLf and top -H.
2. Read /proc/PID/status Threads count for your browser or a server process.
3. Explain in your own words why two threads sharing a counter is risky but two processes are not.





2. The Synchronization Problem — Race Conditions
The bug that only sometimes happens
Suppose two threads share a counter and both run counter = counter + 1. That single line is actually three
machine steps: READ the value, ADD one, WRITE it back. Now imagine the timing goes wrong:
Time

Thread A

1

reads counter (5)

2

Thread B

5
reads counter (5)

3

adds 1 -> 6

4
writes 6

6

5
5

adds 1 -> 6

5

counter

5
6

writes 6

6

Two increments happened, but the counter went from 5 to 6, not 7. One update was lost. This is a race
condition: the result depends on the exact, unpredictable timing of threads. It might work a million times and
fail on the million-and-first, which makes these the hardest bugs to catch.
PRO INSIGHT: The defining feature of a race condition: it is non-deterministic. The same code, same input, gives
different results depending on microscopic timing you cannot control or reproduce. This is why 'it works on my
machine' and why concurrency bugs terrify experienced engineers. The whole field of synchronization exists to
make concurrent code deterministic again.

The critical region
The dangerous code — the part that touches shared data — is called the critical region (or critical section).
The entire solution to race conditions is a single rule: only one thread may be inside the critical region at
a time. This property is called mutual exclusion. If we can guarantee it, the race disappears.

What a correct solution must guarantee
Requirement

Meaning

Mutual exclusion

No two threads in the critical region at once

Progress

If the region is free, a waiting thread may enter (no
needless blocking)

Bounded waiting

A thread cannot be made to wait forever while others go
ahead

No assumptions

Correctness must not depend on CPU speed or thread
count

These four conditions, stated by Tanenbaum, are the yardstick against which every locking mechanism in the
next chapter is measured. A solution that provides mutual exclusion but allows starvation (violating bounded
waiting) is still broken.





PRACTICE EXERCISES
1. Describe a real race condition in a web app (hint: two requests both check 'is this username taken?' then both
create it).
2. Identify the critical region in the counter example and state why exactly one thread may be inside it.
3. Explain why testing rarely catches race conditions but production traffic does.





3. Mutual Exclusion — Locks, Mutexes &
Semaphores
The naive attempts and why they fail
Before the real tools, understand what does NOT work. Simply disabling interrupts is unsafe on multi-core
machines and too powerful to hand to user programs. Busy-waiting on a shared flag (spinning in a loop
checking 'is it free yet?') wastes CPU and can still race unless the check-and-set is atomic — indivisible. The
hardware provides an atomic instruction (test-and-set) that the real tools are built upon.

The mutex — the basic lock
A mutex (mutual exclusion lock) has two states, locked and unlocked, and two operations: lock (if free, take
it and enter; if taken, wait) and unlock (release it, waking a waiter). Wrap the critical region between lock and
unlock and mutual exclusion is guaranteed.
lock(mutex) # wait here until the lock is free, then take it
counter = counter + 1 # critical region: now safe, we are alone
unlock(mutex) # release; a waiting thread may now proceed

1. Acquire the lock. Only one thread succeeds; others block here until it is released.
2. The critical region runs with a guarantee that no other thread is inside it.
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

1. List active System V semaphores on the machine — real programs using them right now.
2. The kernel's semaphore limits.
3. The POSIX semaphore API overview — sem_wait (down) and sem_post (up) are the functions your programs call.

PRACTICE EXERCISES
1. Fix the counter race by wrapping it in lock/unlock, on paper, and trace the two-thread timeline again.
2. Design a semaphore setup for a system allowing at most 3 concurrent downloads. What initial value?
3. Explain why a signalling semaphore starts at 0, not 1.





4. Higher-Level Tools — Monitors & Message
Passing
Why semaphores are not enough
Semaphores work, but they are error-prone: forget one up, or order two down operations wrongly, and you
get a deadlock or a race that is nearly impossible to find. The operations are scattered through the code with
nothing tying them together. Higher-level constructs package the discipline so the compiler or runtime helps
you get it right.

Monitors
A monitor bundles shared data together with the procedures that operate on it, and guarantees that only
one thread executes inside the monitor at a time — the mutual exclusion is automatic, built into the
construct. You do not write lock/unlock; entering any monitor procedure locks it, leaving unlocks it. Java's
synchronized keyword and Python's with lock: are monitors in practice.
# conceptual monitor
monitor BankAccount {
balance = 0
procedure deposit(n) { balance = balance + n } # auto-exclusive
procedure withdraw(n){ balance = balance - n } # auto-exclusive
}

1. The monitor wraps the data...
2. ...and its operations. The runtime ensures only one thread is inside ANY of these procedures at once, so balance can
never be corrupted by a race. The programmer cannot forget to lock, because locking is the construct itself.

Condition variables
Sometimes a thread inside a monitor must WAIT for a condition (a consumer waiting for the buffer to be
non-empty). Condition variables provide wait (release the monitor and sleep until signalled) and signal
(wake a waiting thread). They let threads coordinate on events, not just guard data.

Message passing — sharing nothing
A completely different philosophy: instead of sharing memory and protecting it, share nothing and
communicate by sending messages. Two processes exchange data through send and receive
operations. There is no shared state to race over. This is how separate machines cooperate (there is no
shared memory across a network), and the model behind Go's channels and the actor model.
Approach

Philosophy

Real examples

Shared memory + locks

Share data, protect access

Threads, mutexes, monitors

Message passing

Share nothing, send copies

Pipes, sockets, Go channels, actors





PRO INSIGHT: A famous principle from the Go language captures the shift: 'Do not communicate by sharing
memory; instead, share memory by communicating.' Message passing trades the raw speed of shared memory for
safety and scalability — no locks to forget, and it works across machines. Understanding both models, and when
each fits, is what separates a coder from a systems engineer.

mkfifo /tmp/mypipe
echo "hello" > /tmp/mypipe &
cat /tmp/mypipe

1. Create a named pipe — a message-passing channel in the filesystem.
2. One process sends a message into it (backgrounded, it waits for a reader).
3. Another process receives it. No shared memory, no locks: pure message passing, which you can try right now.

PRACTICE EXERCISES
1. Map three tools you use to the two models: Python threading.Lock, a Unix pipe, a socket.
2. Explain why message passing works across a network but shared-memory locks do not.
3. Try the mkfifo example; then have two terminals talk through one named pipe.





5. Classic Synchronization Problems
These three problems appear in every OS course and interview because each isolates one hard aspect of
concurrency. Solving them teaches the patterns you will reuse forever.

The Producer-Consumer (bounded buffer)
A producer thread makes items and puts them in a fixed-size buffer; a consumer takes them out. The
challenges: the producer must WAIT when the buffer is full, the consumer must WAIT when it is empty, and
they must not corrupt the buffer by accessing it simultaneously. The classic solution uses three semaphores:
Semaphore

Initial value

Purpose

mutex

1

Protects the buffer from simultaneous
access

empty

N

Counts free slots; producer waits on
it when full

full

0

Counts filled slots; consumer waits
on it when empty

The producer does: down(empty), down(mutex), add item, up(mutex), up(full). The consumer mirrors it:
down(full), down(mutex), remove item, up(mutex), up(empty). The two counting semaphores handle waiting;
the binary mutex handles exclusion. This exact pattern underlies every job queue and message broker.
PRO INSIGHT: Order matters critically: the producer takes down(empty) BEFORE down(mutex). Reverse them and
you get deadlock — a producer holding the mutex while waiting for space, and a consumer needing the mutex to
make space. This single ordering lesson is why the problem is taught: it shows that correct primitives, combined
wrongly, still fail.

The Readers-Writers problem
A database may be READ by many threads at once safely, but a WRITE must be exclusive. The goal: allow
multiple simultaneous readers, but give a writer sole access. The tension is fairness — a stream of readers
can STARVE a writer that never gets its turn. Solutions must balance concurrency against starvation, exactly
the trade-off in real database locking.

The Dining Philosophers
Five philosophers sit around a table, one fork between each pair. A philosopher needs BOTH neighbouring
forks to eat. If all five grab their left fork at once, each waits forever for a right fork that never comes — total
deadlock. This tiny problem captures the essence of deadlock and its cures.
Solution

Idea

Resource ordering

Number the forks; always pick up the lower-numbered
first — breaks the circular wait

Limit diners

Allow at most 4 at the table of 5, so at least one can
always eat





Solution

Idea

Ask permission

A waiter (arbitrator) grants forks, preventing the bad
global state

PRO INSIGHT: Why Dining Philosophers endures: it is the smallest possible system that shows ALL FOUR
deadlock conditions at once (Chapter 6). Fix any one condition and the deadlock is impossible. It is a complete
deadlock laboratory in a sentence, which is why every OS course returns to it.
PRACTICE EXERCISES
1. Write the producer and consumer semaphore sequences from memory and check the ordering.
2. Explain how a burst of readers can starve a writer, and one way to prevent it.
3. Apply resource ordering to the philosophers: show why numbering forks breaks the deadlock.





6. Deadlocks — When Everyone Waits Forever
What a deadlock is
A deadlock is a state where a set of processes are all blocked, each waiting for a resource held by another
in the set. Nobody can proceed, nobody will release, and the wait is eternal. The dining philosophers each
holding one fork is the picture. Deadlock is not slowness; it is permanent, mutual paralysis.

The four necessary conditions (Coffman conditions)
Tanenbaum's central result: a deadlock can occur ONLY IF all four of these hold at once. Break any single
one and deadlock becomes impossible. This is the master key to the whole topic.
Condition

Meaning

Break it by...

Mutual exclusion

A resource is held by only one
process at a time

Making resources shareable (not
always possible)

Hold and wait

A process holds one resource while
waiting for another

Requiring all resources be requested
at once

No preemption

A resource cannot be forcibly taken
away

Allowing the system to reclaim
resources

Circular wait

A closed chain of processes each
waits for the next

Ordering resources; always request
in that order

PRO INSIGHT: The most practical takeaway of the entire volume: to prevent deadlock, break CIRCULAR WAIT by
always acquiring locks in a fixed global order. If every thread grabs lock A before lock B, never the reverse, a cycle
cannot form. This one rule prevents the vast majority of real-world deadlocks in databases and multithreaded code.
Remember it above all else.

The four strategies for dealing with deadlock
Strategy

Approach

Used when

Ostrich algorithm

Ignore it; reboot if it happens

Deadlocks are rare and cheap to
recover (many OSes!)

Prevention

Design so a condition can never hold

Correctness is critical; lock ordering
is the common form

Avoidance

Grant requests only if a safe state
remains (Banker's algorithm)

Resource needs are known in
advance

Detection &amp; recovery

Let them happen, detect cycles, then
break them

Databases: detect and kill one victim
transaction

The Banker's algorithm in one paragraph
Avoidance works by never entering an unsafe state. Before granting a resource request, the system asks: 'if
I grant this, does there still exist SOME order in which all processes can finish?' If yes, the state is safe and





the request is granted; if no, the requester waits. It is called the Banker's algorithm because it mirrors a
banker who only lends if all clients could still be satisfied. It is elegant but needs advance knowledge of
maximum needs, which is why real systems more often use detection.

Deadlock in real Linux
# PostgreSQL detects deadlocks automatically and kills a victim:
# ERROR: deadlock detected
# DETAIL: Process 123 waits for ShareLock on transaction 456...
gdb -p <hung_pid> # inspect a suspected deadlocked process
cat /proc/<pid>/status | grep State # 'D' state can signal a lock wait

1. Databases implement DETECTION: PostgreSQL finds the cycle, aborts one transaction, and reports it — you have
likely seen this error. Now you know the theory behind it.
2. For a hung multithreaded program, a debugger shows each thread's stack — two threads each waiting on a lock the
other holds is a deadlock, visible directly.
3. A process stuck in state D or endlessly sleeping on a lock is the operational signature of the theory.

PRACTICE EXERCISES
1. For each of the four conditions, give a concrete example from the dining philosophers.
2. Show how fixed lock ordering breaks circular wait in a two-lock program.
3. Explain why 'detection and recovery' suits databases but 'prevention' suits flight-control software.





7. CPU Scheduling Algorithms — the Full Catalogue
Volume 4 explained THAT the scheduler time-shares the CPU. This chapter explains the ALGORITHMS it
can use to decide who runs next, the classic material of every OS course. Each optimises a different goal,
and understanding the trade-offs is the point.

The goals a scheduler juggles
Metric

Meaning

Who cares

Throughput

Jobs finished per unit time

Batch/server systems

Turnaround time

Total time from submission to
completion

Batch systems

Response time

Time from request to first response

Interactive systems

Fairness

Every process gets a just share

All systems

CPU utilisation

Keeping the CPU busy

Efficiency

These goals conflict. Optimising throughput can hurt response time; perfect fairness can hurt throughput.
Each algorithm below picks a side.

The algorithms
Algorithm

Rule

Strength / Weakness

FCFS

First come, first served (a queue)

Simple / one long job delays
everyone (convoy effect)

SJF

Shortest job first

Optimal average wait / needs to
know job lengths; starves long jobs

SRTF

Shortest remaining time (preemptive
SJF)

Great turnaround / same starvation,
more switching

Round Robin

Each gets a fixed time slice, then
rotate

Fair, responsive / slice size is critical

Priority

Highest priority runs first

Flexible / low-priority jobs can starve

MLFQ

Multiple queues; jobs move between
them by behaviour

Adapts to job type / complex to tune

Round Robin and the time-slice trade-off
Round Robin gives each process a quantum (time slice), then preempts it and moves to the next. The
quantum size is a delicate balance: too LONG and it degrades toward FCFS (poor response); too SHORT
and the CPU spends all its time context-switching instead of working. Typical Linux quanta are a few
milliseconds — long enough to do real work, short enough to feel instant.





PRO INSIGHT: The starvation theme unifies this chapter: any algorithm that always favours some jobs (SJF
favours short ones, Priority favours important ones) can leave others waiting forever. The cure is AGING —
gradually raising a waiting job's priority so it eventually runs. Linux's real scheduler is a fair, priority-with-aging
design (CFS), precisely to get the benefits of priority WITHOUT the starvation. Theory meets your running machine.

Worked example — compare the algorithms
Three jobs arrive at time 0: A needs 24 ms, B needs 3 ms, C needs 3 ms. Under FCFS (order A,B,C)
average wait is (0+24+27)/3 = 17 ms. Under SJF (order B,C,A) average wait is (0+3+6)/3 = 3 ms. Same jobs,
same CPU — scheduling ALONE cut average waiting from 17 to 3. This is why the algorithm matters, and a
classic exam calculation.
chrt -p $$
sudo chrt -f 50 ./realtime_task
ps -eo pid,cls,pri,ni,comm | head

1. Show the scheduling policy and priority of your current shell.
2. Run a task under a REAL-TIME policy (SCHED_FIFO, priority 50) — for work that must never be delayed.
3. See every process's scheduling class (cls), priority and niceness — the catalogue above, live on your machine.

PRACTICE EXERCISES
1. Compute average waiting and turnaround for jobs (6,8,7,3 ms) under FCFS and SJF; compare.
2. Explain the convoy effect and how Round Robin avoids it.
3. Describe how aging prevents starvation in a priority scheduler.





8. Memory Management Theory — Paging &
Replacement
Volume 4 introduced virtual memory and pages. Here is the algorithmic theory beneath it: how the kernel
decides which pages to keep in RAM and which to evict, the classic material examined in every course.

The page fault and the replacement decision
When a process accesses a page not in RAM, a page fault occurs and the kernel must load it. If RAM is full,
it must first EVICT some page to make room. WHICH page to evict is the page replacement problem, and
the choice hugely affects performance: evict a page about to be needed and you fault again immediately.
Algorithm

Evict the page that...

Note

Optimal (OPT)

will not be used for the longest future
time

Impossible (needs the future); the
ideal benchmark

FIFO

was loaded earliest

Simple / can evict a hot page; suffers
Belady's anomaly

LRU

was used least recently

Excellent / costly to track perfectly

Clock (second chance)

FIFO but skip recently-used pages

LRU-like, cheap; what real systems
approximate

PRO INSIGHT: Belady's anomaly is a famous surprise: with FIFO, giving a process MORE memory frames can
sometimes cause MORE page faults, not fewer. It defies intuition and is a favourite exam question. LRU and
Optimal never suffer it. The lesson: intuitive algorithms can hide pathological cases, which is why the theory is
studied rather than guessed.

Thrashing
If processes collectively need more active pages than RAM holds, the system spends all its time swapping
pages in and out instead of working — thrashing. Throughput collapses toward zero while the disk light
stays on. The cure is to reduce the degree of multiprogramming (run fewer processes) or add RAM. This is
the theory behind a server that grinds to a halt under memory pressure, the OOM scenario from Volume 4
seen from the algorithmic side.
vmstat 1 5 # si/so columns: pages swapped in/out per second
sar -B 1 3 # pgpgin/s, majflt/s: paging activity
cat /proc/vmstat | grep -E "pgfault|pgmajfault"

1. Sustained non-zero si/so means active swapping — the machine may be thrashing.
2. Detailed paging statistics: major faults (needing disk) are the expensive ones.
3. Lifetime fault counters: minor faults (in memory) are cheap; major faults (from disk) are what hurt.

PRACTICE EXERCISES
1. Trace FIFO and LRU on the reference string 1,2,3,4,1,2,5,1,2,3,4,5 with 3 frames; count faults.
2. Explain thrashing and two ways to cure it.
3. Why is Optimal impossible to implement, yet still useful to study?





9. File System Design — How It's Built Underneath
Volume 4 covered inodes and the VFS from the user's side. Here is how a filesystem is actually DESIGNED
— how it tracks which disk blocks belong to which file, the core of the file-systems course.

How a file's blocks are tracked
Method

Idea

Weakness

Contiguous

Store each file in consecutive blocks

Fast reads / fragmentation, hard to
grow files

Linked list

Each block points to the next

No fragmentation / slow random
access, pointers waste space

FAT

Linked list moved into one table in
memory

Better random access / table grows
with disk

Inodes (indexed)

Each file has an index block listing its
blocks

Fast, scalable / the Unix/Linux choice

The inode's clever multi-level index
An inode stores the first several block addresses directly (fast access to small files). For larger files, it points
to single, double, and triple indirect blocks — index blocks that point to more index blocks. This design
gives instant access to small files while still supporting enormous ones, all from a fixed-size inode. It is a
beautiful piece of engineering worth understanding once.
Pointer type

Reaches

Good for

Direct (x12)

The first ~48 KB directly

Small files (the majority)

Single indirect

One index block of pointers

Medium files

Double indirect

Index of indexes

Large files

Triple indirect

Index of indexes of indexes

Huge files

PRO INSIGHT: Why this design won: most files are small, and the direct pointers make them instant. But the same
structure scales to terabyte files through indirection, WITHOUT wasting space on small files or imposing a size limit.
It optimises the common case while gracefully handling the rare one — a hallmark of great systems design, and the
reason the inode has survived fifty years.

Free space and consistency
The filesystem also tracks which blocks are FREE (usually with a bitmap: one bit per block, set if used). And
it must stay CONSISTENT across crashes — the job of the journal from Volume 4, which logs intended
changes before making them so a power cut cannot leave the structure half-updated.
PRACTICE EXERCISES
1. Explain why contiguous allocation is fast to read but painful to grow.
2. Trace how the inode reaches block number 100,000 of a huge file through indirection.





3. Why does storing many tiny files sometimes exhaust inodes before disk space?





10. Input / Output — How the Kernel Talks to Devices
The three ways to do I/O
Method

How

Cost

Programmed I/O

CPU polls the device in a loop until
ready

Wastes CPU entirely while waiting

Interrupt-driven

CPU does other work; device
INTERRUPTS when ready

Efficient; an interrupt per chunk

DMA

A controller moves data to RAM
directly, interrupts once at the end

CPU freed almost entirely

The evolution is a story of freeing the CPU. Early systems polled (wasteful). Interrupts let the CPU work while
waiting. Direct Memory Access (DMA) lets a dedicated controller shuttle data straight into RAM, interrupting
the CPU only when the whole transfer is done. This is how your SSD fills memory in the Volume 4 file-read
journey without the CPU copying every byte.

Interrupts — the device's way to get attention
An interrupt is a hardware signal that makes the CPU pause its current work, jump to a kernel interrupt
handler, deal with the device, then resume exactly where it left off. Interrupts are how a keyboard press, a
completed disk read, or an arriving network packet reach the kernel instantly, without the CPU constantly
checking. Chapter 5's context switch and this are close cousins.
cat /proc/interrupts | head
watch -n1 "cat /proc/interrupts | grep -E 'eth|nvme'"
vmstat 1 3 # the 'in' column counts interrupts per second

1. The interrupt table: each device's interrupt count per CPU core.
2. Watch network and disk interrupts climb live as you generate traffic — the theory made visible.
3. System-wide interrupt rate; alongside context switches, the pulse of kernel activity.

PRO INSIGHT: The buffering insight: the kernel sits between fast devices and slow ones (and between applications
and hardware) using BUFFERS and CACHES. The page cache from Volume 4 is exactly this — data read once
stays buffered in RAM so the next read skips the slow device. I/O theory is largely the art of hiding slow hardware
behind fast memory. Every layer buffers.
PRACTICE EXERCISES
1. Order the three I/O methods by CPU efficiency and explain why DMA wins.
2. Watch /proc/interrupts while pinging a host; identify the network card's rising count.
3. Explain how buffering lets a fast process and a slow disk coexist without the process waiting on every byte.





11. Virtualization & the Cloud — the Theory
What virtualization really is
Volume 2 used Docker; here is the theory. Virtualization lets one physical machine present itself as many
independent virtual machines, each believing it has its own hardware. A hypervisor is the layer that creates
and manages them, playing for whole operating systems the role an OS plays for processes: it shares real
hardware among guests that think they are alone.
Type

Runs on

Examples

Trade-off

Type 1 (bare metal)

Directly on hardware

VMware ESXi, Xen, KVM

Fast; runs the cloud

Type 2 (hosted)

On top of a host OS

VirtualBox, VMware
Workstation

Convenient; a bit slower

Virtual machines versus containers
Two ways to isolate workloads, at different layers. A virtual machine virtualises the HARDWARE — each
VM runs a full guest OS with its own kernel (heavy, strongly isolated). A container (Volume 1 Ch. 19)
virtualises the OPERATING SYSTEM — all containers share the host kernel but get isolated views via
namespaces and cgroups (light, fast, less isolated). Choosing between them is a core cloud-design decision.
Virtual Machine

Container

Virtualises

Hardware

The operating system

Contains

A full guest OS + kernel

Just the app and its libraries

Size / start

Gigabytes / minutes

Megabytes / milliseconds

Isolation

Strong (separate kernels)

Lighter (shared kernel)

Use

Different OSes, strong isolation

Many small services, density

PRO INSIGHT: The cloud in one sentence: providers buy huge physical machines, slice them into VMs with Type-1
hypervisors, and rent you the slices by the hour. Your Hetzner VPS is one such slice. Containers then pack many
services INTO each VM. The entire cloud economy rests on this two-level virtualization — hardware into VMs, VMs
into containers. Understanding it is understanding the industry you are entering.
PRACTICE EXERCISES
1. Explain why a Type-1 hypervisor is faster than Type-2.
2. For each: 'run Windows on Linux', 'pack 50 microservices densely' — choose VM or container and justify.
3. Describe how your VPS and Docker together are the two layers of cloud virtualization.





12. OS Design Principles & Exam-Style Problems
The principles that recur
Across every chapter, the same design wisdom appears. These are the ideas Tanenbaum returns to, worth
carrying into your own engineering.
Principle

Meaning

Separate mechanism from policy

Build the mechanism flexible; let policy decide how it is
used (the scheduler runs tasks; the policy picks which)

Optimise the common case

Make frequent operations fast, rare ones merely correct
(inode direct pointers)

Keep it simple

Complexity breeds bugs; the kernel stays as small as it
can

Provide abstractions

Processes, files, address spaces hide messy reality
behind clean models

Atomic primitives

Build safety on small indivisible operations, then compose

Fail safely

Journals, safe states, and detection assume things WILL
go wrong

Exam-style problems to test yourself
Work these on paper; they integrate the whole volume and mirror real exam and interview questions.
#

Problem

1

Two threads increment a shared counter 1000 times
each. Explain why the final value may be under 2000, and
fix it with a mutex.

2

Given jobs with burst times 8,4,9,5 arriving together,
compute average waiting time under FCFS and SJF.

3

State the four Coffman conditions and, for each, describe
one prevention technique.

4

Trace page faults for reference string 7,0,1,2,0,3,0,4 with
3 frames under FIFO and LRU.

5

Write the producer-consumer solution with three
semaphores and explain why down(empty) precedes
down(mutex).

6

Explain Belady's anomaly and name two algorithms
immune to it.

7

Contrast VMs and containers on virtualization layer,
isolation, and startup cost.





#

Problem

8

A process sits in state D for minutes. List the theoretical
and practical causes and how you would investigate.

How this volume connects to the others
Volumes 1–3 taught you to USE Linux. Volume 4 showed HOW Linux works. This volume explains WHY
operating systems are built this way at all — the universal theory beneath every OS, Linux included. Together
they take you from typing commands to understanding the machine at every level, from a shell prompt down
to the algorithms scheduling your CPU and the semaphores guarding your data. That complete picture is
what mastery means, and what makes you rare.

Theory explains why; practice proves you understand. Now you have both.
— End of Volume 5, Operating System Theory —

13. Worked Examples — Every Concept Solved Step
by Step
Theory is only understood when you can DO it. This chapter works each key technique fully, showing every
step of the reasoning. Follow along with pen and paper; redo each one yourself afterwards.

Worked Example 1 — A race condition and its fix
Problem: Two threads each run counter = counter + 1 one thousand times. counter starts at 0. What can
the final value be, and why?
Step 1 — see the hidden three operations. The line is not atomic. In machine terms it is: LOAD counter
into a register; ADD 1; STORE the register back. Three separate steps that can be interrupted between.
Step 2 — trace one bad interleaving (counter currently 41):
Time

Thread A

t1

LOAD 41

t2
t3

ADD -> 42

41
41

ADD -> 42
STORE 42

t6

counter
41

LOAD 41

t4
t5

Thread B

41
42

STORE 42

42

Two increments occurred, but counter rose by only 1. One update was lost.
Step 3 — the answer. The final value can be anything from 1000 (worst case, almost every increment
collides) up to 2000 (perfect, no collisions). It is non-deterministic.
Step 4 — the fix. Put the three-step operation inside a critical region guarded by a mutex:





lock(m)
counter = counter + 1
unlock(m)

1. Acquire the lock; any second thread blocks here.
2. The LOAD-ADD-STORE now runs with no other thread able to interleave.
3. Release; the next thread proceeds. Final value is now ALWAYS exactly 2000.

Why it works: mutual exclusion makes the three hidden steps behave as one indivisible step. The
interleaving from Step 2 becomes impossible because Thread B cannot LOAD until Thread A has unlocked,
by which time A has already STORED.

Worked Example 2 — Producer-Consumer, fully traced
Problem: A buffer holds 3 slots. Write the producer and consumer using semaphores, and show why the
ordering of operations matters.
Step 1 — the three semaphores:
Semaphore

Start

Meaning

mutex

1

Guards the buffer itself

empty

3

Number of free slots

full

0

Number of filled slots

Step 2 — the correct code:
# PRODUCER # CONSUMER
down(empty) down(full)
down(mutex) down(mutex)
put_item() take_item()
up(mutex) up(mutex)
up(full) up(empty)

1. Producer first waits for a free slot (empty), THEN takes the buffer lock.
2. Consumer first waits for an item (full), THEN takes the buffer lock.
3. Each modifies the buffer under mutex.
4. Each releases the buffer lock.
5. Producer signals a new item is available; consumer signals a new slot is free.

Step 3 — why order matters (the deadlock trap). Suppose the producer reversed the first two lines:
down(mutex) THEN down(empty). Trace it: the buffer is full (empty = 0). The producer takes the mutex, then
blocks on down(empty), waiting for a free slot. But the consumer needs the mutex to remove an item and free
a slot, and the producer is holding it. Neither can proceed: deadlock. The correct order (count first, lock
second) prevents holding the lock while waiting for space.

Worked Example 3 — Scheduling calculations
Problem: Four jobs arrive together at time 0 with CPU burst times A=6, B=8, C=7, D=3 (ms). Compute
average waiting time under FCFS and under SJF.
FCFS runs them in arrival order A, B, C, D. Waiting time = how long each waits before it starts:





Job

Starts at

Waiting time

A (6)

0

0

B (8)

6

6

C (7)

14

14

D (3)

21

21

Average waiting = (0 + 6 + 14 + 21) / 4 = 41 / 4 = 10.25 ms.
SJF runs shortest first: order D(3), A(6), C(7), B(8):
Job

Starts at

Waiting time

D (3)

0

0

A (6)

3

3

C (7)

9

9

B (8)

16

16

Average waiting = (0 + 3 + 9 + 16) / 4 = 28 / 4 = 7 ms.
PRO INSIGHT: Result: same four jobs, same CPU, but scheduling alone dropped average waiting from 10.25 ms to
7 ms — a 32% improvement, just by choosing the order. This is why SJF is provably optimal for average waiting
time, and why the algorithm matters. The catch, as the theory warned: SJF needs to know burst times in advance
and can starve long jobs.

Worked Example 4 — Round Robin with a quantum
Problem: Jobs A=6, B=3, C=4 arrive at time 0. Use Round Robin with quantum = 2 ms. When does each
finish?
Trace the rotation (each gets 2 ms, then goes to the back of the queue if work remains):
Time

Running

Remaining after

0-2

A

A=4, B=3, C=4

2-4

B

A=4, C=4, B=1

4-6

C

A=4, B=1, C=2

6-8

A

B=1, C=2, A=2

8-9

B

C=2, A=2 (B DONE at 9)

9-11

C

A=2 (C DONE at 11)

11-13

A

(A DONE at 13)

Finish times: B at 9, C at 11, A at 13. Notice Round Robin spread the CPU fairly — no job waited the whole
time for others to finish, unlike FCFS. That responsiveness is its purpose, paid for with more context
switches.

Worked Example 5 — Page replacement, frame by frame




Problem: Reference string 7, 0, 1, 2, 0, 3, 0, 4 with 3 frames. Count page faults under FIFO and LRU.
FIFO (evict the oldest-loaded page). F = fault:
Ref

Frame1

Frame2

Frame3

Fault?

7

7

-

-

F

0

7

0

-

F

1

7

0

1

F

2

2

0

1

F (evict 7, oldest)

0

2

0

1

hit

3

2

3

1

F (evict 0, now
oldest)

0

2

3

0

F (evict 1)

4

4

3

0

F (evict 2)

FIFO faults = 7.
LRU (evict the least-recently-USED page):
Ref

Frame set (most recent last)

Fault?

7

7

F

0

70

F

1

701

F

2

012

F (evict 7, least recent)

0

120

hit (0 now most recent)

3

203

F (evict 1)

0

230

hit

4

304

F (evict 2)

LRU faults = 6. LRU beat FIFO by one fault here, because it kept the frequently-used page 0 instead of
blindly evicting by age. This is the typical result: LRU approximates the ideal by betting that recently-used
pages will be used again.

Worked Example 6 — Applying the four conditions
Problem: Two threads. Thread 1 locks A then wants B. Thread 2 locks B then wants A. Show the deadlock
and fix it.
The deadlock:
Time

Thread 1

Thread 2

t1

lock A (got it)

lock B (got it)

t2

wants B... waits

wants A... waits





Time

Thread 1

Thread 2

t3

blocked forever

blocked forever

Check the four conditions: mutual exclusion (locks are exclusive) YES; hold-and-wait (each holds one,
wants another) YES; no preemption (cannot steal a held lock) YES; circular wait (1 waits for 2 waits for 1)
YES. All four hold, so deadlock is possible — and here it happened.
The fix — break circular wait with lock ordering. Impose a global rule: ALWAYS lock A before B. Now
Thread 2 must also take A first:
# BOTH threads follow the same order:
lock(A)
lock(B)
# ... work ...
unlock(B)
unlock(A)

1. Every thread acquires A before B, without exception.
2. Now if Thread 2 wants both, it must get A first — but Thread 1 holds A, so Thread 2 waits at A WITHOUT holding B.
3. Thread 1 can therefore get B, finish, and release. No cycle can form.
4. This single discipline eliminates the deadlock class entirely.

PRO INSIGHT: This is the most useful practical result in the whole volume: order your locks consistently and an
entire category of deadlocks becomes impossible. Real database systems, kernels, and multithreaded applications
live by this rule. If you remember one solution from Volume 5, make it this one.





14. Full Solutions to the Exam-Style Problems
Complete worked answers to the eight problems in Chapter 12. Attempt each yourself first, then check.

Solution 1 — Shared counter
The final value may be below 2000 because counter = counter + 1 is three non-atomic steps (load, add,
store); two threads can load the same value and one increment is lost (Worked Example 1). It can range from
1000 to 2000. Fix: guard the line with a mutex (lock/unlock), forcing the three steps to run indivisibly, giving
exactly 2000 every time.

Solution 2 — FCFS vs SJF for bursts 8, 4, 9, 5
FCFS order 8, 4, 9, 5. Start times 0, 8, 12, 21. Waiting = 0+8+12+21 = 41; average = 10.25 ms.
SJF order 4, 5, 8, 9. Start times 0, 4, 9, 17. Waiting = 0+4+9+17 = 30; average = 7.5 ms. SJF wins, as theory
predicts.

Solution 3 — The four conditions and their prevention
Condition

Prevention technique

Mutual exclusion

Make resources shareable where possible (e.g. read-only
data needs no exclusive lock)

Hold and wait

Require a process to request ALL its resources at once,
up front

No preemption

Allow the system to take a resource back (roll back a
transaction)

Circular wait

Impose a global ordering; always request resources in
that order

Solution 4 — Page faults for 7,0,1,2,0,3,0,4 (3 frames)
Worked in Example 5: FIFO = 7 faults, LRU = 6 faults. LRU wins by keeping the frequently referenced page
0.

Solution 5 — Producer-Consumer and the ordering
Full code in Worked Example 2. down(empty) must precede down(mutex) so a producer never holds the
buffer lock while waiting for a free slot. Reversing them lets a full buffer deadlock: producer holds mutex
waiting for space, consumer needs mutex to free space.

Solution 6 — Belady's anomaly
Belady's anomaly: under FIFO, ADDING frames can INCREASE page faults, contrary to intuition. It happens
because FIFO's eviction (by age) does not respect actual usage, so more frames can change the eviction
pattern for the worse. Reference string 1,2,3,4,1,2,5,1,2,3,4,5 is the classic demonstration (more faults with 4
frames than 3). Immune algorithms: LRU and Optimal (OPT), because they are 'stack algorithms' whose
page set with N frames is always a subset of that with N+1 frames.