7. Login

getty / display manager

Presents the login prompt or desktop

Why initramfs exists — a chicken-and-egg puzzle
Here is a subtle problem the design elegantly solves. To mount your root filesystem, the kernel needs the
right driver — but if your root disk uses LVM or encryption, that driver's config lives ON the root disk you
cannot yet mount. The initramfs breaks the deadlock: it is a small, self-contained filesystem loaded into
RAM alongside the kernel, carrying just enough drivers to reach and unlock the real root. Once the real root
is mounted, initramfs has done its job and is discarded.
systemd-analyze
systemd-analyze critical-chain
systemctl get-default
journalctl -b | head -30