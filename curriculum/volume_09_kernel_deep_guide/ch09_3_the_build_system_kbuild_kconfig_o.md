3. The Build System — Kbuild, Kconfig & Out-of-Tree
How the kernel builds
The kernel uses Kbuild, a recursive Make-based system driven by tiny Makefiles that just list objects.
Configuration comes from Kconfig files that generate the .config controlling what is built. Understanding both
lets you add code the kernel's own way, not bolted on.
# A Kbuild Makefile fragment (in-tree)
obj-$(CONFIG_MY_DRIVER) += mydriver.o
mydriver-objs := main.o hw.o sysfs.o

1. obj-$(CONFIG_MY_DRIVER) means 'build this if the config option is set': y = built-in, m = module, n = skip. This is
how every driver is conditionally compiled.