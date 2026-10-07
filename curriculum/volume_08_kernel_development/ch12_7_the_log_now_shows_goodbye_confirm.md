7. The log now shows 'Goodbye' — confirming clean unload. This build-load-check-unload cycle is your entire
development loop.

PRO INSIGHT: insmod versus modprobe: insmod loads exactly the file you name and fails if it needs other
modules. modprobe is smarter — it looks up modules by name in the system directory and loads DEPENDENCIES
automatically. During development you use insmod (direct, local file); for installed modules the system uses
modprobe. Knowing which to reach for saves confusion when a module 'won't load'.

When a module will not load
Symptom

Usual cause

Fix

'Invalid module format'

Built against a different kernel
version

Rebuild with current linux-headers

'Operation not permitted'

Secure Boot rejects unsigned
modules

Disable Secure Boot in the VM, or
sign the module

'Unknown symbol'

Using a function not exported to
modules

Use an EXPORT_SYMBOL'd API, or
the right header

Module taints kernel

Missing or non-GPL
MODULE_LICENSE

Set MODULE_LICENSE("GPL")

PRACTICE EXERCISES