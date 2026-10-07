6. NR is the line number — print lines 5 through 10.
OUTPUT

184729342 203.0.113.42
99182811 198.51.100.7
41230010 192.0.2.19

sort, uniq, cut, tr, xargs — the supporting cast
sort -t',' -k3 -n sales.csv
cut -d',' -f1,3 data.csv
tr 'a-z' 'A-Z' < names.txt
tr -d '\r' < windows.txt > unix.txt
cat urls.txt | xargs -n1 curl -sI | grep HTTP