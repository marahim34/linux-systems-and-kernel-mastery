5. Writing a file CHANGES kernel behaviour: this switches on packet forwarding. The filesystem interface is read AND
write.

PRO INSIGHT: Unique point: /proc and /sys turn kernel introspection into text manipulation. On most operating
systems, inspecting kernel state requires special APIs and programming. On Linux, cat and echo are enough. This
is the 'everything is a file' philosophy applied to the kernel itself — and it is why Linux is the OS you can fully
understand from the command line.

What the kernel does NOT do
A crucial clarification. The kernel does not include the shell, the desktop, the compiler, or the utilities like ls
and grep. Those are user-space programs, mostly from the GNU project, which is why purists call the
system 'GNU/Linux'. The kernel provides mechanism (the ability to run programs, access files); user space
provides the actual programs. Keeping this line clear resolves endless confusion.