2. A multi-file module: mydriver.ko is linked from main.o, hw.o and sysfs.o. The -objs (or -y) variable lists the parts.
# A Kconfig entry
config MY_DRIVER
tristate "My example device driver"
depends on PCI
default m
help
Support for the example device. Say M to build as a module.

1. config NAME defines an option usable in Makefiles as CONFIG_NAME.
2. tristate allows y/m/n (bool allows only y/n). This is what makes it buildable as a module.
3. depends on expresses requirements — the option is hidden unless PCI is enabled.
4. default m suggests building as a module.