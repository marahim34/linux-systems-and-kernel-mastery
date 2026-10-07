7. Advance the offset so the next read continues, and return how many bytes we gave.

PRO INSIGHT: copy_to_user and copy_from_user are not optional politeness — they are security-critical. They
validate that the user pointer really belongs to the calling process and handle the address-space translation.
Dereferencing a raw user pointer directly is a classic, dangerous kernel bug that can crash the system or leak
kernel memory to an attacker. Every byte crossing the user/kernel boundary goes through these functions. No
exceptions.

ioctl — commands beyond read and write
Sometimes a device needs COMMANDS, not just data streams — 'eject', 'set speed', 'get status'. The ioctl
(input/output control) operation handles these: user space sends a command number and optional argument,
and the driver acts on it. It is the escape hatch for device-specific control.





static long my_ioctl(struct file *f, unsigned int cmd,
unsigned long arg)
{
switch (cmd) {
case MY_RESET: do_reset(); break;
case MY_GET_VER: return VERSION;
default: return -ENOTTY; /* unknown command */
}
return 0;
}

1. ioctl receives a command number and an argument.