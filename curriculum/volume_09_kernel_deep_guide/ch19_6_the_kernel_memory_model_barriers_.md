6. The Kernel Memory Model — Barriers, Ordering &
atomics
The problem compilers and CPUs create
This chapter is where C/C++ programmers who have not done lock-free work meet a hard truth: the
compiler and the CPU reorder memory operations. Your writes may become visible to other CPUs in a
different order than you wrote them. In single-threaded code this is invisible; in concurrent lock-free code it
causes bugs that defy all intuition. The kernel gives you tools to control ordering explicitly.

The atomic types
atomic_t counter = ATOMIC_INIT(0);
atomic_inc(&counter);
atomic_dec(&counter);
int v = atomic_read(&counter);
if (atomic_dec_and_test(&counter)) { /* reached zero */ }
atomic_cmpxchg(&counter, old, new); /* compare-and-swap */

1. atomic_t is an integer with indivisible operations — no lock needed for the operation itself.