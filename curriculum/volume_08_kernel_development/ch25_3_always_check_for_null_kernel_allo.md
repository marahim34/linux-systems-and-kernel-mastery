3. ALWAYS check for NULL — kernel allocations genuinely fail, and ignoring it crashes the system...
4. ...return -ENOMEM (out of memory) if so.
5. kfree releases it. Every kmalloc needs a matching kfree, or you leak kernel memory permanently (until reboot).
6. kzalloc is kmalloc plus zeroing — use when you need clean memory.
7. vmalloc for LARGE buffers: virtually contiguous (not physically), slower, but can get big blocks kmalloc cannot.

The GFP flags — context matters
Flag

Meaning

Use when

GFP_KERNEL

Normal; may sleep to reclaim
memory

In normal process context

GFP_ATOMIC

Must not sleep; may fail sooner

In interrupt context (Chapter 10)

GFP_DMA

Memory usable for DMA hardware

Device drivers needing DMA buffers

PRO INSIGHT: The sleep question governs everything in the kernel. GFP_KERNEL may SLEEP — pause the
current task while the kernel frees memory. That is fine in normal context but FORBIDDEN in interrupt context,
where there is no task to sleep. Using GFP_KERNEL in an interrupt handler is a serious bug. This 'can I sleep
here?' question recurs constantly in kernel code, and knowing the answer for your context is a core skill.

Memory leaks are forever
In user space, a leaked allocation is reclaimed when the program exits. In the kernel, there is no exit — a
leaked kmalloc is gone until the machine reboots. Kernel memory discipline is therefore absolute: every
allocation has an owner and a matching free, checked on every code path including error paths. This is why
kernel code uses careful goto-based cleanup (the one place goto is idiomatic in C).





ptr1 = kmalloc(...); if (!ptr1) goto fail;
ptr2 = kmalloc(...); if (!ptr2) goto fail_ptr1;
return 0;
fail_ptr1:
kfree(ptr1);
fail:
return -ENOMEM;