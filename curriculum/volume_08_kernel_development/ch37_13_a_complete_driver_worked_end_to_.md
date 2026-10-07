13. A Complete Driver — Worked End to End
Here is a full, working character device driver that stores a message you can write to it and read back — a
'virtual notepad' device. It combines every concept: module lifecycle, character device registration, file
operations, safe user-space copying, and cleanup. Study it as the integration of the whole volume.

The complete source — part 1: state and file operations
#include <linux/module.h>
#include <linux/fs.h>
#include <linux/cdev.h>
#include <linux/uaccess.h>
#include <linux/slab.h>
#define DEVICE_NAME "notepad"
#define BUF_SIZE 1024
static dev_t dev_number;
static struct cdev my_cdev;
static struct class *dev_class;
static char *buffer;
static size_t data_len;
static int np_open(struct inode *i, struct file *f)
{
pr_info("notepad: opened\n");
return 0;
}
static ssize_t np_read(struct file *f, char __user *ubuf,
size_t len, loff_t *off)
{
if (*off >= data_len) return 0;
if (len > data_len - *off) len = data_len - *off;
if (copy_to_user(ubuf, buffer + *off, len)) return -EFAULT;
*off += len;
return len;
}
static ssize_t np_write(struct file *f, const char __user *ubuf,
size_t len, loff_t *off)
{
if (len > BUF_SIZE) len = BUF_SIZE;
if (copy_from_user(buffer, ubuf, len)) return -EFAULT;
data_len = len;
return len;
}