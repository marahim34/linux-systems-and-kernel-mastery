10. Input / Output — How the Kernel Talks to Devices
The three ways to do I/O
Method

How

Cost

Programmed I/O

CPU polls the device in a loop until
ready

Wastes CPU entirely while waiting

Interrupt-driven

CPU does other work; device
INTERRUPTS when ready

Efficient; an interrupt per chunk

DMA

A controller moves data to RAM
directly, interrupts once at the end

CPU freed almost entirely

The evolution is a story of freeing the CPU. Early systems polled (wasteful). Interrupts let the CPU work while
waiting. Direct Memory Access (DMA) lets a dedicated controller shuttle data straight into RAM, interrupting
the CPU only when the whole transfer is done. This is how your SSD fills memory in the Volume 4 file-read
journey without the CPU copying every byte.

Interrupts — the device's way to get attention
An interrupt is a hardware signal that makes the CPU pause its current work, jump to a kernel interrupt
handler, deal with the device, then resume exactly where it left off. Interrupts are how a keyboard press, a
completed disk read, or an arriving network packet reach the kernel instantly, without the CPU constantly
checking. Chapter 5's context switch and this are close cousins.
cat /proc/interrupts | head
watch -n1 "cat /proc/interrupts | grep -E 'eth|nvme'"
vmstat 1 3 # the 'in' column counts interrupts per second