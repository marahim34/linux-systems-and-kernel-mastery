/*
 * char_dev.c - Complete Linux Character Device Driver with Circular Buffer
 * Demonstrates: alloc_chrdev_region, cdev, file_operations, copy_to_user,
 *               copy_from_user, mutex concurrency protection
 * Inspired by: Robert Love LKD Ch. 13 & Volume 8 Ch. 6
 */

#ifdef MOCK_KERNEL
#include "../mock_kernel/linux/module.h"
#include "../mock_kernel/linux/fs.h"
#include "../mock_kernel/linux/uaccess.h"
#include "../mock_kernel/linux/slab.h"
#include "../mock_kernel/linux/mutex.h"
#else
#include <linux/init.h>
#include <linux/module.h>
#include <linux/fs.h>
#include <linux/cdev.h>
#include <linux/uaccess.h>
#include <linux/slab.h>
#include <linux/mutex.h>
#endif

#define DEVICE_NAME "dojo_char"
#define BUFFER_SIZE 1024

MODULE_LICENSE("GPL");
MODULE_AUTHOR("MD Abdur Rahim");
MODULE_DESCRIPTION("Circular Buffer Character Device Driver");

static dev_t dev_num;
static struct cdev dojo_cdev;
static char device_buffer[BUFFER_SIZE];
static size_t data_len = 0;
static DEFINE_MUTEX(dev_mutex);

static int dojo_open(struct inode *inodep, struct file *filep) {
    (void)inodep; (void)filep;
    pr_info("[dojo_char] Device opened\n");
    return 0;
}

static int dojo_release(struct inode *inodep, struct file *filep) {
    (void)inodep; (void)filep;
    pr_info("[dojo_char] Device released\n");
    return 0;
}

static ssize_t dojo_read(struct file *filep, char __user *user_buf, size_t count, loff_t *offset) {
    (void)filep;
    ssize_t bytes_to_read;
    unsigned long not_copied;

    mutex_lock(&dev_mutex);

    if (*offset >= (loff_t)data_len) {
        mutex_unlock(&dev_mutex);
        return 0; /* EOF */
    }

    bytes_to_read = data_len - *offset;
    if (bytes_to_read > (ssize_t)count) {
        bytes_to_read = count;
    }

    not_copied = copy_to_user(user_buf, device_buffer + *offset, bytes_to_read);
    if (not_copied != 0) {
        mutex_unlock(&dev_mutex);
        return -EFAULT;
    }

    *offset += bytes_to_read;
    pr_info("[dojo_char] Read %zd bytes, new offset %lld\n", bytes_to_read, (long long)*offset);

    mutex_unlock(&dev_mutex);
    return bytes_to_read;
}

static ssize_t dojo_write(struct file *filep, const char __user *user_buf, size_t count, loff_t *offset) {
    (void)filep; (void)offset;
    ssize_t bytes_to_write = count;
    unsigned long not_copied;

    mutex_lock(&dev_mutex);

    if (bytes_to_write > BUFFER_SIZE - 1) {
        bytes_to_write = BUFFER_SIZE - 1;
    }

    not_copied = copy_from_user(device_buffer, user_buf, bytes_to_write);
    if (not_copied != 0) {
        mutex_unlock(&dev_mutex);
        return -EFAULT;
    }

    device_buffer[bytes_to_write] = '\0';
    data_len = bytes_to_write;
    pr_info("[dojo_char] Wrote %zd bytes to buffer: \"%s\"\n", bytes_to_write, device_buffer);

    mutex_unlock(&dev_mutex);
    return bytes_to_write;
}

struct file_operations dojo_fops = {
    .open = dojo_open,
    .release = dojo_release,
    .read = dojo_read,
    .write = dojo_write,
};

static int __init dojo_char_init(void) {
    int ret;
    ret = alloc_chrdev_region(&dev_num, 0, 1, DEVICE_NAME);
    if (ret < 0) {
        pr_err("[dojo_char] Failed to allocate major number\n");
        return ret;
    }

    cdev_init(&dojo_cdev, &dojo_fops);
    ret = cdev_add(&dojo_cdev, dev_num, 1);
    if (ret < 0) {
        unregister_chrdev_region(dev_num, 1);
        pr_err("[dojo_char] Failed to add cdev\n");
        return ret;
    }

    pr_info("[dojo_char] Registered driver with Major: %d, Minor: %d\n",
            MAJOR(dev_num), MINOR(dev_num));
    return 0;
}

static void __exit dojo_char_exit(void) {
    cdev_del(&dojo_cdev);
    unregister_chrdev_region(dev_num, 1);
    pr_info("[dojo_char] Character driver unloaded\n");
}

module_init(dojo_char_init);
module_exit(dojo_char_exit);
