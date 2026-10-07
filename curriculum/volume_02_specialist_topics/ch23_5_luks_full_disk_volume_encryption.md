5. LUKS — Full Disk & Volume Encryption
What LUKS protects against — and what it doesn't
LUKS encrypts data at rest: a stolen laptop, a decommissioned VPS disk, a USB stick lost in an airport. It
does NOT protect a running, unlocked system — while mounted, files are plaintext to any process with
permissions. Remember Volume 1 Ch. 15: init=/bin/bash gives anyone with physical access a root shell —
LUKS is the answer to exactly that.

Encrypting a data disk / USB stick
sudo cryptsetup luksFormat /dev/sdb1
sudo cryptsetup open /dev/sdb1 securedata
sudo mkfs.ext4 /dev/mapper/securedata
sudo mount /dev/mapper/securedata /mnt/secure
# ... work ...
sudo umount /mnt/secure
sudo cryptsetup close securedata