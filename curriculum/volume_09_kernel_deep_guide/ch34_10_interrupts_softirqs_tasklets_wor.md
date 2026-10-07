10. Interrupts, Softirqs, Tasklets, Workqueues &
Threaded IRQ
The full deferral toolkit
Volume 8 introduced the top-half/bottom-half split. Here is the complete set of deferral mechanisms and
precisely when each applies.
Mechanism

Runs in

Sleeps?

Use when

Hardirq handler

Interrupt context

No

The urgent minimum: ack,
grab data

softirq

Interrupt context

No

High-frequency core work
(net, block) —
kernel-defined only

tasklet

Interrupt context (on
softirq)

No

Simple deferred work,
serialised per tasklet

workqueue

Process context (kthread)

Yes

Work that may sleep: I/O,
allocation, locks

threaded IRQ

Dedicated kernel thread

Yes

Modern default: handler
that can sleep

Threaded IRQ — the modern approach
static irqreturn_t hard_handler(int irq, void *dev)
{
if (!is_ours(dev)) return IRQ_NONE;
return IRQ_WAKE_THREAD; /* defer to the thread */
}
static irqreturn_t thread_handler(int irq, void *dev)
{
/* runs in a kthread — MAY sleep, take mutexes, do I/O */
process_data(dev);
return IRQ_HANDLED;
}
request_threaded_irq(irq, hard_handler, thread_handler,
IRQF_SHARED, "mydev", dev);