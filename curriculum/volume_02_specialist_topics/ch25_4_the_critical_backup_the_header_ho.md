4. THE critical backup: the header holds the master key material — a damaged header makes the data unrecoverable
even WITH the passphrase. Store this file off-disk.

Auto-unlock for servers — crypttab





sudo dd if=/dev/urandom of=/root/.diskkey bs=64 count=1
sudo chmod 400 /root/.diskkey
sudo cryptsetup luksAddKey /dev/sdb1 /root/.diskkey
# /etc/crypttab
securedata UUID=<luks-uuid> /root/.diskkey luks
# /etc/fstab
/dev/mapper/securedata /mnt/secure ext4 defaults,nofail 0 2