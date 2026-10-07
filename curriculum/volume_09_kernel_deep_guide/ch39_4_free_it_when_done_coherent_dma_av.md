4. Free it when done. Coherent DMA avoids manual cache management; streaming DMA (dma_map_single) is faster
but needs explicit sync.

PRO INSIGHT: DMA is where Volume 4's theory becomes physical: the device writes directly into RAM you
allocated, and interrupts you when done — the CPU never copies the bulk data. The subtleties that bite: the device
sees a DIFFERENT address than the CPU (bus vs virtual), and CPU caches can hold stale copies of DMA memory
(hence coherent allocations or explicit dma_sync calls). Get the addressing or cache handling wrong and you get
silent data corruption, the hardest kind of bug. Respect the DMA API precisely.