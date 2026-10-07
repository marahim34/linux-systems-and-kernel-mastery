# Tier 4 · Chapter 4: Kernel Concurrency, Locking & RCU

Synthesized from *Linux Mastery* Volume 9 & Robert Love Ch. 9-10.

## 1. Concurrency Sources in the Kernel
Code in the kernel can be interrupted and interleaved by:
1. Symmetric Multiprocessing (SMP): multiple CPU cores running kernel code simultaneously.
2. Kernel Preemption: a higher priority task preempting running kernel code.
3. Interrupts (IRQs): hardware interrupts firing at any time.
4. Bottom halves: softirqs and tasklets.

## 2. Locking Primitives
- **Spinlocks (`spinlock_t`)**: Busy-waiting lock. Must be used in interrupt context where sleeping is prohibited! NEVER call sleeping functions (like `msleep()` or `copy_to_user()`) while holding a spinlock!
- **Mutexes (`struct mutex`)**: Sleeping lock. Used in process context when critical section may sleep or block on I/O.
- **Atomic Operations (`atomic_t`)**: Hardware atomic read/modify/write instructions without lock overhead.

## 3. Read-Copy-Update (RCU)
RCU is a state-of-the-art synchronization mechanism optimized for read-heavy data structures:
- **Readers**: Zero lock contention! Readers simply call `rcu_read_lock()` and `rcu_read_unlock()`. No atomic bus locks or cache bouncing!
- **Writers**: Allocate a new copy of the data, mutate the copy, update the pointer atomically with `rcu_assign_pointer()`, and defer freeing the old copy until all preexisting readers have finished (grace period via `synchronize_rcu()` or `call_rcu()`).
