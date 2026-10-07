3. DEVICE_ATTR_RO declares a read-only attribute named 'speed' (there are RW and WO variants).
4. device_create_file makes /sys/.../speed appear. Now userspace can cat it — this is how drivers expose status and
tunables, the /sys philosophy from Volume 4 made by your hand.

PRO INSIGHT: The driver model is the scaffold that makes 'plug in hardware, the right driver loads and initialises it'
work. Your job as a driver author is mostly to fill in probe (set up this device) and remove (tear it down), declare
which hardware you match, and expose attributes through sysfs. The core handles matching, refcounting, hotplug,
and power management. Learning to work WITH the model — rather than registering char devices by hand as in
Volume 8 — is the leap to writing real, upstreamable drivers.