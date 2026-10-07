1. With no -t, sort splits on whitespace. -k3,3 keys on the third field only. This orders the data by the complete phone
number string.

9.3 By local part, numerically
Split on hyphen and sort by the second piece as a number.
sort -t"-" -k2,2n data.txt

1. -t"-" makes the hyphen the separator; -k2,2n keys on field 2 and the trailing n forces NUMERIC sort, so 9 comes
before 10 (a plain text sort would put 10 first).

9.4 Sort a directory listing by name
Order ls -la output by filename.
ls -la | sort -k9,9