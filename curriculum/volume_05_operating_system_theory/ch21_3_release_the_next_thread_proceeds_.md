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