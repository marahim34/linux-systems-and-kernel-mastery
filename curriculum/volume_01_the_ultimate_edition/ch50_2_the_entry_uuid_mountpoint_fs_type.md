2. The entry: UUID, mountpoint, fs type, options (nofail = a missing disk won't block boot), dump=0, fsck order=2 (root is
1).
3. mount -a applies fstab now AND validates syntax; findmnt confirms. Test BEFORE reboot — a bad fstab drops the
server into emergency mode.





Swap — the safety net
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
sudo sysctl vm.swappiness=10