7. Concurrency Mastery — Spinlocks, Mutexes, RCU,
seqlocks
The full locking toolkit
Primitive

Blocks by

Context

Best for

spinlock_t

Busy-waiting

Any (incl. IRQ)

Short critical sections

mutex

Sleeping

Process only

Longer sections, may
sleep inside

rw_semaphore

Sleeping

Process

Many readers, rare writers

seqlock

Retry (readers)

Any

Read-mostly, very fast
reads

RCU

Nothing (readers)

Any

Read-mostly, readers must
not block writers

completion

Sleeping

Process

Wait for an event to finish

Spinlock variants and the IRQ trap
spin_lock(&lock); /* basic */
spin_lock_bh(&lock); /* also disables softirqs */
spin_lock_irqsave(&lock, flags); /* also disables hardirqs, saves state */