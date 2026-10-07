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