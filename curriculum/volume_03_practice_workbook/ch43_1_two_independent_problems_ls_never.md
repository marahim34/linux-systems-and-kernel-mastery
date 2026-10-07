1. Two independent problems: ls never reads the piped input, and the redirection truncates the file first. Nothing useful
can result.





Section 6 — Meta Characters
6a. 'This directory holds N files'
echo "This directory holds $(ls -1 | wc -l) files"

1. ls -1 lists one name per line, wc -l counts them, and $( ) drops that number into the sentence.

6b. Today's date in a sentence
echo "Today is $(date +%F)"

1. date +%F prints YYYY-MM-DD; command substitution inserts it into the text.

6c. Line count of .bashrc
echo "~/.bashrc has $(wc -l < ~/.bashrc) lines"

1. wc -l < file counts lines without printing the filename, so the sentence reads cleanly.

Section 7 — Archiving
7a. Archive, list, extract one file
tar -C ~ -czf ~/tmp.tgz tmp
tar -tzf ~/tmp.tgz | head
tar -xzf ~/tmp.tgz -C /tmp tmp/dir1