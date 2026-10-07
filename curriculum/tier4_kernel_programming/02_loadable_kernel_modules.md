# Tier 4 · Chapter 2: Writing Loadable Kernel Modules (LKMs)

Synthesized from *Linux Mastery Complete Library* Volume 8 & Robert Love Ch. 17.

## 1. Anatomy of an LKM
```c
#include <linux/init.h>
#include <linux/module.h>
#include <linux/kernel.h>

MODULE_LICENSE("GPL");
MODULE_AUTHOR("MD Abdur Rahim");
MODULE_DESCRIPTION("Mastery Kernel Module");
MODULE_VERSION("1.0");

static int __init my_module_init(void) {
    pr_info("Module loaded successfully into kernel memory!
");
    return 0; // Return 0 for success
}

static void __exit my_module_exit(void) {
    pr_info("Module unloaded from kernel memory.
");
}

module_init(my_module_init);
module_exit(my_module_exit);
```

## 2. Compiling Against Linux Headers
In kernel development, modules are compiled using the kernel's **Kbuild** system:
```makefile
obj-m += my_module.o

KDIR ?= /lib/modules/$(shell uname -r)/build
PWD := $(shell pwd)

default:
	$(MAKE) -C $(KDIR) M=$(PWD) modules

clean:
	$(MAKE) -C $(KDIR) M=$(PWD) clean
```

## 3. Module Commands
```bash
sudo insmod my_module.ko    # Load module
lsmod | grep my_module      # Check loaded status
dmesg | tail -n 10          # Read kernel ring buffer
sudo rmmod my_module        # Unload module
modinfo my_module.ko        # Inspect metadata
```
