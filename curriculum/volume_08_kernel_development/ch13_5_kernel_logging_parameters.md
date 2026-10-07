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