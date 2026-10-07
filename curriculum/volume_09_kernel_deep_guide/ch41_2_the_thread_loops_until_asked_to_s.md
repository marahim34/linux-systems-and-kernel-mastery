2. The thread loops until asked to stop...
3. ...does its work and sleeps between iterations (it is in process context, so sleeping is fine).
4. kthread_should_stop returns true after someone calls kthread_stop, giving clean shutdown. Kernel threads are how
you run ongoing background work inside the kernel.

PRO INSIGHT: Two time traps to remember: never compare jiffies with plain < or > (use time_after/time_before,
which handle the counter wrapping around to zero), and never use udelay for long waits (it burns a CPU core
spinning). Match the wait to the context: udelay/mdelay for tiny waits in atomic context, msleep/usleep_range for
real waits in process context. Kernel threads (kthread) give you a sleep-capable process context for ongoing work
— the right home for anything that must run continuously in the background.
PRACTICE EXERCISES