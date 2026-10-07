4. When the device unbinds or probe fails, the core frees this automatically. No matching free, no leak on error paths.
This is the modern, preferred style for driver resource management — embrace it.

PRO INSIGHT: The allocation-context matrix you must hold in your head: GFP_KERNEL may sleep (process
context only); GFP_ATOMIC never sleeps but is more likely to fail (interrupt context); large allocations prefer
vmalloc; high-frequency same-size objects use a slab cache; and driver resources should use devm_ so cleanup is
automatic. Getting the allocator AND the flags right for your context and pattern is what separates robust kernel
code from code that works on your desk and fails under production memory pressure.