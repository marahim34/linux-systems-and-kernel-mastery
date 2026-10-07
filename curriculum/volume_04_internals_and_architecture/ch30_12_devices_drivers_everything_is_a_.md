12. Devices & Drivers — 'Everything Is a File'
Explained
Hardware as files
You have heard 'everything is a file' throughout these volumes. Chapter 12 shows the machinery. In /dev,
physical and virtual devices appear as special files. Reading or writing these files sends data to or from the
actual hardware, through its driver. This means the same read/write tools work on a disk, a serial port, or a
random-number generator.
Device file

What it is

Try it (carefully)

/dev/sda

First whole disk

sudo fdisk -l /dev/sda (inspect only)

/dev/null

The black hole — discards all input

command > /dev/null (silence output)

/dev/zero

Infinite stream of zero bytes

used to create blank files

/dev/urandom

Endless cryptographic randomness

head -c 16 /dev/urandom | base64 (a
random string)

/dev/tty

Your current terminal

echo hi > /dev/tty

/dev/loop0

A file pretending to be a disk

how disk images are mounted

Type

Character (c)

Block (b)

Data flow

One byte at a time, like a stream

In fixed-size blocks, randomly
addressable

Examples

keyboards, serial ports, /dev/random

disks, SSDs, USB drives

Seen in ls -l

first letter c

first letter b

Two kinds of device

ls -l /dev/sda /dev/null /dev/tty
head -c 20 /dev/urandom | base64
dd if=/dev/zero of=blank.img bs=1M count=10