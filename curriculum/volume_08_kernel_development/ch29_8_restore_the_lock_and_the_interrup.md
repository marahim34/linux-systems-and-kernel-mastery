8. Restore the lock AND the interrupt state together.

PRO INSIGHT: Mutex versus spinlock, the decision that defines kernel concurrency: use a MUTEX when you are in
process context and the critical section might sleep or take time — the waiter sleeps efficiently. Use a SPINLOCK
when the section is very short OR when you are in interrupt context where sleeping is impossible — the waiter
busy-spins. Choosing wrong is a classic bug: a mutex in interrupt context can hang the machine; a spinlock held too
long wastes every waiting CPU. Volume 5's theory, now with real consequences.





The deadlock rule returns
Volume 5's central lesson applies with full force: always acquire multiple locks in a consistent global order, or
you WILL deadlock two CPUs against each other. The kernel even has a runtime deadlock detector
(lockdep) that catches ordering violations during testing — enable it in your development VM.