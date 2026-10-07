8. The Device Model — kobjects, sysfs, buses & the
driver core
The unifying abstraction
Beneath every driver is the driver model: a hierarchy of kobjects that produces /sys, models buses, devices
and drivers, and handles the matching of drivers to hardware. Understanding it explains how a driver gets
bound to a device, where /sys entries come from, and how hotplug works.
Object

Represents

Appears in

kobject

The base 'thing' with a refcount and
sysfs node

/sys everywhere

bus_type

A kind of bus (PCI, USB, platform,
I2C)

/sys/bus/

device

A physical or virtual device

/sys/devices/

device_driver

A driver that can handle devices

/sys/bus/*/drivers/

class

A functional grouping (net, block, tty)

/sys/class/

How binding works — probe and remove
A bus MATCHES devices to drivers (by ID tables). When a match occurs, the driver's probe() is called to
initialise that device; on removal or unbind, remove() tears it down. This is the driver lifecycle for every
modern bus.
static const struct of_device_id my_ids[] = {
{ .compatible = "vendor,mydevice" },
{ }
};
MODULE_DEVICE_TABLE(of, my_ids);
static struct platform_driver my_driver = {
.probe = my_probe,
.remove = my_remove,
.driver = {
.name = "mydevice",
.of_match_table = my_ids,
},
};
module_platform_driver(my_driver);