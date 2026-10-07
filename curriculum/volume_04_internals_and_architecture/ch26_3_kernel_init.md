3. Kernel init

The Linux kernel

Initialises itself, detects CPU and memory, mounts a temporary root

4. initramfs

A tiny in-RAM filesystem

Loads the drivers needed to reach the REAL root disk (e.g. LVM,
encryption)