8. Memory Management Theory — Paging &
Replacement
Volume 4 introduced virtual memory and pages. Here is the algorithmic theory beneath it: how the kernel
decides which pages to keep in RAM and which to evict, the classic material examined in every course.

The page fault and the replacement decision
When a process accesses a page not in RAM, a page fault occurs and the kernel must load it. If RAM is full,
it must first EVICT some page to make room. WHICH page to evict is the page replacement problem, and
the choice hugely affects performance: evict a page about to be needed and you fault again immediately.
Algorithm

Evict the page that...

Note

Optimal (OPT)

will not be used for the longest future
time

Impossible (needs the future); the
ideal benchmark

FIFO

was loaded earliest

Simple / can evict a hot page; suffers
Belady's anomaly

LRU

was used least recently

Excellent / costly to track perfectly

Clock (second chance)

FIFO but skip recently-used pages

LRU-like, cheap; what real systems
approximate

PRO INSIGHT: Belady's anomaly is a famous surprise: with FIFO, giving a process MORE memory frames can
sometimes cause MORE page faults, not fewer. It defies intuition and is a favourite exam question. LRU and
Optimal never suffer it. The lesson: intuitive algorithms can hide pathological cases, which is why the theory is
studied rather than guessed.

Thrashing
If processes collectively need more active pages than RAM holds, the system spends all its time swapping
pages in and out instead of working — thrashing. Throughput collapses toward zero while the disk light
stays on. The cure is to reduce the degree of multiprogramming (run fewer processes) or add RAM. This is
the theory behind a server that grinds to a halt under memory pressure, the OOM scenario from Volume 4
seen from the algorithmic side.
vmstat 1 5 # si/so columns: pages swapped in/out per second
sar -B 1 3 # pgpgin/s, majflt/s: paging activity
cat /proc/vmstat | grep -E "pgfault|pgmajfault"