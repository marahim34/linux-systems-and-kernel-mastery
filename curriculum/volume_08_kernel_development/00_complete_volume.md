# Volume 8: Kernel Development

— End of Volume 2 —

LINUX MASTERY
VOLUME 8 — KERNEL
DEVELOPMENT
Writing Code Inside the Kernel — From Your First Loadable Module to Real Device
Drivers: Kernel C, Modules, Character Devices, Memory, Concurrency, Interrupts,
Debugging & Contributing — with Compilable Examples and Exercises

The specialist path: from operating Linux to BUILDING it · Requires C · Prepared for
MD Abdur Rahim · 2026





Table of Contents — Volume 8
1. What Kernel Development Is — and What You Need First
2. C for the Kernel — How It Differs from Normal C
3. Your First Kernel Module — Hello, Kernel
4. The Module Lifecycle — Build, Load, Inspect, Unload
5. Kernel Logging & Parameters
6. Character Device Drivers — the Core Skill
7. Talking to User Space — copy_to_user & ioctl
8. Kernel Memory Management
9. Concurrency in the Kernel — Locks Done Right
10. Interrupts & Deferred Work
11. Debugging the Kernel
12. The Kernel Source, Coding Style & Contributing
13. A Complete Driver — Worked End to End
14. Exercises with Full Solutions





1. What Kernel Development Is — and What You
Need First
A different kind of programming
Everything in Volumes 1 through 7 lives in user space — the safe, isolated world where a crash kills only
your program. Kernel development means writing code that runs in kernel space, with full hardware access
and no safety net. A bug here does not throw an exception; it can freeze the whole machine (a kernel panic)
or silently corrupt data. This is why kernel code is written with extreme care, and why understanding Volume
4's internals first matters.
User-space program

Kernel code

Runs in

User space (ring 3)

Kernel space (ring 0)

A bug causes

That program crashes

The whole system may panic

Memory

Virtual, protected, generous

Limited, no swap, no protection

Libraries

Full C library, anything

Only kernel APIs — no printf, no
malloc

Floating point

Free to use

Generally forbidden

Debugging

gdb, print, easy

Specialised, harder

What kernel developers actually build
Area

What you write

Who needs it

Device drivers

Code to control hardware (sensors,
cards, USB)

Hardware vendors, embedded, IoT

Filesystems

New ways to store files

Storage companies

Kernel modules

Add features to a running kernel

Everyone extending the kernel

Subsystem work

Networking, scheduling, memory

Core kernel contributors

Embedded/BSP

Board support for custom hardware

Device manufacturers

What you need before starting
Requirement

Why

Your status

C programming

The kernel is written in C

Learn if needed — this volume
assumes basic C

Volume 4 (internals)

You must understand processes,
memory, VFS

You have it

A Linux machine you can crash

You WILL panic the kernel while
learning

Use a VM, never your main machine





Requirement

Why

Your status

Patience

Feedback loops are slower than user
space

The specialist's mindset

PRO INSIGHT: The one rule that saves you: NEVER develop kernel code on a machine you care about. A single
bad pointer can corrupt your filesystem or hang the box. Use a throwaway virtual machine (VirtualBox, QEMU, or a
cheap VPS you can rebuild). Take snapshots before testing. Kernel development is the one place in this entire
library where 'just try it and see' can cost you real data — so isolate ruthlessly.

Setting up your lab
sudo apt install build-essential linux-headers-$(uname -r)
sudo apt install kmod
uname -r
ls /lib/modules/$(uname -r)/build

1. build-essential gives you gcc and make; linux-headers provides the kernel's header files, needed to compile any
module against YOUR running kernel.
2. kmod provides insmod, rmmod, modprobe — the module tools.
3. Confirm your kernel version — modules must be built against exactly this version.
4. The build directory for your kernel; if this exists, you are ready to compile modules.





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

1. The kernel uses explicit fixed-width types so behaviour is identical on 32- and 64-bit machines — never rely on int
being a particular size.
2. Used for buffer sizes and lengths.
3. For positions within a device or file.
4. Encodes a device's major and minor numbers (Chapter 6).





3. Your First Kernel Module — Hello, Kernel
The smallest possible module
/* hello.c */
#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/init.h>
static int __init hello_init(void)
{
printk(KERN_INFO "Hello, kernel! Module loaded.\n");
return 0;
}
static void __exit hello_exit(void)
{
printk(KERN_INFO "Goodbye, kernel! Module unloaded.\n");
}
module_init(hello_init);
module_exit(hello_exit);
MODULE_LICENSE("GPL");
MODULE_AUTHOR("MD Abdur Rahim");
MODULE_DESCRIPTION("A first hello-world module");

1. Kernel headers, not user-space ones — module.h is mandatory for any module.
2. The INIT function runs when the module loads. __init tells the kernel it can free this code after init to save memory.
3. printk logs a message; KERN_INFO is the priority level. Returning 0 means 'load succeeded'.
4. The EXIT function runs on unload; __exit marks it as cleanup-only.
5. module_init/module_exit REGISTER these functions as the entry and exit points — the kernel calls them.
6. MODULE_LICENSE is REQUIRED; 'GPL' grants access to GPL-only kernel functions. Without it the kernel 'taints'
and some APIs are hidden.
7. Metadata shown by modinfo.

PRO INSIGHT: Every module has exactly two hooks: an init function (called on load) and an exit function (called on
unload). That is the entire skeleton. Everything else — drivers, filesystems, features — is built by making these two
functions register and unregister the module's real work with the appropriate kernel subsystem. Master this shape
and every module makes structural sense.

The Makefile





# Makefile
obj-m += hello.o
all:
make -C /lib/modules/$(shell uname -r)/build M=$(PWD) modules
clean:
make -C /lib/modules/$(shell uname -r)/build M=$(PWD) clean

1. obj-m += hello.o tells the kernel build system to build hello.c into a module (hello.ko).
2. The all target invokes the KERNEL's build system (-C into its build dir) and points it back at your directory
(M=$(PWD)). This is how modules are always built.
3. clean removes the build artifacts. Note: Makefiles require real TAB characters, not spaces, before commands.





4. The Module Lifecycle — Build, Load, Inspect,
Unload
The full cycle
make
sudo insmod hello.ko
sudo dmesg | tail -3
lsmod | grep hello
modinfo hello.ko
sudo rmmod hello
sudo dmesg | tail -1

1. Compile: produces hello.ko (the 'kernel object' — a loadable module).
2. insmod INSERTS the module into the running kernel — its init function runs now.
3. Check the kernel log: your 'Hello, kernel!' message appears, proving init ran.
4. lsmod lists loaded modules; yours is now among them.
5. modinfo shows the metadata you set (author, license, description).
6. rmmod REMOVES it — the exit function runs.
7. The log now shows 'Goodbye' — confirming clean unload. This build-load-check-unload cycle is your entire
development loop.

PRO INSIGHT: insmod versus modprobe: insmod loads exactly the file you name and fails if it needs other
modules. modprobe is smarter — it looks up modules by name in the system directory and loads DEPENDENCIES
automatically. During development you use insmod (direct, local file); for installed modules the system uses
modprobe. Knowing which to reach for saves confusion when a module 'won't load'.

When a module will not load
Symptom

Usual cause

Fix

'Invalid module format'

Built against a different kernel
version

Rebuild with current linux-headers

'Operation not permitted'

Secure Boot rejects unsigned
modules

Disable Secure Boot in the VM, or
sign the module

'Unknown symbol'

Using a function not exported to
modules

Use an EXPORT_SYMBOL'd API, or
the right header

Module taints kernel

Missing or non-GPL
MODULE_LICENSE

Set MODULE_LICENSE("GPL")

PRACTICE EXERCISES
1. Build, load, inspect with dmesg and lsmod, and unload the hello module. Confirm both messages appear.
2. Run modinfo on your .ko and identify every field you set.
3. Deliberately omit MODULE_LICENSE, rebuild, load, and observe the 'tainted kernel' warning in dmesg.
4. Change the init message, rebuild, and reload — confirming your edit-build-test loop works.





5. Kernel Logging & Parameters
printk and log levels
printk is the kernel's printf, but it writes to the kernel ring buffer (read with dmesg), not to any screen. Its first
argument is a PRIORITY that controls whether the message reaches the console and how it is filtered.
Level

Macro

Meaning

0

KERN_EMERG

System is unusable

1-3

KERN_ALERT/CRIT/ERR

Serious problems

4

KERN_WARNING

Something worth noting

6

KERN_INFO

Informational (most common in
learning)

7

KERN_DEBUG

Debug detail

printk(KERN_INFO "value is %d, pointer %p\n", x, ptr);
pr_info("modern shorthand for KERN_INFO\n");
pr_err("something went wrong: %d\n", err);
dmesg -w

1. Classic printk with format specifiers — %d int, %p pointer, %s string, much like printf.
2. pr_info, pr_err, pr_debug are modern shorthands preferred in new code.
3. dmesg -w FOLLOWS the kernel log live — keep this open in one terminal while developing to see your messages
instantly.

Module parameters — passing values at load time
static int count = 1;
static char *name = "world";
module_param(count, int, 0644);
MODULE_PARM_DESC(count, "how many times to greet");
module_param(name, charp, 0644);
MODULE_PARM_DESC(name, "who to greet");
/* load with values: */
/* sudo insmod hello.ko count=3 name="Abdur" */

1. Declare variables with defaults.
2. module_param exposes 'count' as a load-time parameter: type int, permissions 0644 (visible in /sys).
3. A human description shown by modinfo.
4. charp = a char pointer (string) parameter.
5. At load time you override defaults from the command line — the module reads count=3 and name="Abdur".
Parameters make modules configurable without recompiling.





PRO INSIGHT: Module parameters appear in /sys/module/YOURMODULE/parameters/ as files, thanks to the
permissions you set (0644 = readable by all). This means a running module can be inspected — and with the right
permissions, tuned — through the filesystem, exactly the /sys philosophy from Volume 4. Your module joins the
kernel's 'everything is a file' world automatically.
PRACTICE EXERCISES
1. Add count and name parameters to your hello module; load it with custom values and verify in dmesg.
2. Read the parameter back from /sys/module/hello/parameters/count.
3. Keep dmesg -w open in one terminal while loading/unloading in another; watch messages appear live.
4. Use pr_info and pr_err instead of printk and confirm identical behaviour.





6. Character Device Drivers — the Core Skill
Why character devices
The most common kernel programming task is a character device driver — code that presents hardware
(or a virtual service) as a file in /dev that user programs can read and write byte by byte (Volume 4, Chapter
12). Learning to write one teaches the whole driver model: register a device, define file operations, handle
open/read/write/close.

Device numbers
Every device has a major number (which driver handles it) and a minor number (which specific device).
The kernel routes operations on /dev/mything to your driver by its major number.
#include <linux/fs.h>
#include <linux/cdev.h>
#include <linux/uaccess.h>
static dev_t dev_number;
static struct cdev my_cdev;
/* in init: */
alloc_chrdev_region(&dev_number, 0, 1, "mychardev");

1. Headers: fs.h for file operations, cdev.h for the char-device structure, uaccess.h for user-memory copying.
2. dev_t holds the combined major+minor number.
3. The cdev structure represents your character device to the kernel.
4. alloc_chrdev_region asks the kernel to ALLOCATE a free major number for one device named 'mychardev' — the
modern way (versus hardcoding a major).

The file_operations structure — the heart of a driver
A driver defines what happens when user space opens, reads, writes, or closes its device. These are wired
up through a file_operations structure: a table of function pointers the kernel calls for each operation.





static struct file_operations fops = {
.owner = THIS_MODULE,
.open = my_open,
.read = my_read,
.write = my_write,
.release = my_release,
};
/* in init, after cdev_init(&my_cdev, &fops): */
cdev_add(&my_cdev, dev_number, 1);

1. The operations table maps file actions to YOUR functions.
2. .owner ties the device's lifetime to your module (prevents unloading while in use).
3. .open runs when a program opens /dev/mychardev.
4. .read runs when it reads from the device.
5. .write runs when it writes.
6. .release runs when it closes.
7. cdev_add ACTIVATES the device: from now on, operations on the device file call your functions. Your driver is live.

PRO INSIGHT: This is the universal driver pattern: fill a file_operations table with your functions, register it against a
device number, and create a device file. User programs then use ordinary open/read/write/close on
/dev/yourdevice, and the kernel routes each call to your code. Whether the device is a real sensor or a pure
software service, the shape is identical. Learn this once and you can write any character driver.
PRACTICE EXERCISES
1. Write the init/exit for a character device that allocates a major number and adds a cdev; load it and confirm the
major appears in /proc/devices.
2. Create the device file with mknod (or udev) and verify /dev/mychardev exists.
3. Stub the four fops functions to just pr_info their name; open and cat the device, watching dmesg show which
callbacks fire.
4. Explain the roles of the major and minor numbers in your own words.





7. Talking to User Space — copy_to_user & ioctl
The memory barrier you must respect
User-space and kernel-space memory are separate and protected (Volume 4). A driver CANNOT simply
dereference a pointer that came from a user program — that pointer belongs to a different address space
and may be invalid or malicious. The kernel provides copy_to_user and copy_from_user to move data
safely across the boundary, with validation.
static ssize_t my_read(struct file *f, char __user *buf,
size_t len, loff_t *off)
{
char msg[] = "Hello from the kernel\n";
size_t msglen = sizeof(msg);
if (*off >= msglen) return 0; /* EOF */
if (len > msglen - *off) len = msglen - *off;
if (copy_to_user(buf, msg + *off, len))
return -EFAULT;
*off += len;
return len;
}

1. read receives a __user pointer (buf) — the annotation marks it as untrusted user memory.
2. Our data to send up.
3. If the offset is past the end, return 0 = end of file. This is how cat knows to stop.
4. Never copy more than what remains or what was asked.
5. copy_to_user safely moves kernel data INTO the user's buffer; it returns non-zero on failure...
6. ...in which case we return -EFAULT (bad address). NEVER use memcpy to user pointers.
7. Advance the offset so the next read continues, and return how many bytes we gave.

PRO INSIGHT: copy_to_user and copy_from_user are not optional politeness — they are security-critical. They
validate that the user pointer really belongs to the calling process and handle the address-space translation.
Dereferencing a raw user pointer directly is a classic, dangerous kernel bug that can crash the system or leak
kernel memory to an attacker. Every byte crossing the user/kernel boundary goes through these functions. No
exceptions.

ioctl — commands beyond read and write
Sometimes a device needs COMMANDS, not just data streams — 'eject', 'set speed', 'get status'. The ioctl
(input/output control) operation handles these: user space sends a command number and optional argument,
and the driver acts on it. It is the escape hatch for device-specific control.





static long my_ioctl(struct file *f, unsigned int cmd,
unsigned long arg)
{
switch (cmd) {
case MY_RESET: do_reset(); break;
case MY_GET_VER: return VERSION;
default: return -ENOTTY; /* unknown command */
}
return 0;
}

1. ioctl receives a command number and an argument.
2. Dispatch on the command...
3. ...each case performs a device-specific action...
4. ...or returns a value.
5. -ENOTTY is the conventional 'this ioctl is not supported' error.
6. ioctl is how tools like hdparm and mount configure devices — commands that do not fit the read/write model.

PRACTICE EXERCISES
1. Implement my_read that returns a fixed string using copy_to_user; cat your device and see it.
2. Implement my_write that copies user data in with copy_from_user and pr_info's it.
3. Add an ioctl with a RESET command and a GET_VERSION command; test from a small user program.
4. Explain why memcpy from a user pointer is a security bug and copy_from_user is not.





8. Kernel Memory Management
Allocating memory in the kernel
There is no malloc. The kernel offers several allocators, each for a purpose. The most common is kmalloc,
which returns physically contiguous memory, fast, for small allocations.
#include <linux/slab.h>
char *buf = kmalloc(1024, GFP_KERNEL);
if (!buf)
return -ENOMEM;
/* ... use buf ... */
kfree(buf);
char *zbuf = kzalloc(1024, GFP_KERNEL); /* zeroed */
void *big = vmalloc(1024 * 1024); /* large, virtually contiguous */

1. slab.h provides the allocators.
2. kmalloc(size, flags): allocate 1024 bytes. GFP_KERNEL means 'normal allocation, may sleep to find memory'.
3. ALWAYS check for NULL — kernel allocations genuinely fail, and ignoring it crashes the system...
4. ...return -ENOMEM (out of memory) if so.
5. kfree releases it. Every kmalloc needs a matching kfree, or you leak kernel memory permanently (until reboot).
6. kzalloc is kmalloc plus zeroing — use when you need clean memory.
7. vmalloc for LARGE buffers: virtually contiguous (not physically), slower, but can get big blocks kmalloc cannot.

The GFP flags — context matters
Flag

Meaning

Use when

GFP_KERNEL

Normal; may sleep to reclaim
memory

In normal process context

GFP_ATOMIC

Must not sleep; may fail sooner

In interrupt context (Chapter 10)

GFP_DMA

Memory usable for DMA hardware

Device drivers needing DMA buffers

PRO INSIGHT: The sleep question governs everything in the kernel. GFP_KERNEL may SLEEP — pause the
current task while the kernel frees memory. That is fine in normal context but FORBIDDEN in interrupt context,
where there is no task to sleep. Using GFP_KERNEL in an interrupt handler is a serious bug. This 'can I sleep
here?' question recurs constantly in kernel code, and knowing the answer for your context is a core skill.

Memory leaks are forever
In user space, a leaked allocation is reclaimed when the program exits. In the kernel, there is no exit — a
leaked kmalloc is gone until the machine reboots. Kernel memory discipline is therefore absolute: every
allocation has an owner and a matching free, checked on every code path including error paths. This is why
kernel code uses careful goto-based cleanup (the one place goto is idiomatic in C).





ptr1 = kmalloc(...); if (!ptr1) goto fail;
ptr2 = kmalloc(...); if (!ptr2) goto fail_ptr1;
return 0;
fail_ptr1:
kfree(ptr1);
fail:
return -ENOMEM;

1. Allocate; on failure jump to cleanup.
2. Allocate the second; on failure jump to a label that frees the FIRST.
3. Success path.
4. Cleanup labels unwind in REVERSE order of allocation — freeing exactly what was allocated so far. This goto-ladder
is the standard, correct kernel cleanup pattern, not bad style.





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

1. Define a mutex.
2. mutex_lock: only one thread enters; others SLEEP until it is free. Use in process context.
3. The protected operation.
4. Release.
5. Define a spinlock for cases where you cannot sleep.
6. spin_lock_irqsave also DISABLES interrupts on this CPU (saving their state in flags) — needed when the data is also
touched by an interrupt handler.
7. The protected operation, now safe even against interrupts.
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





10. Interrupts & Deferred Work
What an interrupt handler does
When hardware needs attention (a key pressed, a packet arrived, a disk finished), it raises an interrupt, and
the kernel runs your driver's interrupt handler (Volume 4, Chapter 10). The handler runs in a special,
restricted context: it must be FAST, it CANNOT sleep, and it cannot do slow work. This creates the central
challenge of interrupt handling.
static irqreturn_t my_handler(int irq, void *dev_id)
{
/* do the MINIMUM: acknowledge hardware, grab data */
schedule_work(&my_work); /* defer the slow part */
return IRQ_HANDLED;
}
/* in init: */
request_irq(irq_number, my_handler, IRQF_SHARED, "mydev", dev);

1. An interrupt handler returns irqreturn_t.
2. Do only the urgent minimum here — this context is time-critical and cannot sleep.
3. schedule_work DEFERS the slow processing to a safer context that CAN sleep (the 'bottom half').
4. IRQ_HANDLED tells the kernel this interrupt was ours and dealt with.
5. request_irq registers your handler for a given interrupt line; IRQF_SHARED allows sharing the line with other
devices.

Top half and bottom half
The solution to 'handlers must be fast but work takes time' is to split it. The top half (the interrupt handler)
does the urgent minimum and returns instantly. It schedules a bottom half (a workqueue or tasklet) to do the
heavy processing later, in a context where sleeping and slow work are allowed. This split keeps the system
responsive while still handling every event.
Mechanism

Context

Can sleep?

Use

Workqueue

Process context

Yes

Slow work: I/O, allocation,
sleeping

Tasklet/softirq

Interrupt context

No

Fast deferred work

Threaded IRQ

Dedicated kernel thread

Yes

Modern, clean approach

PRO INSIGHT: The top-half/bottom-half split is the defining pattern of interrupt handling. The top half is a sprinter
— in and out as fast as possible, no sleeping, just acknowledge and defer. The bottom half is the workhorse — it
does the real processing later where it is safe to be slow. Getting this division right is what keeps a driver from
freezing the whole system every time its device fires an interrupt. It is the interrupt-context answer to the same 'can
I sleep here?' question.





11. Debugging the Kernel
You cannot just attach a debugger
Debugging kernel code is harder than user space — a breakpoint can freeze the machine, and there is no
comfortable gdb-on-a-running-process by default. Kernel developers rely on a different toolkit, with printk still
the workhorse.
Tool

What it does

When

printk / dmesg

Log messages from your code

Always — the primary tool

Kernel oops/panic

The kernel's crash report

Read it — it names the fault

ftrace

Trace kernel function calls

Seeing what the kernel actually does

kgdb

Remote gdb over serial

Real breakpoint debugging (two
machines)

QEMU + gdb

Debug a kernel in a VM from outside

The practical modern lab setup

lockdep

Runtime deadlock detector

Catch lock-ordering bugs while
testing

KASAN

Detects memory errors

Catch buffer overflows, use-after-free

Reading a kernel oops
When kernel code hits a bad pointer, the kernel prints an oops — a crash report — and often continues (or
panics if severe). Learning to read it is essential: it shows the faulting instruction, a call trace (which functions
led there), and the register state. The call trace is gold — it points almost directly at your bug.
dmesg | tail -40
sudo dmesg -w
cat /proc/sys/kernel/panic
echo 1 | sudo tee /sys/module/YOURMOD/parameters/debug

1. After a crash, the oops is in the kernel log — read the call trace from the bottom up to find where your code was.
2. Follow the log live while reproducing the bug.
3. How the system behaves on panic (0 = halt and wait so you can read it; useful in a VM).
4. If your module has a debug parameter, toggle verbose logging at runtime — a common self-debugging pattern.

PRO INSIGHT: The single best kernel-debugging setup for learning: run your target kernel inside QEMU, and
attach gdb from your host machine. This gives you real breakpoints and inspection WITHOUT risking a real
machine — if the kernel panics, you just restart the VM. Combined with printk for quick checks and KASAN for
memory bugs, this is how modern kernel developers work. Set this up early; it turns terrifying crashes into ordinary
debugging.
PRACTICE EXERCISES
1. Deliberately dereference a NULL pointer in your module, load it, and READ the resulting oops call trace.
2. Add a debug module parameter that enables verbose pr_debug logging at runtime.
3. Set up a kernel in QEMU and follow its dmesg from the host.





4. Enable lockdep in your dev kernel and write two functions that lock in opposite order to see it caught.





12. The Kernel Source, Coding Style & Contributing
Getting and navigating the source
git clone --depth 1 https://github.com/torvalds/linux.git
cd linux
ls
make menuconfig
scripts/get_maintainer.pl -f drivers/char/mem.c

1. Clone the kernel source (--depth 1 for just the latest, saving gigabytes and time).
2. The top level: drivers/ (all device drivers), kernel/ (core), mm/ (memory), fs/ (filesystems), net/ (networking),
Documentation/.
3. The configuration menu — choose what to build into the kernel or as modules.
4. get_maintainer.pl tells you WHO maintains a file — essential before submitting a patch, since you email it to them.

Kernel coding style — non-negotiable
Rule

The kernel way

Indentation

TABS, 8 characters wide

Braces

Opening brace on same line (except functions)

Line length

Aim for 80 columns

Naming

lower_case_with_underscores, short

Comments

/* C-style */, explain WHY not what

No typedefs for structs

Use 'struct foo', not a hidden typedef

scripts/checkpatch.pl --file drivers/char/mydriver.c

1. checkpatch.pl automatically checks your code against the kernel style rules. Run it before EVER submitting —
maintainers will reject style violations immediately. It catches whitespace, naming, and structural issues.

How a contribution actually happens
The Linux kernel is developed by email patches, not pull requests. The workflow: make your change,
commit it with a clear message, generate a patch with git format-patch, check it with checkpatch, then send
it with git send-email to the maintainer and mailing list found via get_maintainer.pl. Maintainers review,
request changes, and eventually a patch is accepted into a subsystem tree, then Linus's tree. It is rigorous,
public, and meritocratic.
PRO INSIGHT: A realistic first contribution: start in drivers/staging/ (drivers being cleaned up) or with
Documentation fixes and checkpatch cleanups. These are welcomed from newcomers and teach the workflow
without deep subsystem knowledge. Every kernel contributor started with a small patch. Your name in the Linux
kernel git history is an achievable, career-defining goal — and it begins with one correctly-formatted,
checkpatch-clean patch emailed to the right maintainer.
PRACTICE EXERCISES





1. Clone the kernel source and explore drivers/char/ to see real character drivers like the ones you now understand.
2. Run checkpatch.pl on your own driver and fix every warning.
3. Use get_maintainer.pl on a file to see who you would email a patch to.
4. Read Documentation/process/submitting-patches.rst — the official contribution guide.





13. A Complete Driver — Worked End to End
Here is a full, working character device driver that stores a message you can write to it and read back — a
'virtual notepad' device. It combines every concept: module lifecycle, character device registration, file
operations, safe user-space copying, and cleanup. Study it as the integration of the whole volume.

The complete source — part 1: state and file operations
#include <linux/module.h>
#include <linux/fs.h>
#include <linux/cdev.h>
#include <linux/uaccess.h>
#include <linux/slab.h>
#define DEVICE_NAME "notepad"
#define BUF_SIZE 1024
static dev_t dev_number;
static struct cdev my_cdev;
static struct class *dev_class;
static char *buffer;
static size_t data_len;
static int np_open(struct inode *i, struct file *f)
{
pr_info("notepad: opened\n");
return 0;
}
static ssize_t np_read(struct file *f, char __user *ubuf,
size_t len, loff_t *off)
{
if (*off >= data_len) return 0;
if (len > data_len - *off) len = data_len - *off;
if (copy_to_user(ubuf, buffer + *off, len)) return -EFAULT;
*off += len;
return len;
}
static ssize_t np_write(struct file *f, const char __user *ubuf,
size_t len, loff_t *off)
{
if (len > BUF_SIZE) len = BUF_SIZE;
if (copy_from_user(buffer, ubuf, len)) return -EFAULT;
data_len = len;
return len;
}

1. All the headers from Chapters 6 to 8.
2. The device name (appears as /dev/notepad) and buffer size.
3. State: the device number, the cdev, a device class (for auto-creating the /dev entry), the storage buffer, and how
much data it holds.
4. open: just logs. Returning 0 means success.
5. read: the safe pattern from Chapter 7 — respect the offset, clamp length, copy_to_user, advance, return the count.
6. write: clamp to buffer size, copy_from_user the new content, record its length.





The complete source — part 2: registration and cleanup
static struct file_operations fops = {
.owner = THIS_MODULE,
.open = np_open,
.read = np_read,
.write = np_write,
};
static int __init np_init(void)
{
buffer = kzalloc(BUF_SIZE, GFP_KERNEL);
if (!buffer) return -ENOMEM;
alloc_chrdev_region(&dev_number, 0, 1, DEVICE_NAME);
cdev_init(&my_cdev, &fops);
cdev_add(&my_cdev, dev_number, 1);
dev_class = class_create(DEVICE_NAME);
device_create(dev_class, NULL, dev_number, NULL, DEVICE_NAME);
pr_info("notepad: loaded, major %d\n", MAJOR(dev_number));
return 0;
}
static void __exit np_exit(void)
{
device_destroy(dev_class, dev_number);
class_destroy(dev_class);
cdev_del(&my_cdev);
unregister_chrdev_region(dev_number, 1);
kfree(buffer);
pr_info("notepad: unloaded\n");
}
module_init(np_init);
module_exit(np_exit);
MODULE_LICENSE("GPL");
MODULE_AUTHOR("MD Abdur Rahim");
MODULE_DESCRIPTION("A virtual notepad character device");

1. The operations table wiring file actions to our functions.
2. init: allocate the buffer (checked!), get a major number, register the cdev, and create the /dev/notepad file
automatically via a device class.
3. MAJOR() extracts the major number for logging.
4. exit: tear down in REVERSE order of creation — destroy device, class, cdev, region, then free the buffer.
Mirror-image cleanup prevents leaks and dangling references.
5. Standard registration and metadata.

Building and testing it





make
sudo insmod notepad.ko
echo "Assalamu alaikum" | sudo tee /dev/notepad
sudo cat /dev/notepad
sudo rmmod notepad

1. Build the module.
2. Load it — /dev/notepad appears automatically.
3. WRITE to the device: your np_write stores the text in the kernel buffer.
4. READ it back: np_read returns what you stored. You have round-tripped data through kernel space.
5. Unload; the device vanishes and the buffer is freed. A complete, working driver you built and understand line by line.

PRO INSIGHT: This one driver is the whole volume made concrete. It registers with the kernel, exposes a file in
/dev, safely exchanges data with user space across the protection boundary, allocates and frees kernel memory
correctly, and cleans up in exact reverse order. Every real character driver — for a sensor, a serial port, a custom
board — has this exact skeleton. You now have a template you understand completely, which is the foundation of
all driver work.





14. Exercises with Full Solutions
Answers to the key exercises across the volume. Build and test each in your VM.

Ch.4 — Observing a tainted kernel
/* Remove this line, rebuild, load: */
/* MODULE_LICENSE("GPL"); */
/* dmesg shows: */
/* module verification failed: signature and/or */
/* required key missing - tainting kernel */

1. Without MODULE_LICENSE, the kernel marks itself 'tainted' and hides GPL-only symbols. The dmesg warning is the
kernel telling you it no longer trusts its own integrity for bug reports. Always set the license — this exercise shows why
the warning exists.

Ch.6 — Confirming your major number
cat /proc/devices | grep mychardev
ls -l /dev/mychardev

1. /proc/devices lists registered drivers with their major numbers, proving your cdev registered. The device file's major
(shown by ls -l) must match, confirming the routing from /dev/mychardev to your driver is correct.

Ch.7 — A working write handler
static ssize_t my_write(struct file *f, const char __user *ubuf,
size_t len, loff_t *off)
{
char kbuf[128];
if (len > 127) len = 127;
if (copy_from_user(kbuf, ubuf, len)) return -EFAULT;
kbuf[len] = '\0';
pr_info("user wrote: %s\n", kbuf);
return len; /* report all bytes consumed */
}

1. Clamp to the buffer, copy_from_user safely, null-terminate before treating as a string, log it, and return len so the
writing program believes all its bytes were accepted. Returning fewer would make it retry. Note the mandatory
copy_from_user, never a raw dereference.

Ch.8 — Correct allocation with error path
buffer = kzalloc(BUF_SIZE, GFP_KERNEL);
if (!buffer)
return -ENOMEM;
/* ...later, always: */
kfree(buffer);

1. kzalloc gives zeroed memory; the NULL check is mandatory because kernel allocations fail for real. Every allocation
is paired with a kfree on every exit path — the discipline that prevents permanent kernel memory leaks.

Ch.9 — Choosing the right lock