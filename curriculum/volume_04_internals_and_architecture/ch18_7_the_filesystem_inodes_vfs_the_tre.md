7. The Filesystem — Inodes, VFS & the Tree
Explained
The Virtual File System — one interface for all
Linux supports dozens of filesystems (ext4, xfs, btrfs, NTFS, network filesystems, even /proc which is not a
disk at all). Yet you use the same commands — cd, ls, cat — on all of them. This works because of the
Virtual File System (VFS), a kernel layer that presents every filesystem behind one uniform interface. Your
commands talk to VFS; VFS translates to the specific filesystem underneath.
PRO INSIGHT: The VFS is why 'everything is a file' can be true. A real file on ext4, a process in /proc, a device in
/dev, a remote NFS share, a socket — all are presented through the SAME open/read/write/close interface. One set
of tools, one mental model, infinite backends. This uniformity is arguably Linux's single most powerful idea, and the
VFS is the machinery that delivers it.

The inode — a file's true identity
Here is a surprise for most people: a filename is not the file. The real file is an inode — a numbered record
holding all the file's metadata (permissions, owner, size, timestamps, and pointers to the actual data blocks
on disk). The filename is merely a link: an entry in a directory that points to an inode number. This separation
explains many otherwise-baffling behaviours.
ls -i notes.txt
stat notes.txt
df -i