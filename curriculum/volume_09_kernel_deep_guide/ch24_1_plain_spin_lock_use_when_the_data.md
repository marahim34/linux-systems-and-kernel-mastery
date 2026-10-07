1. Plain spin_lock: use when the data is NEVER touched from softirq or hardirq context.
2. spin_lock_bh: use when a SOFTIRQ/tasklet also touches this data — it disables bottom halves to prevent
self-deadlock.
3. spin_lock_irqsave: use when a HARDIRQ handler also touches this data — disables interrupts on this CPU and
saves prior state. Getting this wrong causes deadlock when an interrupt fires while you hold the lock.

RCU — the kernel's crown jewel
Read-Copy-Update lets readers access shared data with ZERO locking overhead — no atomic operations,
no cache-line bouncing — while writers make changes safely. It is how the kernel scales read-mostly
structures (the dentry cache, network routes) to hundreds of cores. The idea: readers work on the current
version lock-free; writers create a NEW version, publish it atomically, and wait for all pre-existing readers to
finish (a 'grace period') before freeing the old version.





/* Reader — no locks, just mark the critical section: */
rcu_read_lock();
struct obj *p = rcu_dereference(shared_ptr);
if (p) use(p->field);
rcu_read_unlock();
/* Writer — publish new, retire old after grace period: */
struct obj *new = kmalloc(...);
*new = *old; new->field = x;
rcu_assign_pointer(shared_ptr, new);
synchronize_rcu(); /* wait for all readers to finish */
kfree(old);

1. rcu_read_lock marks a reader critical section — extremely cheap, no actual lock.
2. rcu_dereference safely loads the shared pointer with the needed ordering barrier.