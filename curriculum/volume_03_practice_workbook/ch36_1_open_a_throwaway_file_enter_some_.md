1. Open a throwaway file, enter some lines, press Esc to be sure you are in Normal mode, then try each verb. yy copies
the current line and p pastes it after the cursor.

1c. Toggle line numbers
:set number
:set relativenumber
:set nonumber

1. :set number shows absolute numbers, relativenumber shows distance from the cursor (handy with counts like 5j), and
nonumber turns them off.

Section 2 — Files & Directories
2a. Build the tree, swap two files





mkdir -p ~/tmp/some/dir1 ~/tmp/some/dir2
touch ~/tmp/some/dir1/a.txt ~/tmp/some/dir2/b.txt
mv ~/tmp/some/dir1/a.txt ~/tmp/some/dir2/a.txt
mv ~/tmp/some/dir2/b.txt ~/tmp/some/dir1/b.txt
ls -R ~/tmp/some