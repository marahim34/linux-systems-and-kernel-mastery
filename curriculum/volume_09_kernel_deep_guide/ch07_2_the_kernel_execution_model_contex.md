2. The Kernel Execution Model — Contexts You Run
In
The question that governs every line: what context am I in?
Kernel code runs in one of several contexts, and each forbids certain actions. Calling a sleeping function in
atomic context, or touching user memory from a kernel thread, is a bug that may not show up until
production. You must always know your context.
Context

When

May sleep?

May access user
memory?

Process (syscall)

Serving a syscall for a task

Yes

Yes (copy_to/from_user)

Kernel thread

A kthread you spawned

Yes

No (no user context)

Softirq/tasklet

Deferred interrupt work

No

No

Hardirq (top half)

Hardware interrupt handler

No

No

NMI

Non-maskable interrupt

No, very restricted

No

PRO INSIGHT: The 'can I sleep?' test is the master question of kernel programming. Sleeping means the scheduler
may run another task while you wait — allocating with GFP_KERNEL, taking a mutex, or calling copy_to_user can
all sleep. In ANY interrupt or atomic context, sleeping is forbidden and will trigger 'scheduling while atomic' — a
serious bug. Before every function call, know: what context am I in, and can this call sleep? This one discipline
prevents a large fraction of all kernel bugs.

Checking and enforcing context
might_sleep(); /* debug: warns if called in atomic context */
in_interrupt(); /* true if in interrupt context */
if (in_atomic()) { ... } /* detect atomic context */
preempt_disable(); preempt_enable(); /* control preemption */

1. might_sleep() is a debugging annotation: put it in functions that may sleep, and the kernel warns if they are ever
called from atomic context. A cheap early-warning system.
2. in_interrupt() tells you at runtime whether you are in interrupt context — use to choose GFP_ATOMIC vs
GFP_KERNEL if a function serves both.
3. in_atomic() detects any atomic context (interrupt or preemption-disabled).
4. preempt_disable/enable bracket code that must not be preempted — creating a small atomic section even in process
context.

Per-CPU data — avoiding locks by not sharing
A powerful kernel technique: instead of one shared variable guarded by a lock, keep a SEPARATE copy per
CPU. Each CPU touches only its own copy, so no locking is needed for the common case. This is how the
kernel scales counters and caches to hundreds of cores without contention.





DEFINE_PER_CPU(int, my_counter);
this_cpu_inc(my_counter); /* increment THIS cpu's copy, lock-free */
int total = 0;
int cpu;
for_each_possible_cpu(cpu)
total += per_cpu(my_counter, cpu); /* sum across cpus when needed */