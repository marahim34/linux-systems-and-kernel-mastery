3. The cdev structure represents your character device to the kernel.
4. alloc_chrdev_region asks the kernel to ALLOCATE a free major number for one device named 'mychardev' — the
modern way (versus hardcoding a major).

The file_operations structure — the heart of a driver
A driver defines what happens when user space opens, reads, writes, or closes its device. These are wired
up through a file_operations structure: a table of function pointers the kernel calls for each operation.





static struct file_operations fops = {
.owner = THIS_MODULE,
.open = my_open,
.read = my_read,
.write = my_write,
.release = my_release,
};
/* in init, after cdev_init(&my_cdev, &fops): */
cdev_add(&my_cdev, dev_number, 1);