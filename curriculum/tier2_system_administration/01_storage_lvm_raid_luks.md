# Tier 2 · Chapter 1: Storage Subsystems (LVM, RAID, LUKS)

## 1. The Storage Abstraction Stack
```
  [ Filesystem (ext4 / xfs / btrfs) ]
                  ▲
  [ Logical Volume (LV) ]
                  ▲
  [ Volume Group (VG) ]
                  ▲
  [ Physical Volumes (PV: /dev/sda2, /dev/sdb1) ]
                  ▲
  [ Encrypted Layer (LUKS / dm-crypt) ]
                  ▲
  [ Physical Disk or Software RAID (mdadm) ]
```

## 2. LVM Hands-On Commands
```bash
# Initialize Physical Volume
pvcreate /dev/sdb1

# Create Volume Group
vgcreate vg_data /dev/sdb1

# Create Logical Volume (50GB)
lvcreate -L 50G -n lv_app vg_data

# Format with ext4
mkfs.ext4 /dev/vg_data/lv_app

# Grow Logical Volume by 10GB AND resize filesystem live!
lvextend -L +10G -r /dev/vg_data/lv_app
```
