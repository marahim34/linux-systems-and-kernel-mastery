1. Create with -c, inspect with -t before extracting, then extract only tmp/dir1 by naming it. -C sets the base directory
each time.

7b. Compare gzip vs bzip2 size
tar -czf a.tgz -C ~ tmp
tar -cjf a.tbz -C ~ tmp
ls -l a.tgz a.tbz