3. Mutual Exclusion — Locks, Mutexes &
Semaphores
The naive attempts and why they fail
Before the real tools, understand what does NOT work. Simply disabling interrupts is unsafe on multi-core
machines and too powerful to hand to user programs. Busy-waiting on a shared flag (spinning in a loop
checking 'is it free yet?') wastes CPU and can still race unless the check-and-set is atomic — indivisible. The
hardware provides an atomic instruction (test-and-set) that the real tools are built upon.

The mutex — the basic lock
A mutex (mutual exclusion lock) has two states, locked and unlocked, and two operations: lock (if free, take
it and enter; if taken, wait) and unlock (release it, waking a waiter). Wrap the critical region between lock and
unlock and mutual exclusion is guaranteed.
lock(mutex) # wait here until the lock is free, then take it
counter = counter + 1 # critical region: now safe, we are alone
unlock(mutex) # release; a waiting thread may now proceed