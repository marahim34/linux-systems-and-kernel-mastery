7. Any delimiter works — use | when your pattern is full of slashes (paths), avoiding escape soup.

awk — complete treatment
awk sees every line as columns ($1, $2...; $0 = whole line) and runs pattern { action } rules on each. It has
variables, math, and even functions — a mini programming language for tabular text.





awk '{print $1, $9}' access.log
awk -F: '{print $1}' /etc/passwd
awk '$9 >= 500' access.log
awk '{bytes[$1] += $10} END {for (ip in bytes) print bytes[ip], ip}' access.log | sort -rn
| head -5
df -h | awk '$5+0 > 80 {print $6, "is", $5, "full"}'
awk 'NR==5,NR==10' file.txt