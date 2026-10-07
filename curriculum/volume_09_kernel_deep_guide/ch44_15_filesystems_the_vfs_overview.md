15. Filesystems & the VFS (Overview)
A filesystem plugs into the Virtual File System (Volume 4) by implementing a set of operations the VFS
calls. You provide the behaviour behind open, read, lookup, and so on for your storage format.
VFS object

You implement

Represents

super_block

fill_super, statfs

A mounted filesystem instance

inode

inode_operations (lookup, create)

A file or directory's metadata

dentry

d_ops (rare)

A name-to-inode cache entry

file

file_operations (read, write, mmap)

An open file

address_space

readpage, writepage

A file's page cache mapping

Writing a full on-disk filesystem is a large undertaking, but simple in-memory or virtual filesystems (like a
custom /proc-style interface) are approachable and teach the VFS contract. Many drivers expose information
through a small virtual filesystem rather than a char device.
PRO INSIGHT: The VFS is a set of interfaces you implement, not inherit — pure C polymorphism through operation
tables (super_operations, inode_operations, file_operations). This is the same function-pointer-table pattern as char
drivers, scaled up: fill in the operations for your filesystem and the VFS drives them. Understanding that ALL of
Linux I/O — files, sockets, devices, procfs — flows through these operation tables is the unifying insight of kernel
I/O, and the reason 'everything is a file' holds all the way down.