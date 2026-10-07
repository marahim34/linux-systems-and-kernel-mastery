# Tier 4 · Chapter 3: Character Device Drivers & File Operations

Synthesized from *Linux Mastery* Volume 8 & Robert Love Ch. 13.

## 1. What is a Character Device?
A character device provides a stream of unbuffered, sequential bytes (e.g. serial ports, keyboard, sensors, crypto engines, virtual buffers).
User space accesses them via filesystem nodes in `/dev` (e.g. `/dev/dojo_char`).

## 2. Major and Minor Numbers
- **Major Number**: Identifies the device driver in the kernel.
- **Minor Number**: Identifies the specific physical device instance managed by that driver.

```c
dev_t dev_num;
alloc_chrdev_region(&dev_num, 0, 1, "my_char_device");
int major = MAJOR(dev_num);
int minor = MINOR(dev_num);
```

## 3. The `file_operations` Structure
The bridge between user-space syscalls and kernel driver functions:
```c
static struct file_operations fops = {
    .owner   = THIS_MODULE,
    .open    = device_open,
    .release = device_release,
    .read    = device_read,
    .write   = device_write,
    .unlocked_ioctl = device_ioctl,
};
```

## 4. User-Kernel Data Transfer
```c
// Sending data to user space
copy_to_user(user_buffer, kernel_buffer, count);

// Reading data from user space
copy_from_user(kernel_buffer, user_buffer, count);
```
Returns number of uncopied bytes. 0 means complete success!
