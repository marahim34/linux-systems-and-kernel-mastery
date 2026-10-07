3. The Filesystem — Deep Dive
One tree to rule them all
Windows thinks in drive letters (C:, D:). Linux thinks in one tree rooted at /. A second disk does not get a
letter — it gets mounted onto a directory, becoming part of the same tree. This is why your Windows D: drive
appears at /mnt/d inside WSL: it has been grafted onto the tree.
ls /
ls /mnt/d