1. The shell feeds the three lines to cat as stdin until EOF; > notes.txt captures them. A clean way to write a small file
from a script.

Section 5 — Pipes
5a. Count conf files in /etc
ls /etc | grep conf | wc -l

1. ls lists /etc, grep keeps names containing conf, wc -l counts them. Each stage reads the previous stage's output —
the essence of a pipeline.

5b. Usernames from /etc/passwd
head -3 /etc/passwd | cut -d':' -f1

1. head -3 takes the first three lines, then cut splits on colon and prints field 1, the username. /etc/passwd is
colon-separated.

5c. Why cat file | ls > file is meaningless
# ls ignores stdin, so the piped data is discarded,
# and > file empties the file before ls even runs.