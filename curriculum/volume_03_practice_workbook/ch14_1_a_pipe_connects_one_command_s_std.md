1. A pipe connects one command's stdout to the next command's stdin, so the next command must actually READ
stdin. ls does not read stdin, so piping into it is pointless. Redirection needs a filename, not a command, so > cat file is a
syntax error. The two sensible lines chain readers of stdin correctly.

5.2 Extract a field
Print the second space-separated field of a string.
echo "1 2 3" | cut -d" " -f2

1. echo sends the text into the pipe. cut splits on the delimiter set by -d (a space) and -f2 selects field two, printing 2. cut
is the lightweight tool for column extraction when no logic is needed.

5.3 Save a clean manual page
Turn a man page into plain text without control characters.
man nano | col -b > nano-manual.txt

1. man formats its page with backspace-based bold and underline. col -b strips those control sequences, leaving plain
ASCII. The result is redirected into a text file you can read or search anywhere.

PRACTICE EXERCISES