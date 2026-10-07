2. Grow the root volume by 10 GB AND (-r) resize the filesystem inside, live, no reboot. This is how you use that extra
disk space your VPS provider just granted.

Filesystem health
sudo smartctl -H /dev/sda
sudo fsck -n /dev/sdb1
sudo tune2fs -l /dev/sda1 | grep -i "mount count"