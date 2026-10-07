5. Persist the array definition...
6. ...into the boot image so the array assembles before mounting. Forgetting this = 'my RAID vanished after reboot'.

The failure drill — practice BEFORE it's real





sudo mdadm --fail /dev/md0 /dev/sdb
cat /proc/mdstat
sudo mdadm --remove /dev/md0 /dev/sdb
sudo mdadm --add /dev/md0 /dev/sdd
watch cat /proc/mdstat