1. The shell sets up redirections BEFORE running the command: > ls truncates the file ls to empty first. ls(1) ignores
stdin, lists the directory, and writes to stdout which now points at the file ls. The terminal shows nothing; the listing goes
into the file. A classic lesson that redirection happens before execution.

4.7 A here-document
Combine a file's contents with inline text into file2.
cat file << EOF 1> file2
hello
EOF

1. << EOF is a here-document: the shell feeds every line up to EOF into cat as stdin. cat prints the named file plus the
here-doc text to stdout, and 1> file2 captures all of it. Here-docs are how scripts pass multi-line input to a command.

4.8 Copy via redirection
Duplicate a file using only redirection.
cat < file > file2

1. cat reads stdin (redirected from file) and writes stdout (redirected to file2). The effect is a copy. It shows how cat plus
redirection can stand in for cp in simple cases.

PRACTICE EXERCISES