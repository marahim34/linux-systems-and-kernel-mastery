19. Capstone Project & Full Solutions
The capstone — a complete, concurrent, poll-able driver
Combine the volume into one project: a character driver that buffers data written by producers and delivered
to blocked readers, with a background kernel thread, proper locking, blocking I/O, poll support, and a sysfs
status attribute. The specification:
Requirement

Concepts exercised

A FIFO buffer of messages

Kernel memory, list_head (Ch.4,5)

Multiple writers, safely

Spinlock or mutex (Ch.7)

Readers block until data

Wait queues, signals (Ch.9)

poll/select support

poll callback (Ch.9)

A kthread aging old messages

Kernel threads, timers (Ch.12)

/sys attribute showing count

Driver model, sysfs (Ch.8)

No leaks, clean unload

Resource discipline, devm_ (Ch.5)

lockdep &amp; KASAN clean

Correctness tooling (Ch.16)

Build it incrementally: first the char device, then locking, then blocking reads, then poll, then the kthread, then
sysfs. Test each layer before adding the next, with lockdep and KASAN enabled throughout. The finished
driver demonstrates every core competency of kernel development and is a genuine portfolio piece.

Solution sketches to the chapter exercises
Ch.4 — Intrusive list module: embed a list_head in your struct, use LIST_HEAD for the anchor,
list_add_tail to append, list_for_each_entry to iterate (it recovers each object via container_of), and
list_for_each_entry_safe when deleting during iteration so freeing the current node does not corrupt the walk.
Free every node in exit; KASAN confirms no leak.
Ch.5 — Managed allocation: in probe use devm_kzalloc(&pdev-;>dev, ...) and add NO kfree — the core
frees on unbind and on probe-failure paths, eliminating error-path leaks. Verify by unbinding and watching for
no KASAN report.
Ch.7 — RCU read-mostly list: readers wrap access in rcu_read_lock/unlock and use
list_for_each_entry_rcu; the writer adds with list_add_rcu, and to remove uses list_del_rcu then
synchronize_rcu before kfree, so no reader ever touches freed memory. rcu_dereference/rcu_assign_pointer
provide the ordering.
Ch.9 — Blocking read with poll: a wait_event_interruptible on a 'data_available' condition, woken by
wake_up_interruptible when a writer adds data; return -ERESTARTSYS if the wait is signal-interrupted. The
poll callback registers the same wait queue with poll_wait and returns EPOLLIN when data is present.
Together they support both blocking read and select/epoll.
Ch.10 — Threaded IRQ / workqueue: the hard handler returns IRQ_WAKE_THREAD (or schedule_work)
so all sleeping work runs in the threaded half / workqueue with GFP_KERNEL and mutexes permitted; the
hard half only acknowledges the device and checks ownership on shared lines.





Ch.12 — Heartbeat kthread: kthread_run a function that loops while !kthread_should_stop(), doing work
and msleep(1000) between beats; kthread_stop in exit ends it cleanly. Because it is process context,
sleeping and mutexes are fine.
Ch.17 — Hardened ioctl: copy_from_user the request, validate every field (bounds, counts) before use,
allocate with kmalloc_array to defeat multiplication overflow, check capable() for privileged commands, and
zero any buffer copied back to prevent info leaks. Each check maps to a known CVE class.

You now hold the full arsenal: the execution model, the memory model, advanced
concurrency including RCU, the device model, interrupts and DMA, the major driver
classes, and the path upstream. With your C and C++ foundation, the remaining
distance to real kernel contribution is practice on real hardware or QEMU — not
more theory.
— End of Volume 9, Kernel Development: The Complete Guide —