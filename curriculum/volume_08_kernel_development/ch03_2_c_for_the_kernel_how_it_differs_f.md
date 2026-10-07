2. C for the Kernel — How It Differs from Normal C
The library you cannot use
Normal C programs link against the C standard library — printf, malloc, fopen, strcpy. In the kernel, none of
these exist. The kernel provides its OWN versions with different names and rules. Writing kernel C is
learning this parallel vocabulary. The logic of C is identical; the toolkit is different.
User space (libc)

Kernel equivalent

Note

printf()

printk()

Logs to the kernel buffer, not a
screen

malloc() / free()

kmalloc() / kfree()

Allocates kernel memory; can fail,
must check

memcpy()

memcpy()

Exists, but also copy_to/from_user
for user data

fopen() / fread()

(no direct file I/O)

The kernel IS the file layer; different
model

exit()

return codes

A module returns 0 or a negative
errno

assert()

BUG_ON() / WARN_ON()

Kernel-style assertions

Rules that do not exist in user space
Rule

Reason

No standard library

The kernel runs before/below libc; it has its own

No floating point (usually)

Saving FPU state on every syscall would be costly

Small fixed stack (a few KB)

No deep recursion, no large local arrays

Every allocation can fail

No swap to fall back on; always check kmalloc

You may run in interrupt context

Where you cannot sleep — some functions are banned

Concurrency is everywhere

Many CPUs run kernel code at once (Chapter 9)

PRO INSIGHT: The mindset shift: in user space you assume resources are plentiful and failures are exceptional. In
the kernel you assume the opposite — memory is scarce, allocations fail, other CPUs run your code
simultaneously, and a mistake is catastrophic. Defensive, minimal, careful code is not a style choice here; it is
survival. This discipline, once learned, makes you a better programmer everywhere.

Kernel data types





u8, u16, u32, u64 /* fixed-width unsigned integers */
s8, s16, s32, s64 /* fixed-width signed */
size_t /* sizes */
loff_t /* file offsets */
dev_t /* device numbers */