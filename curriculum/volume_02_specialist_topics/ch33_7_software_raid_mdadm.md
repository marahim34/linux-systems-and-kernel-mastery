7. Software RAID — mdadm
What RAID is and is NOT
RAID keeps a server RUNNING through a disk failure (availability). It is not a backup: deletion, ransomware,
and filesystem corruption replicate to all disks instantly. RAID + backups, never RAID instead of backups.
Level

Disks

Capacity

Survives

Use

RAID 0

2+

100%

NOTHING — any
disk dies, all data
dies

scratch speed only

RAID 1

2

50%

1 disk failure

the sane default for
small servers

RAID 5

3+

n-1 disks

1 failure

capacity-efficient;
slow rebuilds on big
disks

RAID 10

4+

50%

1 per mirror pair

databases: fast +
redundant

Building a RAID 1 mirror
sudo apt install mdadm
sudo mdadm --create /dev/md0 --level=1 --raid-devices=2 /dev/sdb /dev/sdc
cat /proc/mdstat
sudo mkfs.ext4 /dev/md0 && sudo mount /dev/md0 /mnt/raid
sudo mdadm --detail --scan | sudo tee -a /etc/mdadm/mdadm.conf
sudo update-initramfs -u