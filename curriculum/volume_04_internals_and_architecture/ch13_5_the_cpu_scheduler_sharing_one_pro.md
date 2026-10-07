5. The CPU Scheduler — Sharing One Processor
Among Many
The illusion of simultaneity
Your machine runs hundreds of processes but has only a handful of CPU cores. How do they all seem to run
at once? The kernel's scheduler gives each process a tiny slice of CPU time — a few milliseconds — then
switches to the next, hundreds of times per second. The switching is so fast that everything APPEARS
simultaneous. This is time-sharing, and it is the scheduler's entire purpose.

The context switch
Each time the scheduler moves from one process to another, it performs a context switch: it saves the exact
state of the outgoing process (all CPU register values, the program counter) into memory, and loads the state
of the incoming one. The process being paused never notices; when its turn comes again, it resumes exactly
where it stopped, as if time had not passed.
vmstat 1 5
# the 'cs' column = context switches per second
cat /proc/interrupts | head
grep ctxt /proc/stat