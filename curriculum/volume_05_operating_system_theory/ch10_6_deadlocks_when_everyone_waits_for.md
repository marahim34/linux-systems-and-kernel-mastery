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