1. Relative archives are portable and safe; absolute-path archives can clobber real system locations on extraction.

Section 8 — Data Tools





8a. Last field of every line
awk '{print $NF}' file

1. $NF is the last field on each line regardless of field count, so this prints the final column throughout the file.

8b. Sorted unique extensions
ls | sed -n 's/.*\.//p' | sort -u

1. sed strips everything up to the last dot, leaving the extension; sort -u gives the unique sorted set. Files without a dot
produce no output.

8c. nl -ba vs cat -n
nl -ba file
cat -n file