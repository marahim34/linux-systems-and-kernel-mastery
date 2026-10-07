7. Talking to User Space — copy_to_user & ioctl
The memory barrier you must respect
User-space and kernel-space memory are separate and protected (Volume 4). A driver CANNOT simply
dereference a pointer that came from a user program — that pointer belongs to a different address space
and may be invalid or malicious. The kernel provides copy_to_user and copy_from_user to move data
safely across the boundary, with validation.
static ssize_t my_read(struct file *f, char __user *buf,
size_t len, loff_t *off)
{
char msg[] = "Hello from the kernel\n";
size_t msglen = sizeof(msg);
if (*off >= msglen) return 0; /* EOF */
if (len > msglen - *off) len = msglen - *off;
if (copy_to_user(buf, msg + *off, len))
return -EFAULT;
*off += len;
return len;
}

1. read receives a __user pointer (buf) — the annotation marks it as untrusted user memory.