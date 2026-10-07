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