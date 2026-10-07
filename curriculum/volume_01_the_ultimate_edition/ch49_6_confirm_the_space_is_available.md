6. Confirm the space is available.

fstab — done correctly
sudo blkid /dev/sdb1
# /etc/fstab
UUID=5e6f7a8b-... /mnt/data ext4 defaults,nofail 0 2
sudo mount -a && findmnt /mnt/data