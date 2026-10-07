8. Data Tools — awk, cut, sort, nl, paste
8.1 Print the last field
Extract the final field of a line (here, the year from date).
date | awk '{print $NF}'

1. awk splits each line into fields $1, $2, and so on. NF is the number of fields, so $NF is always the LAST one
regardless of how many there are. This trick avoids counting columns.

8.2 Unique first names
List distinct first names from a space-separated file.
cut -d' ' -f1 names.txt | sort -u

1. cut takes field 1 using space as the delimiter. sort -u sorts and removes duplicates in one step (u = unique). Sorting is
required for uniqueness because duplicates must be adjacent.

8.3 Two columns from a CSV
Print columns 1 and 3 of a comma-separated file.
cut -d',' -f1,3 data.txt

1. -d',' sets comma as the separator; -f1,3 selects fields 1 and 3 together. cut is ideal when you simply need specific
columns and no computation.

8.4 File sizes with awk
Show just the size column of ls output for dotfiles.
ls -l .bash* | awk '{print $5}'