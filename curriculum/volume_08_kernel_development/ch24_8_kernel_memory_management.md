8. Kernel Memory Management
Allocating memory in the kernel
There is no malloc. The kernel offers several allocators, each for a purpose. The most common is kmalloc,
which returns physically contiguous memory, fast, for small allocations.
#include <linux/slab.h>
char *buf = kmalloc(1024, GFP_KERNEL);
if (!buf)
return -ENOMEM;
/* ... use buf ... */
kfree(buf);
char *zbuf = kzalloc(1024, GFP_KERNEL); /* zeroed */
void *big = vmalloc(1024 * 1024); /* large, virtually contiguous */

1. slab.h provides the allocators.
2. kmalloc(size, flags): allocate 1024 bytes. GFP_KERNEL means 'normal allocation, may sleep to find memory'.