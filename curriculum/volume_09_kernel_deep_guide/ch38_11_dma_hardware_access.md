11. DMA & Hardware Access
Reaching the hardware
Drivers talk to devices through memory-mapped registers and move bulk data with DMA. Both have strict
rules the kernel enforces, because raw hardware access from the wrong place corrupts systems.
void __iomem *regs = devm_ioremap_resource(&pdev->dev, res);
u32 status = readl(regs + STATUS_REG);
writel(START_BIT, regs + CTRL_REG);

1. ioremap maps a device's physical register block into kernel virtual address space; the devm_ version auto-unmaps on
unbind. The __iomem annotation marks it as device memory, not normal RAM.
2. readl/readb/readw read device registers with the correct barriers and byte ordering — never dereference __iomem
pointers directly.
3. writel writes a register. These accessors ensure ordering and portability across architectures.

DMA — letting the device read/write memory directly
dma_addr_t dma_handle;
void *cpu_buf = dma_alloc_coherent(&pdev->dev, SIZE,
&dma_handle, GFP_KERNEL);
/* give dma_handle to the device; use cpu_buf from the CPU */
/* ... device transfers data ... */
dma_free_coherent(&pdev->dev, SIZE, cpu_buf, dma_handle);

1. dma_addr_t is the address the DEVICE uses (a bus address), distinct from the CPU pointer.
2. dma_alloc_coherent allocates a buffer both the CPU and device can access consistently, returning BOTH a CPU
pointer (cpu_buf) and a device address (dma_handle).