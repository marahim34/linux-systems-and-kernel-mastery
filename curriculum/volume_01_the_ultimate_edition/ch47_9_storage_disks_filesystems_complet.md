9. Storage, Disks & Filesystems — Complete
From metal to files — the storage stack
The chain: physical disk (/dev/sda) → partitions (/dev/sda1) → optionally LVM volumes → a filesystem
(ext4/xfs) written onto them → mounted into the tree. Understanding this chain lets you debug any storage
problem by asking 'which layer is broken?'
lsblk -f