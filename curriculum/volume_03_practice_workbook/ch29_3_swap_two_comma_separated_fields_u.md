3. Swap two comma-separated fields using capture groups.





12. find — Locating Files
12.1 By extension
Find all .txt files under ~/tmp.
find ~/tmp -type f -name "*.txt"

1. find walks the tree from ~/tmp. -type f limits to regular files; -name "*.txt" matches the pattern (quoted so the shell
does not expand it first). find tests each entry against these conditions.

12.2 Search several roots
Look for document.pdf under two directories at once.
find ~/tmp ~/doc -type f -name "document.pdf"

1. find accepts multiple starting directories; it searches all of them. The conditions apply the same way in each tree.

12.3 By size
Find files larger than 10 bytes.
find ~/tmp -type f -size +10c

1. -size +10c means greater than 10 characters (bytes). The suffixes are c bytes, k kilobytes, M megabytes. A leading +
means 'more than', - means 'less than'.

12.4 By name pattern
Find directories whose name has a t then an a.
find ~/tmp -type d -name "*t*a*"

1. -type d restricts to directories; the glob *t*a* requires a t somewhere before an a. find's -name uses shell-style globs,
not regex.

12.5 By modification time
Find files modified two or more days ago.
find ~/tmp -type f -mtime +1

1. -mtime counts in 24-hour days. +1 means older than 1 full day, which in find's arithmetic is 2 days or more. -mtime -1
would mean within the last day.

12.6 Several patterns with OR
Find temporary files of many kinds.





find ~/tmp -type f \( -name "*.tmp" -o -name "*.bak" -o -name "*~" \)

1. -o is logical OR. The escaped parentheses \( \) group the alternatives so the -type f applies to all of them. Grouping is
needed because otherwise -o would bind loosely and change the meaning.

12.7 By permission
Find files readable by others.
find ~/tmp -type f -perm -004

1. -perm -004 matches files where AT LEAST the others-read bit is set (the leading dash means 'all of these bits', tested
loosely). 004 is r for others in octal. This is how you audit world-readable files.

PRACTICE EXERCISES