17. Security, Hardening & Common Vulnerabilities
The bug classes that become CVEs
Vulnerability

Cause

Defence

Missing user-copy check

Trusting a user pointer/length

copy_to/from_user, validate lengths

Integer overflow

size arithmetic wraps

check_add_overflow, kmalloc_array

Use-after-free

Freeing while still referenced

Refcounts (kref), RCU, careful
ownership

Race condition (TOCTOU)

Check then use without locking

Lock across the whole operation

Info leak

Copying uninitialised kernel memory
to user

Zero buffers (kzalloc), copy exact
sizes

Missing capability check

Not verifying privilege

capable(CAP_SYS_ADMIN) where
needed

if (copy_from_user(&req, arg, sizeof(req))) return -EFAULT;
if (req.count > MAX_ALLOWED) return -EINVAL; /* validate! */
buf = kmalloc_array(req.count, sizeof(*buf), GFP_KERNEL);
if (!buf) return -ENOMEM;
if (!capable(CAP_SYS_ADMIN)) return -EPERM; /* privilege check */