3. Kernel + initramfs

Kernel starts, uses a mini root
filesystem to load disk/LVM drivers

'Cannot find root device' —
fstab/UUID errors

4. systemd (PID 1)

Mounts real root, starts services in
dependency order

Boot hangs waiting for a failed unit