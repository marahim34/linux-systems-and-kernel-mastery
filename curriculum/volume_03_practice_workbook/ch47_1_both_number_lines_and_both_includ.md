1. Both number lines and both include blank lines here (nl needs -ba to do so; cat -n always does). nl offers more
formatting control such as separators and starting number.

Section 9 — Sorting
9a. Numeric column ascending then descending
sort -t',' -k2,2n data.csv
sort -t',' -k2,2nr data.csv

1. -k2,2n sorts field 2 numerically ascending; adding r reverses to descending. Restricting the key to 2,2 avoids
surprises from later fields.

9b. -k3 versus -k3,3
sort -k3 file # from field 3 to END of line
sort -k3,3 file # field 3 ONLY

1. -k3 uses field 3 through the line's end as the sort key, so later fields act as tiebreakers. -k3,3 keys on exactly field 3.
The difference shows when field 3 values tie.

9c. ls sorted by size, biggest last
ls -la | sort -k5,5n