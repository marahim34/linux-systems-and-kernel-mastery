4. The correct way to read a file LINE BY LINE: IFS= preserves whitespace, -r prevents backslash mangling...
5. ...and < input.txt feeds the file in. This is the safe file-reading pattern.

PRO INSIGHT: The dangerous anti-pattern to avoid: for line in $(cat file). It breaks on spaces and is a classic bug.
The correct line-by-line read is the while IFS= read -r loop above. Similarly, prefer for f in *.log (a glob) over for f in
$(ls *.log) — the glob handles spaces and odd filenames safely. Loops that touch filenames must be written
carefully.
PRACTICE EXERCISES