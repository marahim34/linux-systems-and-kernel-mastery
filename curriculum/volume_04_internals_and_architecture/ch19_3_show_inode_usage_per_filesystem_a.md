3. Show inode USAGE per filesystem. A disk can run out of inodes (too many tiny files) even with free space left — a
classic puzzling failure this explains.

Why the inode model explains everything
Puzzle

Explanation via inodes

Hard links

Two names pointing to the SAME inode — same file, two
labels

Deleting a file

You remove a NAME (link). The inode and data survive
until the LAST name is gone

A deleted file still using space

A process still holds the inode open; the name is gone but
the inode is not freed yet (Volume 1's lsof +L1 mystery)

Renaming is instant

Only the directory entry changes; the inode and gigabytes
of data never move

Permissions belong to the file, not the name

Because they live in the inode, shared by all its links





PRO INSIGHT: Unique point: because names and data are separate, moving a 100 GB file within one filesystem is
INSTANT — only the directory entry changes, the inode stays put. Across filesystems it is slow, because the data
must actually be copied to a new inode. This is why mv is sometimes instant and sometimes not — and now you
know precisely why.

Journaling — surviving a power cut
Modern filesystems like ext4 keep a journal: before making a change, they write their intention to a log. If
power fails mid-write, the journal lets the system finish or undo the half-done operation on reboot, preventing
corruption. This is why a Linux server survives an unclean shutdown far better than older systems that could
be left in a broken state.