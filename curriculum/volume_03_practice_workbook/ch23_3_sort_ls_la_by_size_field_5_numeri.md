3. Sort ls -la by size (field 5) numerically and confirm the biggest file is last.





10. grep — Pattern Searching
These use POSIX classes: [[:space:]] any whitespace, [[:digit:]] any digit. -E turns on extended regex so +,
{n}, ( ) and | work without backslashes.

10.1 Numbers starting with 4
Find phone numbers whose local part starts with 4.
grep -E "[[:space:]]+4-[[:digit:]]{4}$" data.txt

1. [[:space:]]+ matches the spaces before the number; 4- is a literal '4-'; [[:digit:]]{4} matches exactly four digits; $
anchors to end of line. Together: a number of the form 4-NNNN at the line's end.

10.2 Last name S, phone has a 2
Match lines where the last name starts with S and the number contains 2.
grep -E "^S[^,]*,.*[0-9-]*2" data.txt

1. ^S anchors an uppercase S at line start; [^,]* is the rest of the last name up to the comma; ,.* skips ahead; [0-9-]*2
requires a 2 somewhere in the digits. Anchors plus negated classes let you target a specific field.

10.3 First name contains lowercase a
Match people whose first name has an 'a'.
grep -E ",[[:space:]]*[A-Za-z]*a[A-Za-z]*[[:space:]]+" data.txt