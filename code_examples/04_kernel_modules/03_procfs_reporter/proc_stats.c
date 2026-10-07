/*
 * proc_stats.c - Virtual Filesystem Interface via /proc
 * Demonstrates: proc_create, proc_ops, seq_file or basic read/write
 * Inspired by: Robert Love LKD Ch. 12 & Volume 8
 */

#ifdef MOCK_KERNEL
#include "../mock_kernel/linux/module.h"
#include "../mock_kernel/linux/fs.h"
#include "../mock_kernel/linux/uaccess.h"
#else
#include <linux/init.h>
#include <linux/module.h>
#include <linux/proc_fs.h>
#include <linux/uaccess.h>
#endif

#define PROC_ENTRY_NAME "dojo_stats"

MODULE_LICENSE("GPL");
MODULE_AUTHOR("MD Abdur Rahim");
MODULE_DESCRIPTION("Procfs Kernel Metrics Reporter");

static char proc_msg[256];

#ifndef MOCK_KERNEL
static ssize_t proc_read(struct file *file, char __user *buf, size_t count, loff_t *pos) {
    int len = snprintf(proc_msg, sizeof(proc_msg),
                      "Linux Mastery Engine - Kernel Subsystem Status: ONLINE\nActive Students: 1\n");
    if (*pos >= len) return 0;
    if (copy_to_user(buf, proc_msg, len)) return -EFAULT;
    *pos += len;
    return len;
}

static const struct proc_ops proc_fops = {
    .proc_read = proc_read,
};
#endif

static int __init proc_stats_init(void) {
#ifndef MOCK_KERNEL
    proc_create(PROC_ENTRY_NAME, 0444, NULL, &proc_fops);
#endif
    pr_info("[proc_stats] Created /proc/%s entry\n", PROC_ENTRY_NAME);
    return 0;
}

static void __exit proc_stats_exit(void) {
#ifndef MOCK_KERNEL
    remove_proc_entry(PROC_ENTRY_NAME, NULL);
#endif
    pr_info("[proc_stats] Removed /proc/%s entry\n", PROC_ENTRY_NAME);
}

module_init(proc_stats_init);
module_exit(proc_stats_exit);
