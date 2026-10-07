10. Interrupts & Deferred Work
What an interrupt handler does
When hardware needs attention (a key pressed, a packet arrived, a disk finished), it raises an interrupt, and
the kernel runs your driver's interrupt handler (Volume 4, Chapter 10). The handler runs in a special,
restricted context: it must be FAST, it CANNOT sleep, and it cannot do slow work. This creates the central
challenge of interrupt handling.
static irqreturn_t my_handler(int irq, void *dev_id)
{
/* do the MINIMUM: acknowledge hardware, grab data */
schedule_work(&my_work); /* defer the slow part */
return IRQ_HANDLED;
}
/* in init: */
request_irq(irq_number, my_handler, IRQF_SHARED, "mydev", dev);