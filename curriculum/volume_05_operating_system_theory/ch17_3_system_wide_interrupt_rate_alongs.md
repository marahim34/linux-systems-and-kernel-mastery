3. System-wide interrupt rate; alongside context switches, the pulse of kernel activity.

PRO INSIGHT: The buffering insight: the kernel sits between fast devices and slow ones (and between applications
and hardware) using BUFFERS and CACHES. The page cache from Volume 4 is exactly this — data read once
stays buffered in RAM so the next read skips the slow device. I/O theory is largely the art of hiding slow hardware
behind fast memory. Every layer buffers.
PRACTICE EXERCISES