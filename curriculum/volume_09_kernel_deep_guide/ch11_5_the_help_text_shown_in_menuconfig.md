5. The help text shown in menuconfig. This is how your driver becomes a first-class, configurable part of the kernel.

Out-of-tree modules — your development mode
# Out-of-tree Makefile
obj-m := mydriver.o
KDIR := /lib/modules/$(shell uname -r)/build
all:
$(MAKE) -C $(KDIR) M=$(PWD) modules
clean:
$(MAKE) -C $(KDIR) M=$(PWD) clean
install:
$(MAKE) -C $(KDIR) M=$(PWD) modules_install

1. obj-m builds a module outside the kernel tree — your normal development loop.