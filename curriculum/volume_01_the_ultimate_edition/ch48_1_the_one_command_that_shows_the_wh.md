1. The one command that shows the whole chain: devices, partitions, filesystem types, labels, UUIDs, and mount points
in a tree.
OUTPUT

NAME FSTYPE LABEL UUID MOUNTPOINT
sda
■■sda1 ext4 1f2e3d4c-... /
■■sda2 swap 9a8b7c6d-... [SWAP]
sdb
■■sdb1 ext4 data 5e6f7a8b-... /mnt/data

Adding a new disk — the full ritual
sudo fdisk /dev/sdb
# inside fdisk: n (new), p (primary), Enter x3, w (write)
sudo mkfs.ext4 -L data /dev/sdb1
sudo mkdir /mnt/data
sudo mount /dev/sdb1 /mnt/data
df -h /mnt/data