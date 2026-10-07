3. Your First Kernel Module — Hello, Kernel
The smallest possible module
/* hello.c */
#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/init.h>
static int __init hello_init(void)
{
printk(KERN_INFO "Hello, kernel! Module loaded.\n");
return 0;
}
static void __exit hello_exit(void)
{
printk(KERN_INFO "Goodbye, kernel! Module unloaded.\n");
}
module_init(hello_init);
module_exit(hello_exit);
MODULE_LICENSE("GPL");
MODULE_AUTHOR("MD Abdur Rahim");
MODULE_DESCRIPTION("A first hello-world module");