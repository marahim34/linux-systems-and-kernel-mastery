1. For 4.3, the file named 2 is created empty because echo emits no errors. For 4.6, > ls truncates first, then the
directory listing is written into the file, so the terminal stays silent and cat ls shows the result.

4b. Split streams of a mixed command
ls /etc /nope > out.txt 2> err.txt
cat out.txt # the successful /etc listing
cat err.txt # the 'No such file' error for /nope

1. /etc succeeds (stdout) and /nope fails (stderr). Separate redirections put each stream in its own file.

4c. Here-document into a file
cat << EOF > notes.txt
line one
line two
line three
EOF
cat notes.txt