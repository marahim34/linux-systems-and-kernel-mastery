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