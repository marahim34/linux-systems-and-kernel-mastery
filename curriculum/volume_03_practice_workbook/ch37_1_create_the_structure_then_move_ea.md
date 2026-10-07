1. Create the structure, then move each file into the other directory. ls -R confirms the swap. Do one mv at a time and
re-list to stay oriented.

2b. An extra cp option
cp --backup=numbered file dest/

1. --backup keeps a numbered copy (file.~1~) instead of silently overwriting an existing destination. Useful when you
want to overwrite but keep the old version just in case.

2c. Compare cp -r and cp -a on timestamps
cp -r ~/tmp ~/tmp.r
cp -a ~/tmp ~/tmp.a
ls -l ~/tmp ~/tmp.r ~/tmp.a

1. cp -r may reset modification times to now; cp -a preserves the originals along with permissions and ownership.
Compare the ls -l times to see the difference.

Section 3 — File Globbing
3a. Create test files and predict results
touch A1.txt b2.log C3.JPG d4d.md 'weird name.txt'
ls [A-Z]* # A1.txt C3.JPG
ls *[0-9]*.log # b2.log
ls *.??? # A1.txt b2.log d4d.md (3-char ext)
ls *.[jJ][pP][gG] # C3.JPG