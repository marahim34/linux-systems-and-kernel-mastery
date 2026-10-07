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