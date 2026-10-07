2. In WSL: your Windows D: drive, mounted into the Linux tree — where your GoOdo project lives.

Every directory, explained properly
Path

Name origin

What lives there &amp; when you visit

/bin, /usr/bin

binaries

The commands themselves. which ls shows you: /usr/bin/ls

/etc

et cetera

ALL system config as text files: ssh, nginx, fstab, users. Your most-edited directory as
an admin

/home

—

One folder per user. Your personal universe: ~/ = /home/abdur

/root

—

Root's home. NOT the same as / itself

/var

variable

Data that grows: /var/log (logs), /var/lib (databases), /var/www (websites)

/tmp

temporary

Scratch space, world-writable, wiped on reboot

/usr

Unix system
resources

Installed software: binaries, libraries, docs

/opt

optional

Self-contained third-party apps — a good home for /opt/goodo

/dev

devices

Hardware as files: /dev/sda (disk), /dev/null (black hole), /dev/urandom (randomness)

/proc, /sys

process/system

Virtual windows into the kernel: not real files, generated live when read

/boot

—

Kernel images and bootloader — look, don't touch

/srv, /media,
/mnt

—

Served data; auto-mounted USB drives; manual mounts

Absolute vs relative paths — get this into muscle memory





cd /var/log
cd nginx
cd ..
cd ../..
cd ./scripts
cd ~
cd -