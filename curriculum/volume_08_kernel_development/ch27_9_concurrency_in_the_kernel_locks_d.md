9. Concurrency in the Kernel — Locks Done Right
Why the kernel is a concurrency minefield
This is where Volume 5's theory becomes urgent reality. Many CPUs run kernel code SIMULTANEOUSLY.
Interrupts can preempt your code at any moment. Two processes can enter your driver at once. Shared data
— a counter, a list, a buffer — WILL be corrupted by races (Volume 5, Chapter 2) unless you protect it.
Kernel concurrency bugs are among the hardest in all of computing.

The locking primitives
Primitive

Use when

Can it sleep?

Mutex

Protecting data in process context

Yes — the holder may sleep

Spinlock

Short critical sections, or interrupt
context

NO — it busy-waits

atomic_t

A single counter

N/A — lock-free atomic ops

RCU

Read-mostly data, high performance

Advanced

#include <linux/mutex.h>
static DEFINE_MUTEX(my_lock);
mutex_lock(&my_lock);
shared_data++; /* critical section */
mutex_unlock(&my_lock);
#include <linux/spinlock.h>
static DEFINE_SPINLOCK(my_slock);
unsigned long flags;
spin_lock_irqsave(&my_slock, flags);
shared_list_add(item); /* critical section, IRQ-safe */
spin_unlock_irqrestore(&my_slock, flags);