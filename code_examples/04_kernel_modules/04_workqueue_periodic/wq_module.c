/*
 * wq_module.c - Deferred Execution via Linux Kernel Workqueues
 * Demonstrates: struct work_struct, schedule_delayed_work, bottom-half processing
 * Inspired by: Robert Love LKD Ch. 8 (Bottom Halves and Deferring Work)
 */

#ifdef MOCK_KERNEL
#include "../mock_kernel/linux/module.h"
#else
#include <linux/init.h>
#include <linux/module.h>
#include <linux/workqueue.h>
#endif

MODULE_LICENSE("GPL");
MODULE_AUTHOR("MD Abdur Rahim");
MODULE_DESCRIPTION("Asynchronous Workqueue Task Scheduling");

#ifndef MOCK_KERNEL
static struct delayed_work dojo_work;
static int work_ticks = 0;

static void work_handler(struct work_struct *work) {
    work_ticks++;
    pr_info("[dojo_wq] Deferred bottom-half execution tick: %d\n", work_ticks);
    if (work_ticks < 3) {
        schedule_delayed_work(&dojo_work, msecs_to_jiffies(1000));
    }
}
#endif

static int __init wq_module_init(void) {
    pr_info("[dojo_wq] Initializing deferred workqueue...\n");
#ifndef MOCK_KERNEL
    INIT_DELAYED_WORK(&dojo_work, work_handler);
    schedule_delayed_work(&dojo_work, msecs_to_jiffies(1000));
#endif
    return 0;
}

static void __exit wq_module_exit(void) {
#ifndef MOCK_KERNEL
    cancel_delayed_work_sync(&dojo_work);
#endif
    pr_info("[dojo_wq] Workqueue flushed and module unloaded\n");
}

module_init(wq_module_init);
module_exit(wq_module_exit);
