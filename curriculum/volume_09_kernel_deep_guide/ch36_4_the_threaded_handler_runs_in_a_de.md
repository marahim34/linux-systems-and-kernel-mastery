4. The threaded handler runs in a dedicated kernel thread, where it CAN sleep — take mutexes, allocate with
GFP_KERNEL, do slow work.
5. request_threaded_irq registers both halves. This split gives you a fast atomic acknowledgement AND a
sleep-capable processing context — the cleanest modern pattern, preferred over manual tasklet/workqueue juggling.





Workqueues for deferred sleeping work
static void my_work_fn(struct work_struct *w)
{
/* process context: may sleep */
}
static DECLARE_WORK(my_work, my_work_fn);
schedule_work(&my_work); /* queue it to run later */