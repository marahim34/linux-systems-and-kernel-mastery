1. Process-context-only data uses a mutex (the waiter sleeps efficiently). Data shared with an interrupt handler MUST
use a spinlock with irqsave — because an interrupt cannot sleep and a mutex could deadlock it. The context of ALL
accessors decides the lock, not just the one you are writing.

Ch.11 — Reading an oops
/* After a NULL dereference, dmesg shows: */
/* BUG: kernel NULL pointer dereference at 0000000000000000 */
/* Call Trace: */
/* my_read+0x2a/0x80 [mymodule] <- YOUR function and offset */
/* vfs_read+0x9b/0x150 */