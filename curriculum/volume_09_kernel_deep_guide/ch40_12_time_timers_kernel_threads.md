12. Time, Timers & Kernel Threads
unsigned long start = jiffies;
if (time_after(jiffies, start + msecs_to_jiffies(500))) { }
ktime_t t = ktime_get();
udelay(10); /* busy-wait microseconds (atomic context) */
msleep(20); /* sleep milliseconds (process context) */

1. jiffies is the kernel's tick counter — coarse time. Save a start value...
2. ...and use time_after (not raw comparison, which breaks on wraparound) to check elapsed time.
3. ktime_get gives high-resolution time for precise measurement.
4. udelay busy-waits — the only option in atomic context, but wastes CPU; keep it tiny.
5. msleep actually sleeps — use in process context to yield the CPU while waiting.
static struct task_struct *thread;
thread = kthread_run(thread_fn, data, "my_kthread");
/* the thread function: */
static int thread_fn(void *data)
{
while (!kthread_should_stop()) {
do_work();
msleep(100);
}
return 0;
}
/* to stop: kthread_stop(thread); */

1. kthread_run spawns a kernel thread running thread_fn, named for ps/top visibility.