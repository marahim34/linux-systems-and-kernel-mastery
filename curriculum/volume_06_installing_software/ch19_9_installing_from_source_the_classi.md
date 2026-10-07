9. Installing From Source — the Classic Build
When and why
Sometimes software is not packaged anywhere, or you need the very latest version, or you want custom
build options. Then you compile it from its source code. This is more work and you lose automatic updates,
so it is a last resort — but knowing how demystifies a lot of Linux.

The classic three-step dance
sudo apt install build-essential
tar -xzf program-1.4.tar.gz
cd program-1.4
./configure
make
sudo make install