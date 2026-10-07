3. The Kernel — the Heart of the System
What the kernel actually is
The kernel is a single program — a large C program of about 30 million lines — that loads into protected
memory at boot and stays running until shutdown. It is not a process you can see in your process list,
because it IS the thing that runs processes. Everything else on the machine exists at its pleasure. Its job is to
be the sole manager of four things:
Subsystem

Manages

Covered in

Process management

Creating, running, ending programs

Chapters 4–5

Memory management

Who gets which RAM, the
virtual-memory illusion