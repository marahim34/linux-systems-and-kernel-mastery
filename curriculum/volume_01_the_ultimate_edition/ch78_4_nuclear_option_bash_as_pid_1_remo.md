4. Nuclear option: bash as PID 1. Remount root writable with: mount -o remount,rw / — then repair passwd/fstab, and
reboot.

The kernel at runtime — modules and sysctl





uname -r
lsmod | head
sudo modprobe br_netfilter
lsmod | grep br_netfilter
sysctl net.ipv4.ip_forward
sudo sysctl -w net.ipv4.ip_forward=1
echo 'net.ipv4.ip_forward=1' | sudo tee /etc/sysctl.d/99-forward.conf