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