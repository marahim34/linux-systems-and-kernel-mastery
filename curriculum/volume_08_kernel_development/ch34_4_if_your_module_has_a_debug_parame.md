4. If your module has a debug parameter, toggle verbose logging at runtime — a common self-debugging pattern.

PRO INSIGHT: The single best kernel-debugging setup for learning: run your target kernel inside QEMU, and
attach gdb from your host machine. This gives you real breakpoints and inspection WITHOUT risking a real
machine — if the kernel panics, you just restart the VM. Combined with printk for quick checks and KASAN for
memory bugs, this is how modern kernel developers work. Set this up early; it turns terrifying crashes into ordinary
debugging.
PRACTICE EXERCISES