#ifndef _MOCK_LINUX_FS_H
#define _MOCK_LINUX_FS_H

#include "types.h"
#include <errno.h>

struct inode {
    unsigned long i_ino;
    dev_t i_rdev;
};

struct file {
    void *private_data;
    loff_t f_pos;
    unsigned int f_flags;
};

struct file_operations {
    int (*open)(struct inode *, struct file *);
    int (*release)(struct inode *, struct file *);
    ssize_t (*read)(struct file *, char *, size_t, loff_t *);
    ssize_t (*write)(struct file *, const char *, size_t, loff_t *);
    long (*unlocked_ioctl)(struct file *, unsigned int, unsigned long);
};

struct cdev {
    const struct file_operations *ops;
    dev_t dev;
    unsigned int count;
};

static inline void cdev_init(struct cdev *cdev, const struct file_operations *fops) {
    if (cdev) cdev->ops = fops;
}

static inline int cdev_add(struct cdev *cdev, dev_t dev, unsigned int count) {
    if (cdev) { cdev->dev = dev; cdev->count = count; }
    return 0;
}

static inline void cdev_del(struct cdev *cdev) {
    (void)cdev;
}

static inline int register_chrdev_region(dev_t from, unsigned count, const char *name) {
    (void)from; (void)count; (void)name; return 0;
}

static inline int alloc_chrdev_region(dev_t *dev, unsigned baseminor, unsigned count, const char *name) {
    (void)baseminor; (void)count; (void)name;
    *dev = 240 << 20; /* Simulated Major 240 */
    return 0;
}

static inline void unregister_chrdev_region(dev_t from, unsigned count) {
    (void)from; (void)count;
}

#define MAJOR(dev) ((unsigned int)((dev) >> 20))
#define MINOR(dev) ((unsigned int)((dev) & 0xfffff))
#define MKDEV(ma, mi) (((ma) << 20) | (mi))

#endif
