# Tier 4 · Chapter 1: Linux Kernel Architecture & Source Tour

Synthesized from Robert Love's *Linux Kernel Development* & Bovet's *Understanding the Linux Kernel*.

## 1. Monolithic Kernel with Modularity
The Linux kernel is a monolithic design: all core subsystems (scheduler, virtual memory, filesystems, network stack, device drivers) execute in a single unified privileged address space (**Ring 0**).
However, it gains microkernel-like flexibility through **Loadable Kernel Modules (LKMs)**, allowing code to be loaded and unloaded dynamically into the running kernel without rebooting.

## 2. Core Kernel Subsystems
1. **Process Scheduler (CFS / EEVDF)**: Manages CPU time allocation among threads.
2. **Memory Management (MM)**: Page tables, TLB management, buddy allocator, SLAB/SLUB cache, virtual memory areas (`vm_area_struct`).
3. **Virtual Filesystem (VFS)**: Abstract layer providing uniform file interface across ext4, btrfs, nfs, procfs, sysfs via `inode`, `dentry`, `file`, and `super_block` objects.
4. **Network Stack**: BSD socket layer, TCP/IP stack, sk_buff packet buffers, netdevice drivers.
5. **Device Drivers**: Character devices, block devices, platform devices.

## 3. Kernel Space vs User Space Rules
- **No glibc**: You cannot use `printf()`, `malloc()`, `exit()`, or `<stdio.h>`. You use `printk()`, `kmalloc()`, etc.
- **Small fixed stack**: Kernel stack is strictly limited (typically 8KB or 16KB per thread). Never allocate large buffers on stack!
- **Floating point forbidden**: FP registers are not saved on kernel entry for performance reasons.
- **Never dereference user pointers directly**: User memory can be swapped out, invalid, or malicious. Always use `copy_to_user()` and `copy_from_user()`.
