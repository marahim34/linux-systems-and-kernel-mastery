1. Two commands separated by a semicolon. The first replaces any run of whitespace with one space, globally (g). The
second removes trailing whitespace by matching spaces before end of line ($) and replacing with nothing. -E enables +
without a backslash.

11.2 Simple replacement
Rename Ellen Jones to Ellen Michaels everywhere.
sed 's/Ellen Jones/Ellen Michaels/g' names.txt

1. s/old/new/g substitutes on every line, g meaning all occurrences per line. Output goes to the screen; add -i to edit the
file in place once you trust the result.

11.3 Targeted replacement
Change Ike's number without touching Mike's.
sed -E '/^Ike Deveron.*phone/s/[0-9]{3}-[0-9]{4}/234-0123/' names.txt