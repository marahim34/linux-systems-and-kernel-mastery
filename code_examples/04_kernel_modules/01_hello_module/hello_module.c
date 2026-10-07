/*
 * hello_module.c - Fundamental Linux Kernel Module (LKM)
 * Demonstrates: module_init, module_exit, printk / pr_info, module parameters
 * Inspired by: Robert Love "Linux Kernel Development" Ch. 17 & Volume 8
 */

#ifdef MOCK_KERNEL
#include "../mock_kernel/linux/module.h"
#else
#include <linux/init.h>
#include <linux/module.h>
#include <linux/kernel.h>
#endif

MODULE_LICENSE("GPL");
MODULE_AUTHOR("MD Abdur Rahim <marahim34@github>");
MODULE_DESCRIPTION("Introduction to Linux Kernel Modules - Mastery Dojo");
MODULE_VERSION("1.0.0");

static char *whom = "Linux Master";
module_param(whom, charp, 0644);
MODULE_PARM_DESC(whom, "Recipient of the greeting message");

static int howmany = 1;
module_param(howmany, int, 0644);
MODULE_PARM_DESC(howmany, "Number of times to print greeting");

static int __init hello_dojo_init(void) {
    pr_info("========================================\n");
    pr_info("[dojo_hello] Kernel module loaded successfully!\n");
    for (int i = 0; i < howmany; i++) {
        pr_info("[dojo_hello] (%d/%d) Welcome to Linux Kernel Mastery, %s!\n", i + 1, howmany, whom);
    }
    pr_info("========================================\n");
    return 0;
}

static void __exit hello_dojo_exit(void) {
    pr_info("[dojo_hello] Unloading module. Goodbye from kernel space!\n");
}

module_init(hello_dojo_init);
module_exit(hello_dojo_exit);
