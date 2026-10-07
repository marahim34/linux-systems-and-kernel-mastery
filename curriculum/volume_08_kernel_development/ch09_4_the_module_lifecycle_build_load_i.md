4. The Module Lifecycle — Build, Load, Inspect,
Unload
The full cycle
make
sudo insmod hello.ko
sudo dmesg | tail -3
lsmod | grep hello
modinfo hello.ko
sudo rmmod hello
sudo dmesg | tail -1