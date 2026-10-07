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