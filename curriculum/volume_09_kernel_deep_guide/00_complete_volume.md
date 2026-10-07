# Volume 9: Kernel Development Complete Guide

/* Data touched only in process context, may take time: */
mutex_lock(&lock); ... mutex_unlock(&lock);
/* Data ALSO touched by an interrupt handler: */
spin_lock_irqsave(&slock, flags);
...
spin_unlock_irqrestore(&slock, flags);

1. Process-context-only data uses a mutex (the waiter sleeps efficiently). Data shared with an interrupt handler MUST
use a spinlock with irqsave — because an interrupt cannot sleep and a mutex could deadlock it. The context of ALL
accessors decides the lock, not just the one you are writing.

Ch.11 — Reading an oops
/* After a NULL dereference, dmesg shows: */
/* BUG: kernel NULL pointer dereference at 0000000000000000 */
/* Call Trace: */
/* my_read+0x2a/0x80 [mymodule] <- YOUR function and offset */
/* vfs_read+0x9b/0x150 */

1. The Call Trace, read from the top, names the failing function (my_read) in your module with the byte offset (+0x2a).
That points almost exactly at the faulting line. The lower entries (vfs_read) show the kernel path that called you. This
trace is the fastest route to the bug.

Ch.13 — Why reverse-order cleanup
/* init order: buffer -> region -> cdev -> class -> device */
/* exit order: device -> class -> cdev -> region -> buffer */

1. Resources often depend on earlier ones (the device entry depends on the class, which depends on the region).
Tearing down in reverse ensures you never destroy something another still-live resource depends on, and never leak by
forgetting one. This mirror pattern is the standard for all kernel setup/teardown.

You have crossed from operating the kernel to writing it. Few make this journey —
and it begins with one module you build yourself.
— End of Volume 8, Kernel Development —

LINUX MASTERY
VOLUME 9 — KERNEL
DEVELOPMENT: THE COMPLETE




GUIDE
A Serious, In-Depth Treatment for C/C++ Programmers — the Kernel Execution
Model,
Memory & Allocators, Advanced Concurrency (RCU, Memory Barriers), the Device
Model,
Interrupts & DMA, Char/Block/Net Drivers, Filesystems, Debugging & Upstreaming

Assumes fluency in C and C++ · Builds on Volumes 4 and 8 · Prepared for MD
Abdur Rahim · 2026





Table of Contents — Volume 9
1. From C/C++ to the Kernel — the Mental Reset
2. The Kernel Execution Model — Contexts You Run In
3. The Build System — Kbuild, Kconfig & Out-of-Tree
4. Data Structures — Lists, Trees, Hashes the Kernel Way
5. Memory Management In Depth — Allocators & the MM
6. The Kernel Memory Model — Barriers, Ordering & atomics
7. Concurrency Mastery — Spinlocks, Mutexes, RCU, seqlocks
8. The Device Model — kobjects, sysfs, buses & the driver core
9. Character Drivers, Done Properly
10. Interrupts, Softirqs, Tasklets, Workqueues & Threaded IRQ
11. DMA & Hardware Access
12. Time, Timers & Kernel Threads
13. Block Devices & the I/O Stack (Overview)
14. Network Drivers & the sk_buff (Overview)
15. Filesystems & the VFS (Overview)
16. Debugging, Tracing & Performance
17. Security, Hardening & Common Vulnerabilities
18. Upstreaming — Style, Patches & the Community
19. Capstone Project & Full Solutions





1. From C/C++ to the Kernel — the Mental Reset
What your C knowledge transfers, and what betrays you
You know C, so the syntax is free. But several habits from application C and especially C++ are actively
dangerous in the kernel. This chapter is the reset.
Your habit

In the kernel

Because

#include <stdio.h>, libc

Gone entirely

The kernel is freestanding; it has its
own headers

malloc/free

kmalloc/kfree, and more

Multiple allocators with context rules

Unbounded recursion, big locals

Forbidden

The kernel stack is ~8–16 KB, fixed

float/double

Effectively banned

FPU state is not saved across kernel
entry by default

Exceptions, RTTI, STL (C++)

None

The kernel is C; no C++ runtime
exists in it

Assume allocation succeeds

Always check

No OOM safety net; failure is normal

Single-threaded assumptions

Never

Your code runs on all CPUs at once

errno

Return -E values directly

Negative errno is the kernel
convention

PRO INSIGHT: The deepest reset for a C++ programmer: there is no runtime beneath you. No new/delete, no
constructors firing automatically, no exceptions unwinding the stack, no STL container managing memory. The
kernel is C with manual everything, running in an environment where a mistake halts the machine. Your C++
instincts for abstraction must be replaced by explicit, defensive, resource-tracked C. The good news: your
understanding of memory, pointers, and undefined behaviour is exactly what keeps you alive here.

The kernel's idioms that replace language features
You would reach for (C++)

Kernel idiom

Templates / generics

void * plus container_of() and macros

Constructors/destructors

explicit init/exit functions and goto cleanup

RAII

manual paired acquire/release; devm_* managed
resources

std::list, std::map

list_head, rb_root, hlist (intrusive structures)

Exceptions

integer error codes checked on every call

dynamic_cast

container_of() to recover the enclosing struct

The single most important idiom to internalise is container_of() and intrusive data structures. Instead of a list
holding pointers to your objects, your objects EMBED a list node, and container_of() recovers the object from
the node. This is how the kernel gets generic containers in C without templates, and it is everywhere.





struct my_item {
int value;
struct list_head node; /* embedded, intrusive */
};
/* given a list_head *p, recover the my_item: */
struct my_item *it = container_of(p, struct my_item, node);

1. Your object embeds the list node directly, rather than the list pointing at your object.
2. container_of takes a pointer to a MEMBER, the containing type, and the member name, and computes the address of
the enclosing struct by subtracting the member's offset. Type-safe generic containers in pure C. Study this macro until it
is obvious — it underpins the whole kernel.





2. The Kernel Execution Model — Contexts You Run
In
The question that governs every line: what context am I in?
Kernel code runs in one of several contexts, and each forbids certain actions. Calling a sleeping function in
atomic context, or touching user memory from a kernel thread, is a bug that may not show up until
production. You must always know your context.
Context

When

May sleep?

May access user
memory?

Process (syscall)

Serving a syscall for a task

Yes

Yes (copy_to/from_user)

Kernel thread

A kthread you spawned

Yes

No (no user context)

Softirq/tasklet

Deferred interrupt work

No

No

Hardirq (top half)

Hardware interrupt handler

No

No

NMI

Non-maskable interrupt

No, very restricted

No

PRO INSIGHT: The 'can I sleep?' test is the master question of kernel programming. Sleeping means the scheduler
may run another task while you wait — allocating with GFP_KERNEL, taking a mutex, or calling copy_to_user can
all sleep. In ANY interrupt or atomic context, sleeping is forbidden and will trigger 'scheduling while atomic' — a
serious bug. Before every function call, know: what context am I in, and can this call sleep? This one discipline
prevents a large fraction of all kernel bugs.

Checking and enforcing context
might_sleep(); /* debug: warns if called in atomic context */
in_interrupt(); /* true if in interrupt context */
if (in_atomic()) { ... } /* detect atomic context */
preempt_disable(); preempt_enable(); /* control preemption */

1. might_sleep() is a debugging annotation: put it in functions that may sleep, and the kernel warns if they are ever
called from atomic context. A cheap early-warning system.
2. in_interrupt() tells you at runtime whether you are in interrupt context — use to choose GFP_ATOMIC vs
GFP_KERNEL if a function serves both.
3. in_atomic() detects any atomic context (interrupt or preemption-disabled).
4. preempt_disable/enable bracket code that must not be preempted — creating a small atomic section even in process
context.

Per-CPU data — avoiding locks by not sharing
A powerful kernel technique: instead of one shared variable guarded by a lock, keep a SEPARATE copy per
CPU. Each CPU touches only its own copy, so no locking is needed for the common case. This is how the
kernel scales counters and caches to hundreds of cores without contention.





DEFINE_PER_CPU(int, my_counter);
this_cpu_inc(my_counter); /* increment THIS cpu's copy, lock-free */
int total = 0;
int cpu;
for_each_possible_cpu(cpu)
total += per_cpu(my_counter, cpu); /* sum across cpus when needed */

1. Declare a per-CPU integer — physically one instance per processor.
2. Increment the current CPU's private copy with no lock and no cache-line bouncing — extremely fast.
3. To read the global value, sum every CPU's copy. You pay the cost only on the rare read, not the frequent write. This
'shard per CPU' pattern is a cornerstone of kernel scalability.





3. The Build System — Kbuild, Kconfig & Out-of-Tree
How the kernel builds
The kernel uses Kbuild, a recursive Make-based system driven by tiny Makefiles that just list objects.
Configuration comes from Kconfig files that generate the .config controlling what is built. Understanding both
lets you add code the kernel's own way, not bolted on.
# A Kbuild Makefile fragment (in-tree)
obj-$(CONFIG_MY_DRIVER) += mydriver.o
mydriver-objs := main.o hw.o sysfs.o

1. obj-$(CONFIG_MY_DRIVER) means 'build this if the config option is set': y = built-in, m = module, n = skip. This is
how every driver is conditionally compiled.
2. A multi-file module: mydriver.ko is linked from main.o, hw.o and sysfs.o. The -objs (or -y) variable lists the parts.
# A Kconfig entry
config MY_DRIVER
tristate "My example device driver"
depends on PCI
default m
help
Support for the example device. Say M to build as a module.

1. config NAME defines an option usable in Makefiles as CONFIG_NAME.
2. tristate allows y/m/n (bool allows only y/n). This is what makes it buildable as a module.
3. depends on expresses requirements — the option is hidden unless PCI is enabled.
4. default m suggests building as a module.
5. The help text shown in menuconfig. This is how your driver becomes a first-class, configurable part of the kernel.

Out-of-tree modules — your development mode
# Out-of-tree Makefile
obj-m := mydriver.o
KDIR := /lib/modules/$(shell uname -r)/build
all:
$(MAKE) -C $(KDIR) M=$(PWD) modules
clean:
$(MAKE) -C $(KDIR) M=$(PWD) clean
install:
$(MAKE) -C $(KDIR) M=$(PWD) modules_install

1. obj-m builds a module outside the kernel tree — your normal development loop.
2. KDIR points at your running kernel's build directory.
3. The build enters the KERNEL's build system (-C) and points it back at your code (M=$(PWD)) — Kbuild does the
actual work.
4. modules_install copies the .ko into /lib/modules so modprobe can find it. Out-of-tree is how you develop; in-tree
(Chapters above) is how you upstream.





PRO INSIGHT: The build-system distinction that matters: OUT-OF-TREE (obj-m in your own directory) is for
development and third-party drivers — fast iteration, no kernel source needed beyond headers. IN-TREE
(obj-$(CONFIG_x) inside the kernel source with a Kconfig entry) is for code you intend to UPSTREAM. Start
out-of-tree to build and test, then convert to in-tree with proper Kconfig when you are ready to contribute. Knowing
both, and when to use each, marks the transition from hobbyist to contributor.





4. Data Structures — Lists, Trees, Hashes the Kernel
Way
Intrusive by design
The kernel provides highly optimised, INTRUSIVE data structures: your object embeds the linkage, and
macros operate on it. No allocation for nodes, no templates, cache-friendly. Master these three and you can
read most kernel code.
#include <linux/list.h>
struct task { int id; struct list_head list; };
LIST_HEAD(my_tasks); /* the list head */
struct task *t = kmalloc(sizeof(*t), GFP_KERNEL);
list_add_tail(&t->list, &my_tasks); /* append */
struct task *pos;
list_for_each_entry(pos, &my_tasks, list)
pr_info("task %d\n", pos->id);
list_del(&t->list); kfree(t);

1. The doubly-linked list is the kernel's workhorse container.
2. Your struct embeds a list_head.
3. LIST_HEAD declares and initialises the anchor.
4. Allocate your object...
5. ...and link it in with list_add_tail (or list_add for the front).
6. list_for_each_entry iterates, giving you each CONTAINING object directly (it uses container_of internally). No casts,
no node objects.
7. Unlink then free — order matters; unlink while the object is still valid.

Red-black trees and hash tables
Structure

Header

Use when

list_head

linux/list.h

Ordered traversal, queues, LRU

hlist

linux/list.h

Hash buckets (single-pointer head
saves memory)

rb_root (red-black tree)

linux/rbtree.h

Sorted data with O(log n) lookup

DECLARE_HASHTABLE

linux/hashtable.h

Fast keyed lookup

xarray / idr

linux/xarray.h

Integer-to-pointer mapping (IDs to
objects)





PRO INSIGHT: These intrusive structures are why the kernel is fast and why it looks alien to application
programmers. Because the linkage lives INSIDE your object, adding to a list needs no allocation and touches no
separate node — the object is the node. One object can even sit in several lists at once by embedding several
list_heads. For a C++ programmer used to std::list allocating wrapper nodes, this is a genuinely better design for
systems code. Learn container_of and list_for_each_entry cold; they appear on nearly every kernel page.
PRACTICE EXERCISES
1. Build a module holding a linked list of structs; add several, iterate printing them, and free all on exit — with no
leaks.
2. Rewrite the same collection using an rb_tree keyed by an integer id; implement insert and lookup.
3. Explain, from the macro definition, exactly how container_of computes the enclosing struct's address.
4. Embed TWO list_heads in one struct and place it in two different lists simultaneously.





5. Memory Management In Depth — Allocators & the
MM
The allocator zoo
The kernel has several allocators because different needs have different constraints: size, contiguity, speed,
and context. Choosing correctly is a real skill.
Allocator

Returns

Use for

kmalloc

Physically contiguous, small

General small allocations, DMA-able

kzalloc

Same, zeroed

When you need clean memory

vmalloc

Virtually contiguous, large

Big buffers where physical contiguity
is not needed

kmem_cache (slab)

Fixed-size objects from a pool

Many same-size objects (frequent
alloc/free)

alloc_pages

Raw pages

Page-granular allocations, DMA

devm_kmalloc

Managed, auto-freed on unbind

Driver allocations tied to a device
lifetime

Slab caches — for objects you allocate constantly
static struct kmem_cache *my_cache;
/* init: */
my_cache = kmem_cache_create("my_obj", sizeof(struct my_obj),
0, SLAB_HWCACHE_ALIGN, NULL);
/* hot path: */
struct my_obj *o = kmem_cache_alloc(my_cache, GFP_KERNEL);
kmem_cache_free(my_cache, o);
/* exit: */
kmem_cache_destroy(my_cache);

1. A slab cache is a pool of fixed-size objects, far faster than kmalloc for high-frequency same-size allocations.
2. Create it once, naming the object and its size; SLAB_HWCACHE_ALIGN aligns objects to cache lines for
performance.
3. Allocate and free from the pool in your hot path — the slab keeps freed objects ready for instant reuse, avoiding
repeated setup.
4. Destroy the cache on unload (all objects must be freed first). This is how the kernel manages millions of task_structs,
inodes, and dentries efficiently.

Managed allocations — devm_, the closest thing to RAII
For a C++ programmer missing RAII, the devm_ family is the kernel's answer. Memory (and other resources)
allocated with devm_kmalloc, devm_ioremap, etc. are automatically freed when the device unbinds. This





eliminates most cleanup code and a whole class of leak bugs in drivers.
static int my_probe(struct platform_device *pdev)
{
struct my_priv *priv;
priv = devm_kzalloc(&pdev->dev, sizeof(*priv), GFP_KERNEL);
if (!priv) return -ENOMEM;
/* no kfree needed anywhere — freed automatically on unbind */
return 0;
}

1. In a driver's probe function...
2. devm_kzalloc ties the allocation to the device (&pdev-;>dev).
3. Still check for failure.
4. When the device unbinds or probe fails, the core frees this automatically. No matching free, no leak on error paths.
This is the modern, preferred style for driver resource management — embrace it.

PRO INSIGHT: The allocation-context matrix you must hold in your head: GFP_KERNEL may sleep (process
context only); GFP_ATOMIC never sleeps but is more likely to fail (interrupt context); large allocations prefer
vmalloc; high-frequency same-size objects use a slab cache; and driver resources should use devm_ so cleanup is
automatic. Getting the allocator AND the flags right for your context and pattern is what separates robust kernel
code from code that works on your desk and fails under production memory pressure.





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
2. Atomic increment/decrement — safe against concurrent CPUs.
3. Atomic read.
4. dec_and_test atomically decrements AND tells you if it hit zero — the classic reference-counting primitive.
5. cmpxchg: set to new ONLY if it currently equals old, atomically — the building block of all lock-free algorithms.

Memory barriers — enforcing order
Barrier

Guarantees

Use

smp_mb()

Full barrier: all prior loads/stores
before later

General ordering

smp_wmb()

Write barrier: prior stores before later
stores

Publishing data then a flag

smp_rmb()

Read barrier: prior loads before later
loads

Reading a flag then the data

READ_ONCE / WRITE_ONCE

Prevents compiler tearing/reordering
one access

Any shared-variable access without a
lock

smp_load_acquire / store_release

Acquire/release ordering (like
C++11)

The modern, preferred pairing





/* Producer publishes data, THEN sets ready flag: */
obj->data = 42;
smp_wmb(); /* ensure data write lands first */
WRITE_ONCE(obj->ready, 1);
/* Consumer sees flag, THEN reads data: */
if (READ_ONCE(obj->ready)) {
smp_rmb(); /* ensure we read data AFTER seeing flag */
use(obj->data);
}

1. The producer writes the payload...
2. ...then a WRITE barrier guarantees that payload is visible BEFORE...
3. ...the ready flag is set. Without the barrier, another CPU could see ready=1 but stale data.
4. The consumer checks the flag...
5. ...a READ barrier ensures it reads the payload AFTER observing the flag...
6. ...so the data it uses is the published value. This paired barrier pattern is the essence of lock-free publication.

PRO INSIGHT: If you have done C++11 std::atomic with memory_order_acquire/release, this will feel familiar —
the kernel's smp_load_acquire/smp_store_release are the same concept, and the preferred modern style. The
crucial warning: lock-free code without correct barriers is WRONG even when it passes every test on your machine,
because reordering is timing- and architecture-dependent (x86 is forgiving; ARM is not). Never write lock-free kernel
code by intuition. Use established patterns, use acquire/release, and when in doubt, use a lock — correctness first.





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
3. Use the data; it is guaranteed valid until rcu_read_unlock.
4. The writer copies, modifies the copy (Read-COPY-Update)...
5. rcu_assign_pointer atomically publishes the new version — new readers see it, old readers still use the old.
6. synchronize_rcu blocks until every reader that MIGHT hold the old pointer has finished...
7. ...only THEN is it safe to free the old version. No reader ever sees freed memory, with no reader-side locking.

PRO INSIGHT: RCU is the single most distinctive and powerful concurrency mechanism in Linux, and
understanding it marks a serious kernel developer. The mental model: readers are free and never block; the cost is
moved entirely to writers, who must wait out a grace period before reclaiming old data. It fits read-mostly data
perfectly — which describes much of the kernel. It is subtle: readers must not sleep (in classic RCU), and you must
use rcu_dereference/rcu_assign_pointer for the ordering. But mastered, it is how Linux achieves its legendary
multi-core scalability.

Deadlock avoidance, enforced
Volume 5's lock-ordering rule is enforced here by lockdep, the runtime dependency validator. Enable
CONFIG_PROVE_LOCKING in your development kernel and it tracks every lock acquisition order,
screaming the moment two code paths could form a cycle — catching deadlocks that might otherwise appear
only once a year in production. No serious kernel work is done without lockdep on in testing.
PRACTICE EXERCISES
1. Protect a shared counter three ways (atomic_t, spinlock, mutex) and reason about which fits which context.
2. Implement a read-mostly list with RCU: readers iterate lock-free, a writer replaces an entry safely.
3. Write two functions that acquire locks A,B in opposite orders; enable lockdep and capture its report.
4. Explain, using acquire/release, why rcu_dereference and rcu_assign_pointer are needed rather than plain
pointer access.





8. The Device Model — kobjects, sysfs, buses & the
driver core
The unifying abstraction
Beneath every driver is the driver model: a hierarchy of kobjects that produces /sys, models buses, devices
and drivers, and handles the matching of drivers to hardware. Understanding it explains how a driver gets
bound to a device, where /sys entries come from, and how hotplug works.
Object

Represents

Appears in

kobject

The base 'thing' with a refcount and
sysfs node

/sys everywhere

bus_type

A kind of bus (PCI, USB, platform,
I2C)

/sys/bus/

device

A physical or virtual device

/sys/devices/

device_driver

A driver that can handle devices

/sys/bus/*/drivers/

class

A functional grouping (net, block, tty)

/sys/class/

How binding works — probe and remove
A bus MATCHES devices to drivers (by ID tables). When a match occurs, the driver's probe() is called to
initialise that device; on removal or unbind, remove() tears it down. This is the driver lifecycle for every
modern bus.
static const struct of_device_id my_ids[] = {
{ .compatible = "vendor,mydevice" },
{ }
};
MODULE_DEVICE_TABLE(of, my_ids);
static struct platform_driver my_driver = {
.probe = my_probe,
.remove = my_remove,
.driver = {
.name = "mydevice",
.of_match_table = my_ids,
},
};
module_platform_driver(my_driver);

1. An ID table declares which hardware this driver supports — here by device-tree 'compatible' string.
2. MODULE_DEVICE_TABLE exposes the IDs so the kernel can autoload your module when matching hardware
appears (hotplug).
3. The driver structure binds probe and remove callbacks...
4. ...names the driver and links its match table.
5. module_platform_driver is a macro that generates the init/exit boilerplate to register this driver — one line replaces a
dozen. The core now calls my_probe whenever a matching device appears.





Exposing attributes via sysfs
static ssize_t speed_show(struct device *d,
struct device_attribute *a, char *buf)
{
return sysfs_emit(buf, "%d\n", get_speed());
}
static DEVICE_ATTR_RO(speed);
/* in probe: */
device_create_file(dev, &dev_attr_speed);

1. A show function produces the text a user reads from the sysfs file.
2. sysfs_emit safely formats into the sysfs buffer.
3. DEVICE_ATTR_RO declares a read-only attribute named 'speed' (there are RW and WO variants).
4. device_create_file makes /sys/.../speed appear. Now userspace can cat it — this is how drivers expose status and
tunables, the /sys philosophy from Volume 4 made by your hand.

PRO INSIGHT: The driver model is the scaffold that makes 'plug in hardware, the right driver loads and initialises it'
work. Your job as a driver author is mostly to fill in probe (set up this device) and remove (tear it down), declare
which hardware you match, and expose attributes through sysfs. The core handles matching, refcounting, hotplug,
and power management. Learning to work WITH the model — rather than registering char devices by hand as in
Volume 8 — is the leap to writing real, upstreamable drivers.





9. Character Drivers, Done Properly
Beyond the basics — the professional character driver
Volume 8 built a minimal char device. A production one adds: proper concurrency (multiple openers),
blocking I/O (readers wait for data), poll/select support, and clean integration with the driver model. Here are
the professional additions.

Blocking I/O — making read wait for data
static DECLARE_WAIT_QUEUE_HEAD(read_queue);
static ssize_t my_read(struct file *f, char __user *buf,
size_t len, loff_t *off)
{
if (wait_event_interruptible(read_queue, data_available))
return -ERESTARTSYS; /* interrupted by a signal */
/* ... now data_available is true; copy it out ... */
}
/* when data arrives (e.g. in an interrupt): */
data_available = true;
wake_up_interruptible(&read_queue);

1. A wait queue lets a reader SLEEP until data is ready, instead of spinning or returning empty.
2. wait_event_interruptible sleeps the calling process until the condition becomes true — efficiently yielding the CPU.
3. If a signal interrupts the wait, return -ERESTARTSYS so the syscall is retried or reported correctly. Handling signals
is mandatory for correctness.
4. When data arrives, set the condition and wake_up the sleepers. The woken reader re-checks the condition and
proceeds. This is the correct blocking-I/O pattern.

poll/select support
static __poll_t my_poll(struct file *f, poll_table *wait)
{
__poll_t mask = 0;
poll_wait(f, &read_queue, wait);
if (data_available) mask |= EPOLLIN | EPOLLRDNORM;
return mask;
}

1. poll lets userspace use select/poll/epoll on your device — essential for event loops.
2. poll_wait registers your wait queue with the poll infrastructure (does not sleep here).
3. Report readable when data is present; the mask tells userspace which events are ready.
4. This makes your device a first-class citizen in any event-driven program.

PRO INSIGHT: The difference between a toy driver and a real one is these behaviours: it must handle multiple
concurrent openers safely (locking around shared state), let readers block efficiently rather than busy-wait (wait
queues), respect signals (ERESTARTSYS), and support poll for event loops. Each is a well-established pattern. A
char driver with correct blocking I/O, signal handling, poll support, and driver-model integration is genuinely
production-grade — and demonstrates you understand the kernel's I/O contract, not just its syntax.





10. Interrupts, Softirqs, Tasklets, Workqueues &
Threaded IRQ
The full deferral toolkit
Volume 8 introduced the top-half/bottom-half split. Here is the complete set of deferral mechanisms and
precisely when each applies.
Mechanism

Runs in

Sleeps?

Use when

Hardirq handler

Interrupt context

No

The urgent minimum: ack,
grab data

softirq

Interrupt context

No

High-frequency core work
(net, block) —
kernel-defined only

tasklet

Interrupt context (on
softirq)

No

Simple deferred work,
serialised per tasklet

workqueue

Process context (kthread)

Yes

Work that may sleep: I/O,
allocation, locks

threaded IRQ

Dedicated kernel thread

Yes

Modern default: handler
that can sleep

Threaded IRQ — the modern approach
static irqreturn_t hard_handler(int irq, void *dev)
{
if (!is_ours(dev)) return IRQ_NONE;
return IRQ_WAKE_THREAD; /* defer to the thread */
}
static irqreturn_t thread_handler(int irq, void *dev)
{
/* runs in a kthread — MAY sleep, take mutexes, do I/O */
process_data(dev);
return IRQ_HANDLED;
}
request_threaded_irq(irq, hard_handler, thread_handler,
IRQF_SHARED, "mydev", dev);

1. The hard (top-half) handler runs in true interrupt context...
2. ...quickly checks the interrupt is ours (return IRQ_NONE if not — vital on shared lines)...
3. ...and returns IRQ_WAKE_THREAD to hand off to the threaded half.
4. The threaded handler runs in a dedicated kernel thread, where it CAN sleep — take mutexes, allocate with
GFP_KERNEL, do slow work.
5. request_threaded_irq registers both halves. This split gives you a fast atomic acknowledgement AND a
sleep-capable processing context — the cleanest modern pattern, preferred over manual tasklet/workqueue juggling.





Workqueues for deferred sleeping work
static void my_work_fn(struct work_struct *w)
{
/* process context: may sleep */
}
static DECLARE_WORK(my_work, my_work_fn);
schedule_work(&my_work); /* queue it to run later */

1. A work function runs in process context and may do anything that sleeps.
2. DECLARE_WORK binds a work item to the function.
3. schedule_work queues it onto the system workqueue; a kernel thread runs it soon. Use this from a hardirq to defer
sleeping work safely.

PRO INSIGHT: The decision tree for deferred work: if it MUST be fast and cannot sleep, keep it in the hardirq or a
tasklet. If it may sleep (allocation, I/O, mutex), it MUST go to a workqueue or a threaded IRQ. The modern,
recommended default for device interrupts is request_threaded_irq — it gives you a tiny atomic top half and a
sleep-capable bottom half with minimal boilerplate. Reaching for the right mechanism, matched to whether the work
can sleep, is core interrupt-handling competence.





11. DMA & Hardware Access
Reaching the hardware
Drivers talk to devices through memory-mapped registers and move bulk data with DMA. Both have strict
rules the kernel enforces, because raw hardware access from the wrong place corrupts systems.
void __iomem *regs = devm_ioremap_resource(&pdev->dev, res);
u32 status = readl(regs + STATUS_REG);
writel(START_BIT, regs + CTRL_REG);

1. ioremap maps a device's physical register block into kernel virtual address space; the devm_ version auto-unmaps on
unbind. The __iomem annotation marks it as device memory, not normal RAM.
2. readl/readb/readw read device registers with the correct barriers and byte ordering — never dereference __iomem
pointers directly.
3. writel writes a register. These accessors ensure ordering and portability across architectures.

DMA — letting the device read/write memory directly
dma_addr_t dma_handle;
void *cpu_buf = dma_alloc_coherent(&pdev->dev, SIZE,
&dma_handle, GFP_KERNEL);
/* give dma_handle to the device; use cpu_buf from the CPU */
/* ... device transfers data ... */
dma_free_coherent(&pdev->dev, SIZE, cpu_buf, dma_handle);

1. dma_addr_t is the address the DEVICE uses (a bus address), distinct from the CPU pointer.
2. dma_alloc_coherent allocates a buffer both the CPU and device can access consistently, returning BOTH a CPU
pointer (cpu_buf) and a device address (dma_handle).
3. You hand dma_handle to the device's registers; the device reads/writes cpu_buf's memory directly, bypassing the
CPU (Volume 4's DMA).
4. Free it when done. Coherent DMA avoids manual cache management; streaming DMA (dma_map_single) is faster
but needs explicit sync.

PRO INSIGHT: DMA is where Volume 4's theory becomes physical: the device writes directly into RAM you
allocated, and interrupts you when done — the CPU never copies the bulk data. The subtleties that bite: the device
sees a DIFFERENT address than the CPU (bus vs virtual), and CPU caches can hold stale copies of DMA memory
(hence coherent allocations or explicit dma_sync calls). Get the addressing or cache handling wrong and you get
silent data corruption, the hardest kind of bug. Respect the DMA API precisely.





12. Time, Timers & Kernel Threads
unsigned long start = jiffies;
if (time_after(jiffies, start + msecs_to_jiffies(500))) { }
ktime_t t = ktime_get();
udelay(10); /* busy-wait microseconds (atomic context) */
msleep(20); /* sleep milliseconds (process context) */

1. jiffies is the kernel's tick counter — coarse time. Save a start value...
2. ...and use time_after (not raw comparison, which breaks on wraparound) to check elapsed time.
3. ktime_get gives high-resolution time for precise measurement.
4. udelay busy-waits — the only option in atomic context, but wastes CPU; keep it tiny.
5. msleep actually sleeps — use in process context to yield the CPU while waiting.
static struct task_struct *thread;
thread = kthread_run(thread_fn, data, "my_kthread");
/* the thread function: */
static int thread_fn(void *data)
{
while (!kthread_should_stop()) {
do_work();
msleep(100);
}
return 0;
}
/* to stop: kthread_stop(thread); */

1. kthread_run spawns a kernel thread running thread_fn, named for ps/top visibility.
2. The thread loops until asked to stop...
3. ...does its work and sleeps between iterations (it is in process context, so sleeping is fine).
4. kthread_should_stop returns true after someone calls kthread_stop, giving clean shutdown. Kernel threads are how
you run ongoing background work inside the kernel.

PRO INSIGHT: Two time traps to remember: never compare jiffies with plain < or > (use time_after/time_before,
which handle the counter wrapping around to zero), and never use udelay for long waits (it burns a CPU core
spinning). Match the wait to the context: udelay/mdelay for tiny waits in atomic context, msleep/usleep_range for
real waits in process context. Kernel threads (kthread) give you a sleep-capable process context for ongoing work
— the right home for anything that must run continuously in the background.
PRACTICE EXERCISES
1. Write a driver that spawns a kthread printing a heartbeat every second, and stops it cleanly on unload.
2. Use a wait queue so a char device read blocks until the kthread signals data, then returns it.
3. Add poll support so select() works on your device.
4. Convert a busy udelay loop to a proper msleep and explain why it matters for the scheduler.





13. Block Devices & the I/O Stack (Overview)
Block drivers serve storage — disks, SSDs — where data moves in blocks and performance depends on
scheduling and merging requests. The modern interface is blk-mq (multi-queue), built for many-core,
high-IOPS devices.
Layer

Role

Filesystem / page cache

Issues reads/writes as block requests

blk-mq

Per-CPU submission queues; merges and schedules
requests

I/O scheduler

Orders requests (mq-deadline, BFQ, none for NVMe)

Block driver

Your code: takes requests, drives the hardware,
completes them

A block driver registers a request-handling function that receives bio/request structures describing what to
read or write where, programs the hardware (usually via DMA), and signals completion. The complexity
versus char drivers is the performance machinery: queues, merging, and completion handling across many
cores. For most learners, understanding the STACK and where a driver plugs in matters more than writing
one early.
PRO INSIGHT: Key insight for block work: the whole stack exists to turn random, small filesystem operations into
efficient, ordered, merged, parallel hardware transfers. Your driver sits at the bottom, and its job is throughput and
correctness under massive concurrency. NVMe drivers use 'none' scheduling because the device itself parallelises;
spinning disks benefit from ordering. Knowing WHERE your driver sits in this stack, and what the layers above have
already done to the requests, is the foundation of block-device work.





14. Network Drivers & the sk_buff (Overview)
Network drivers move packets between the wire and the kernel's networking stack. The central data structure
is the sk_buff (socket buffer), which carries a packet and its metadata through every layer.
Concept

Role

sk_buff (skb)

Holds one packet plus headroom, headers, metadata

net_device

Represents a network interface (eth0)

NAPI

Interrupt+polling hybrid for high packet rates

ndo_start_xmit

Your TX function: send a packet to the hardware

netif_rx / napi

Your RX path: hand received packets up the stack

A network driver registers a net_device with operations for transmit and receive. On receive, under high load
it uses NAPI — disabling interrupts and POLLING for packets in batches — to avoid interrupt storms
(thousands of interrupts per second would collapse the system). The sk_buff is passed up the stack, gaining
and shedding headers at each layer.
PRO INSIGHT: The sk_buff is the packet's vehicle through the entire network stack, and NAPI is the answer to a
real scaling crisis: at gigabit speeds, one interrupt per packet means hundreds of thousands of interrupts per
second, drowning the CPU. NAPI switches to polling under load — the driver disables RX interrupts and pulls
packets in batches, restoring interrupts only when traffic subsides. This interrupt-mitigation pattern is essential
knowledge, and mirrors the general kernel theme: batch expensive operations, poll when busy, interrupt when idle.





15. Filesystems & the VFS (Overview)
A filesystem plugs into the Virtual File System (Volume 4) by implementing a set of operations the VFS
calls. You provide the behaviour behind open, read, lookup, and so on for your storage format.
VFS object

You implement

Represents

super_block

fill_super, statfs

A mounted filesystem instance

inode

inode_operations (lookup, create)

A file or directory's metadata

dentry

d_ops (rare)

A name-to-inode cache entry

file

file_operations (read, write, mmap)

An open file

address_space

readpage, writepage

A file's page cache mapping

Writing a full on-disk filesystem is a large undertaking, but simple in-memory or virtual filesystems (like a
custom /proc-style interface) are approachable and teach the VFS contract. Many drivers expose information
through a small virtual filesystem rather than a char device.
PRO INSIGHT: The VFS is a set of interfaces you implement, not inherit — pure C polymorphism through operation
tables (super_operations, inode_operations, file_operations). This is the same function-pointer-table pattern as char
drivers, scaled up: fill in the operations for your filesystem and the VFS drives them. Understanding that ALL of
Linux I/O — files, sockets, devices, procfs — flows through these operation tables is the unifying insight of kernel
I/O, and the reason 'everything is a file' holds all the way down.





16. Debugging, Tracing & Performance
The professional toolkit
Tool

Purpose

printk / dynamic_debug

Logging; enable per-site at runtime

ftrace

Function and event tracing inside the kernel

kprobes

Dynamically instrument almost any kernel function

eBPF / bpftrace

Safe, programmable tracing and profiling

perf

CPU profiling, hardware counters, hotspots

KASAN / KMSAN

Detect memory corruption and uninitialised use

lockdep

Prove lock ordering, catch deadlocks

KGDB / QEMU+gdb

Source-level breakpoint debugging

echo 1 > /sys/kernel/debug/tracing/events/enable # trace everything (noisy)
trace-cmd record -p function_graph -g my_function
perf top
bpftrace -e 'kprobe:my_driver_read { printf("read by %s\n", comm); }'

1. ftrace is controlled through /sys/kernel/debug/tracing — enabling events records kernel activity to a ring buffer.
2. trace-cmd with function_graph shows the call graph beneath a function — see exactly what your code invokes and
how long each takes.
3. perf top shows which kernel functions burn CPU right now, system-wide — find hotspots.
4. bpftrace attaches a tiny safe program to your function, printing which process (comm) calls it — dynamic,
production-safe instrumentation without recompiling.

PRO INSIGHT: The modern kernel-debugging progression: printk for quick checks; ftrace/trace-cmd to see control
flow and timing without recompiling; KASAN and lockdep always ON in your development kernel to catch memory
and locking bugs automatically; perf and bpftrace for performance and production tracing; and QEMU+gdb for real
breakpoints when you must step through. A C/C++ developer used to gdb will feel at home with QEMU+gdb, but the
tracing tools (ftrace, eBPF) are the ones that make you effective — they observe a LIVE system without stopping it,
which is where kernel bugs actually live.





17. Security, Hardening & Common Vulnerabilities
The bug classes that become CVEs
Vulnerability

Cause

Defence

Missing user-copy check

Trusting a user pointer/length

copy_to/from_user, validate lengths

Integer overflow

size arithmetic wraps

check_add_overflow, kmalloc_array

Use-after-free

Freeing while still referenced

Refcounts (kref), RCU, careful
ownership

Race condition (TOCTOU)

Check then use without locking

Lock across the whole operation

Info leak

Copying uninitialised kernel memory
to user

Zero buffers (kzalloc), copy exact
sizes

Missing capability check

Not verifying privilege

capable(CAP_SYS_ADMIN) where
needed

if (copy_from_user(&req, arg, sizeof(req))) return -EFAULT;
if (req.count > MAX_ALLOWED) return -EINVAL; /* validate! */
buf = kmalloc_array(req.count, sizeof(*buf), GFP_KERNEL);
if (!buf) return -ENOMEM;
if (!capable(CAP_SYS_ADMIN)) return -EPERM; /* privilege check */

1. Copy user input safely — never trust the pointer.
2. VALIDATE every field from userspace before using it — an unchecked count is an exploit waiting to happen.
3. kmalloc_array checks for multiplication overflow that plain kmalloc(count * size) would miss — a classic
integer-overflow defence.
4. Check allocation.
5. Verify the caller has the required privilege before a sensitive operation — omitting this is a real, common CVE pattern.

PRO INSIGHT: Kernel code is the ultimate trust boundary: it runs with full privilege, and its inputs come from
untrusted userspace and hardware. Every value crossing into the kernel is hostile until validated. The mindset —
validate all input, check every arithmetic operation for overflow, track ownership to prevent use-after-free, hold locks
across whole check-and-use sequences, zero memory before it can leak, and verify privileges — is not paranoia; it
is the difference between a driver and a CVE. For your eQuorum work serving banks, this security-first kernel
mindset transfers directly to writing trustworthy systems.





18. Upstreaming — Style, Patches & the Community
The path from your code to the mainline kernel
scripts/checkpatch.pl --strict 0001-my-patch.patch
git format-patch -1 --signoff
./scripts/get_maintainer.pl 0001-my-patch.patch
git send-email --to=maintainer@... --cc=linux-kernel@vger.kernel.org 0001-*.patch

1. checkpatch --strict enforces kernel coding style; fix EVERY warning before sending, or reviewers stop reading.
2. format-patch produces a mailable patch; --signoff adds your Signed-off-by line, the legal Developer Certificate of
Origin attestation (required).
3. get_maintainer identifies who to email — patches go to the subsystem maintainer and relevant lists, not a web form.
4. send-email delivers it as plain-text email (never HTML). Maintainers review on the list; expect revisions across
several versions (v2, v3...).

What reviewers expect
Expectation

Meaning

One logical change per patch

Split large work into a reviewable series

Clear commit message

WHY the change, not just what; reference the problem

Signed-off-by

The DCO attestation of your right to submit

checkpatch-clean

No style violations

Responds to feedback

Revise and resend; engage respectfully

No regressions

'We do not break userspace' — tested

PRO INSIGHT: Upstreaming is a craft and a culture, not just a technical step. The kernel community values small,
well-explained, correct patches and rewards persistence through review. Your first patch will likely get critical
feedback — that is normal and not personal; revise and resend. Start with drivers/staging, Documentation fixes, or
a small real bug. Getting a patch into the mainline kernel is a permanent, verifiable credential that few engineers
hold, and for someone building a company like Aisora, it is a powerful signal of deep systems competence. The
path is open to anyone who does the work correctly.





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