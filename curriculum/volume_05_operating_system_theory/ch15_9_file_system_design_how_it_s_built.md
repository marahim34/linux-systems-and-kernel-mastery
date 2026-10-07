9. File System Design — How It's Built Underneath
Volume 4 covered inodes and the VFS from the user's side. Here is how a filesystem is actually DESIGNED
— how it tracks which disk blocks belong to which file, the core of the file-systems course.

How a file's blocks are tracked
Method

Idea

Weakness

Contiguous

Store each file in consecutive blocks

Fast reads / fragmentation, hard to
grow files

Linked list

Each block points to the next

No fragmentation / slow random
access, pointers waste space

FAT

Linked list moved into one table in
memory

Better random access / table grows
with disk

Inodes (indexed)

Each file has an index block listing its
blocks

Fast, scalable / the Unix/Linux choice

The inode's clever multi-level index
An inode stores the first several block addresses directly (fast access to small files). For larger files, it points
to single, double, and triple indirect blocks — index blocks that point to more index blocks. This design
gives instant access to small files while still supporting enormous ones, all from a fixed-size inode. It is a
beautiful piece of engineering worth understanding once.
Pointer type

Reaches

Good for

Direct (x12)

The first ~48 KB directly

Small files (the majority)

Single indirect

One index block of pointers

Medium files

Double indirect

Index of indexes

Large files

Triple indirect

Index of indexes of indexes

Huge files

PRO INSIGHT: Why this design won: most files are small, and the direct pointers make them instant. But the same
structure scales to terabyte files through indirection, WITHOUT wasting space on small files or imposing a size limit.
It optimises the common case while gracefully handling the rare one — a hallmark of great systems design, and the
reason the inode has survived fifty years.

Free space and consistency
The filesystem also tracks which blocks are FREE (usually with a bitmap: one bit per block, set if used). And
it must stay CONSISTENT across crashes — the job of the journal from Volume 4, which logs intended
changes before making them so a power cut cannot leave the structure half-updated.
PRACTICE EXERCISES