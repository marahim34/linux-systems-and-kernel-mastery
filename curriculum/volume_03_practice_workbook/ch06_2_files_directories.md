2. Files & Directories
2.1 Create a directory structure
Build a nested hierarchy under ~/tmp in one command.
cd
mkdir -p ~/tmp/some/dir1 \
~/tmp/some/dir2/doc1 \
~/tmp/some/dir2/doc2/test/more \
~/tmp/some/dir3/html
ls -R ~/tmp/some

1. cd with no argument goes HOME. mkdir -p creates every missing parent in a path and never errors if something
already exists, so several deep branches are built at once. The backslash at line end continues one command across
lines. ls -R lists recursively to verify the whole tree.

2.2 Move files around
Reorganise files between directories with mv (setup shown first).
mkdir -p ~/tmp/tmp2
mv ~/tmp/dir1 ~/tmp/tmp2/
mv ~/tmp/dir2 ~/tmp/tmp2/
mv ~/tmp/tmp2/dir2/here/1.lst ~/tmp/tmp2/dir1/1.lst
mv ~/tmp/tmp2/dir1/1.txt ~/tmp/tmp2/dir2/1.txt
ls -R ~/tmp/tmp2

1. mv both moves and renames: give it a directory target to move into it, or a full new path to move-and-rename in one
step. Moving a directory carries all its contents. Build such reorganisations one line at a time and re-run ls -R after each
to confirm.

2.3 Reading the cp manual
The four cp options every backup uses (from man cp).
-v, --verbose explain what is being done
-u update: copy only if source is newer
-p preserve mode, ownership, timestamps
-R, -r copy directories recursively

1. -v narrates each copy. -u skips files already up to date, so re-running a big copy is cheap. -p keeps metadata intact,
which matters for backups and deploys. -r (or -R) is required to copy a directory and its contents.

2.4 A full recursive backup
Copy all of ~/tmp into ~/tmp.backup.
cp -r ~/tmp ~/tmp.backup

1. -r walks the whole tree and copies every file and subdirectory. For a backup that also preserves permissions and
timestamps, cp -a (archive) is the stronger choice, as covered in the main volume.

PRACTICE EXERCISES