4. IRQ_HANDLED tells the kernel this interrupt was ours and dealt with.
5. request_irq registers your handler for a given interrupt line; IRQF_SHARED allows sharing the line with other
devices.

Top half and bottom half
The solution to 'handlers must be fast but work takes time' is to split it. The top half (the interrupt handler)
does the urgent minimum and returns instantly. It schedules a bottom half (a workqueue or tasklet) to do the
heavy processing later, in a context where sleeping and slow work are allowed. This split keeps the system
responsive while still handling every event.
Mechanism

Context

Can sleep?

Use

Workqueue

Process context

Yes

Slow work: I/O, allocation,
sleeping

Tasklet/softirq

Interrupt context

No

Fast deferred work

Threaded IRQ

Dedicated kernel thread

Yes

Modern, clean approach

PRO INSIGHT: The top-half/bottom-half split is the defining pattern of interrupt handling. The top half is a sprinter
— in and out as fast as possible, no sleeping, just acknowledge and defer. The bottom half is the workhorse — it
does the real processing later where it is safe to be slow. Getting this division right is what keeps a driver from
freezing the whole system every time its device fires an interrupt. It is the interrupt-context answer to the same 'can
I sleep here?' question.