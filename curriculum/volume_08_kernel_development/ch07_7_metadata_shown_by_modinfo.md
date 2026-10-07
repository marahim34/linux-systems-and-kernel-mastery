7. Metadata shown by modinfo.

PRO INSIGHT: Every module has exactly two hooks: an init function (called on load) and an exit function (called on
unload). That is the entire skeleton. Everything else — drivers, filesystems, features — is built by making these two
functions register and unregister the module's real work with the appropriate kernel subsystem. Master this shape
and every module makes structural sense.

The Makefile





# Makefile
obj-m += hello.o
all:
make -C /lib/modules/$(shell uname -r)/build M=$(PWD) modules
clean:
make -C /lib/modules/$(shell uname -r)/build M=$(PWD) clean

1. obj-m += hello.o tells the kernel build system to build hello.c into a module (hello.ko).