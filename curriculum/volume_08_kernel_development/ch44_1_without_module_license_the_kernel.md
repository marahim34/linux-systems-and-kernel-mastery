1. Without MODULE_LICENSE, the kernel marks itself 'tainted' and hides GPL-only symbols. The dmesg warning is the
kernel telling you it no longer trusts its own integrity for bug reports. Always set the license — this exercise shows why
the warning exists.

Ch.6 — Confirming your major number
cat /proc/devices | grep mychardev
ls -l /dev/mychardev

1. /proc/devices lists registered drivers with their major numbers, proving your cdev registered. The device file's major
(shown by ls -l) must match, confirming the routing from /dev/mychardev to your driver is correct.

Ch.7 — A working write handler
static ssize_t my_write(struct file *f, const char __user *ubuf,
size_t len, loff_t *off)
{
char kbuf[128];
if (len > 127) len = 127;
if (copy_from_user(kbuf, ubuf, len)) return -EFAULT;
kbuf[len] = '\0';
pr_info("user wrote: %s\n", kbuf);
return len; /* report all bytes consumed */
}