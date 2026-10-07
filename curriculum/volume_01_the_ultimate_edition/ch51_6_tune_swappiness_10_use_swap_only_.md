6. Tune: swappiness 10 = 'use swap only under real pressure' — right for servers (default 60 is desktop-tuned). Persist
in /etc/sysctl.d/.

PRO INSIGHT: Small-VPS survival: 2 GB RAM + no swap means one traffic spike triggers the OOM-killer and your
backend 'mysteriously' dies at 3 AM. Swap converts a crash into mere slowness. Always add it.

LVM in one page — why clouds love it
LVM inserts a flexible layer: physical volumes (PV) pool into a volume group (VG), from which logical
volumes (LV) are carved. The payoff: resize live, add disks to the pool, snapshot before risky changes.
sudo lvs
sudo lvextend -r -L +10G /dev/ubuntu-vg/root