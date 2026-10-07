12. The Kernel Source, Coding Style & Contributing
Getting and navigating the source
git clone --depth 1 https://github.com/torvalds/linux.git
cd linux
ls
make menuconfig
scripts/get_maintainer.pl -f drivers/char/mem.c