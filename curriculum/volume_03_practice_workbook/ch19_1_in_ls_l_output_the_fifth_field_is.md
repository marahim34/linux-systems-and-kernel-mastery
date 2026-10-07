1. In ls -l output the fifth field is the byte size, so awk '{print $5}' prints only sizes. The glob .bash* limits the listing to
bash-related dotfiles.

8.5 Number every line
Add line numbers, including blank lines.
nl -ba test.txt

1. nl numbers lines. -ba means number ALL body lines (b) including blanks (a). Without it, nl skips empty lines by
default, which surprises people.

8.6 Join files side by side
Merge two files column-wise.





paste 1.txt 2.txt

1. paste places corresponding lines of each file next to each other separated by a tab. It is the horizontal counterpart to
cat, which stacks files vertically.

PRACTICE EXERCISES