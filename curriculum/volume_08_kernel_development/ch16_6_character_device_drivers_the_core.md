6. Character Device Drivers — the Core Skill
Why character devices
The most common kernel programming task is a character device driver — code that presents hardware
(or a virtual service) as a file in /dev that user programs can read and write byte by byte (Volume 4, Chapter
12). Learning to write one teaches the whole driver model: register a device, define file operations, handle
open/read/write/close.

Device numbers
Every device has a major number (which driver handles it) and a minor number (which specific device).
The kernel routes operations on /dev/mything to your driver by its major number.
#include <linux/fs.h>
#include <linux/cdev.h>
#include <linux/uaccess.h>
static dev_t dev_number;
static struct cdev my_cdev;
/* in init: */
alloc_chrdev_region(&dev_number, 0, 1, "mychardev");