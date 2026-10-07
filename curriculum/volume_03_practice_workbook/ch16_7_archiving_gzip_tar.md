7. Archiving — gzip & tar
7.1 Maximum compression
Compress file.txt as hard as gzip can.
gzip -9 file.txt

1. gzip replaces file.txt with file.txt.gz. -9 selects the strongest (slowest) compression level; -1 is fastest and weakest.
Note gzip works on a single file and removes the original by default.

7.2 Decompress
Restore file.txt from its .gz.
gzip -d file.txt.gz

1. -d decompresses, recreating file.txt and removing the .gz. gunzip file.txt.gz does exactly the same thing.

7.3 Create a tar.gz with relative paths
Archive ~/tmp so entries read tmp/... not /home/you/tmp/...
tar -C "$HOME" -czf "$HOME/package.tar.gz" tmp

1. -C changes into $HOME first, so the archived path is the relative tmp. -c create, -z gzip, -f names the output file.
Relative paths make archives safe to extract anywhere without overwriting absolute locations.

7.4 List an archive's contents
See what is inside without extracting.
tar -tzf "$HOME/package.tar.gz"

1. -t lists the table of contents, -z for gzip, -f the file. Always inspect an archive with -t before extracting so you know
what and where it will write.

7.5 Extract into a directory
Unpack the archive under /tmp.
tar -xzf ~/package.tar.gz -C /tmp

1. -x extract, -z gzip, -f file, and -C /tmp extracts INTO /tmp. Without -C it would extract into the current directory.

7.6 Use bzip2 compression
Create a .tar.bz2 instead of gzip.
tar -cjf ~/package.tar.bz2 -C ~ tmp

1. -j selects bzip2 instead of gzip (-z). bzip2 usually compresses a little smaller but slower. The rest of the flags mirror
7.3.





7.7 Extract a single file
Pull just one file out of a bz2 archive.
tar -xjf ~/package.tar.bz2 -C ~ tmp/dir2/here/1.lst