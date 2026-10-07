4. When data arrives, set the condition and wake_up the sleepers. The woken reader re-checks the condition and
proceeds. This is the correct blocking-I/O pattern.

poll/select support
static __poll_t my_poll(struct file *f, poll_table *wait)
{
__poll_t mask = 0;
poll_wait(f, &read_queue, wait);
if (data_available) mask |= EPOLLIN | EPOLLRDNORM;
return mask;
}

1. poll lets userspace use select/poll/epoll on your device — essential for event loops.
2. poll_wait registers your wait queue with the poll infrastructure (does not sleep here).