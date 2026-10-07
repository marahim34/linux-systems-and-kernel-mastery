6. Memory — Virtual Memory & the Great Illusion
The problem
Many processes run at once, each needing memory. If they all shared the same physical RAM addresses
directly, they would constantly overwrite each other, and a program written for one machine's memory layout
would not run on another. The solution is one of the deepest ideas in computing: virtual memory.

The illusion each process is given
The kernel gives EVERY process its own private, enormous, continuous view of memory — its virtual
address space — as if it alone owned the whole machine. Process A's address 0x400000 and process B's
address 0x400000 are completely different physical locations. Neither can see or touch the other's memory.
Each process lives in a perfect private bubble.
PRO INSIGHT: This is the illusion that makes modern computing possible. Each process THINKS it has the whole
machine to itself, in one clean continuous stretch of memory starting from zero. In reality the kernel and the CPU's
memory-management unit (MMU) translate these fake addresses to scattered real ones, invisibly, billions of times
per second. Isolation, security, and simplicity all flow from this one trick.

How the translation works — pages
Memory is managed in fixed chunks called pages, usually 4 kilobytes each. The kernel keeps a page table
for every process, mapping its virtual pages to physical frames in RAM. When a process reads a virtual
address, the MMU consults this table to find the real location. If the page is not currently in RAM, a page
fault occurs and the kernel fetches it.
Term

Meaning

Page

A fixed-size chunk of virtual memory (typically 4 KB)

Frame

A physical chunk of RAM the same size as a page

Page table

Per-process map from virtual pages to physical frames

Page fault

A needed page is not in RAM; the kernel must load it

MMU

Hardware that performs the translation on every access

Swapping — using disk as overflow RAM
When RAM fills up, the kernel moves less-used pages out to disk (the swap area), freeing frames for active
work. If a swapped-out page is needed again, a page fault brings it back. Swap makes the machine survive
memory pressure — slowly, but without crashing. This is exactly why Volume 1 insisted you add swap to a
small VPS.





cat /proc/meminfo | grep -E "MemTotal|MemAvailable|SwapTotal"
free -h
cat /proc/self/maps | head
sudo cat /proc/1234/smaps_rollup 2>/dev/null | head