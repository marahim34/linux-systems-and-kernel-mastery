1. After the comma and optional spaces, [A-Za-z]*a[A-Za-z]* matches a word that contains a lowercase a with letters
around it. The trailing whitespace marks the end of the first-name field.

10.4 Local numbers starting 5 or 6
Find numbers whose local part begins with 5 or 6.
grep -E "[[:space:]]+[[:digit:]]-([56])[[:digit:]]{3}$" data.txt

1. ([56]) matches a single 5 or 6 right after the area digit and hyphen; [[:digit:]]{3}$ requires three more digits to end the
line. Grouping with ( ) and the class [56] express 'either 5 or 6' cleanly.

PRACTICE EXERCISES