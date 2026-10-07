3. Even a trivial 'echo hello' makes dozens of system calls just to start up, load libraries, and print. Nothing happens
without the kernel.

PRO INSIGHT: Unique point: the system-call interface is a STABLE CONTRACT that almost never breaks. A
program compiled for Linux in 1995 can often still run today because the kernel keeps its promise: 'these calls will
keep working.' Linus Torvalds enforces one rule above all — 'we do not break user space.' This
backward-compatibility discipline is a major reason Linux dominates: businesses trust that their software will keep
running for decades.