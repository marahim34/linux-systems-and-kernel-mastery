5. Define a spinlock for cases where you cannot sleep.
6. spin_lock_irqsave also DISABLES interrupts on this CPU (saving their state in flags) — needed when the data is also
touched by an interrupt handler.