3. File Globbing
Globs are patterns the SHELL expands into matching filenames before the command runs. They are not
regex. Create a few test files first (touch A1.txt file2.log photo.JPG notes.md) to see each one work.

3.1 Uppercase-starting names
List files whose name starts with an uppercase letter.
ls [A-Z]*

1. [A-Z] matches exactly one character in the range A to Z; the trailing * matches any rest. So the whole pattern is 'one
uppercase letter, then anything'.

3.2 A number, then .lst or .log
List files containing a digit and ending in .lst or .log.
ls *[0-9]*.lst *[0-9]*.log

1. [0-9] matches one digit; the surrounding * allow anything before and after it. Two separate patterns are given as two
arguments, so both extensions are matched in one command.

3.3 Any three-character extension
List files ending with a dot and exactly three characters.
ls *.???

1. ? matches exactly one character. Three of them after the dot means an extension of exactly three characters, such as
.txt or .log but not .md or .html.

3.4 Every spelling of .jpg
Match .jpg, .JPG, .Jpg and so on in one argument.
ls *.[jJ][pP][gG]