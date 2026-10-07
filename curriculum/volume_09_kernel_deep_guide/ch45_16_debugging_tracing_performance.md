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