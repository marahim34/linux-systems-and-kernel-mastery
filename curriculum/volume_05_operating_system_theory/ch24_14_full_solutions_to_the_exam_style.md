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