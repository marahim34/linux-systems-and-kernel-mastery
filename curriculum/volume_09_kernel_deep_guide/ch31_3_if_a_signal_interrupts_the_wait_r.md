3. If a signal interrupts the wait, return -ERESTARTSYS so the syscall is retried or reported correctly. Handling signals
is mandatory for correctness.