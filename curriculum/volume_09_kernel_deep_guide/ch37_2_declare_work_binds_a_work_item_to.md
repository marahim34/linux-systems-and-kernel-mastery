2. DECLARE_WORK binds a work item to the function.
3. schedule_work queues it onto the system workqueue; a kernel thread runs it soon. Use this from a hardirq to defer
sleeping work safely.

PRO INSIGHT: The decision tree for deferred work: if it MUST be fast and cannot sleep, keep it in the hardirq or a
tasklet. If it may sleep (allocation, I/O, mutex), it MUST go to a workqueue or a threaded IRQ. The modern,
recommended default for device interrupts is request_threaded_irq — it gives you a tiny atomic top half and a
sleep-capable bottom half with minimal boilerplate. Reaching for the right mechanism, matched to whether the work
can sleep, is core interrupt-handling competence.