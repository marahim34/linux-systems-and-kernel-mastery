4. Delete carriage returns — THE fix for 'bad interpreter ^M' errors when scripts were edited on Windows. You will need
this in WSL someday.
5. xargs turns input lines into command arguments: check the HTTP status of every URL in a file.

Worked example — full log investigation
# Question: which URLs caused the most 404s yesterday?
grep "$(date -d yesterday +%d/%b/%Y)" access.log \
| awk '$9 == 404 {print $7}' \
| sort | uniq -c | sort -rn | head