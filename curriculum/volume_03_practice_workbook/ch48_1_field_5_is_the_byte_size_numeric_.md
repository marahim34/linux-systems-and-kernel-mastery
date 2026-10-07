1. Field 5 is the byte size; numeric ascending puts the largest file at the bottom. Add r to put it on top.

Section 10 — grep
10a. Count comment lines
grep -E "^#" /etc/ssh/ssh_config | wc -l

1. ^# matches lines beginning with a hash (comments); wc -l counts them. Works on any config file.





10b. Lines ending in exactly four digits
grep -E "[0-9]{4}$" file

1. [0-9]{4}$ requires four digits immediately before end of line. Add a boundary like [^0-9] before it if you must exclude
longer runs.

10c. {1} and (5|6) equivalence
grep -E "[[:digit:]]-(5|6)[[:digit:]]{3}$" data.txt

1. [56] and (5|6) both mean 'a 5 or a 6' for a single character, so they are interchangeable here. {1} is implicit for a single
item, so writing it changes nothing.

Section 11 — sed
11a. http to https, then in place
sed 's/http:/https:/g' site.conf # preview
sed -i.bak 's/http:/https:/g' site.conf # apply, keep .bak
diff site.conf.bak site.conf