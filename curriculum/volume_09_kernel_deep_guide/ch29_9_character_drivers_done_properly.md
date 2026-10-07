9. Character Drivers, Done Properly
Beyond the basics — the professional character driver
Volume 8 built a minimal char device. A production one adds: proper concurrency (multiple openers),
blocking I/O (readers wait for data), poll/select support, and clean integration with the driver model. Here are
the professional additions.

Blocking I/O — making read wait for data
static DECLARE_WAIT_QUEUE_HEAD(read_queue);
static ssize_t my_read(struct file *f, char __user *buf,
size_t len, loff_t *off)
{
if (wait_event_interruptible(read_queue, data_available))
return -ERESTARTSYS; /* interrupted by a signal */
/* ... now data_available is true; copy it out ... */
}
/* when data arrives (e.g. in an interrupt): */
data_available = true;
wake_up_interruptible(&read_queue);