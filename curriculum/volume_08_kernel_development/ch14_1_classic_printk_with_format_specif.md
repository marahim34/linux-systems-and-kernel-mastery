1. Classic printk with format specifiers — %d int, %p pointer, %s string, much like printf.
2. pr_info, pr_err, pr_debug are modern shorthands preferred in new code.
3. dmesg -w FOLLOWS the kernel log live — keep this open in one terminal while developing to see your messages
instantly.

Module parameters — passing values at load time
static int count = 1;
static char *name = "world";
module_param(count, int, 0644);
MODULE_PARM_DESC(count, "how many times to greet");
module_param(name, charp, 0644);
MODULE_PARM_DESC(name, "who to greet");
/* load with values: */
/* sudo insmod hello.ko count=3 name="Abdur" */