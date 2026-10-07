/* Data touched only in process context, may take time: */
mutex_lock(&lock); ... mutex_unlock(&lock);
/* Data ALSO touched by an interrupt handler: */
spin_lock_irqsave(&slock, flags);
...
spin_unlock_irqrestore(&slock, flags);