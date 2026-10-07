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