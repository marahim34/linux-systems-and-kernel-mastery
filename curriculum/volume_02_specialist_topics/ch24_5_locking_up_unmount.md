5. Locking up: unmount...
6. ...and close. The disk is now ciphertext again — losing this USB stick in Berlin costs you hardware, not data.

Key management — the part people regret skipping
sudo cryptsetup luksAddKey /dev/sdb1
sudo cryptsetup luksRemoveKey /dev/sdb1
sudo cryptsetup luksDump /dev/sdb1 | grep -A2 "Keyslots"
sudo cryptsetup luksHeaderBackup /dev/sdb1 --header-backup-file sdb1.header