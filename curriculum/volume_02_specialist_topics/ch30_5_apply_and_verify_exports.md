5. Apply and verify exports.
# client:
sudo apt install nfs-common
sudo mount -t nfs 10.8.0.1:/srv/nfs/shared /mnt/shared
# fstab:
10.8.0.1:/srv/nfs/shared /mnt/shared nfs defaults,nofail,_netdev 0 0