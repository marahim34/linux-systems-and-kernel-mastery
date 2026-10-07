5. Advanced: reboot into a specific boot entry (older kernel) — recovery after a bad kernel update.

Rescue modes — your parachutes
# From the GRUB menu (hold Shift/Esc while booting):
# 'Advanced options' -> select older kernel
# Or edit an entry (e key) and append to the linux line:
systemd.unit=rescue.target
systemd.unit=emergency.target
init=/bin/bash