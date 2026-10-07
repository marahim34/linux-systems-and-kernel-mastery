# Volume 3: The Practice Workbook

LINUX MASTERY
VOLUME 3 — THE PRACTICE
WORKBOOK
Sixty Worked Exercises with Full Explanations — Vim, Files, Globbing, Redirection,
Pipes, Meta Characters, Archiving, Text Tools, grep, sed, find & the Shell
Environment

Based on the TAMK Linux exercise set · Solved and explained
Prepared for MD Abdur Rahim · Tampere, Finland · 2026





How to Use This Workbook
Each entry gives the task, the command, and a numbered explanation of every part. Read the task, cover
the command, and try it yourself in a terminal first. Then reveal the answer and check your reasoning against
the explanation. The sections build on each other, so work top to bottom.
Set up a scratch area once and practice everything inside it, so nothing important is ever at risk:
mkdir -p ~/tmp && cd ~/tmp

1. Create a disposable working directory and enter it. Everything in this workbook happens here.

Sections
1. Vim — configuration and editing
2. Files & Directories — structure, moving, copying
3. File Globbing — the shell's pattern language
4. Redirection — stdin, stdout, stderr
5. Pipes — composing commands
6. Meta Characters — command substitution
7. Archiving — gzip & tar
8. Data Tools — awk, cut, sort, nl, paste
9. Sorting — the sort command in depth
10. grep — pattern searching with regex
11. sed — stream editing
12. find — locating files by any criterion
13. Shell Environment — variables and the prompt
14. User Commands — writing shell functions





Terms & Commands — What They Are and When to
Use Them
A quick reference for every tool and term used in this workbook. Read this first, then keep it beside you while
solving. The 'When to use' column is the part worth memorising.

Editing & the shell
Term

What it is

When to use it

vim

A modal terminal text editor

Editing files on any server; fast
keyboard-only edits

.vimrc

Vim's personal config file in ~

Store your editor preferences once,
applied everywhere

Normal / Insert mode

Vim's command mode vs typing
mode

Esc for Normal (navigate/edit), i for
Insert (type)

bash

The default shell that runs
commands

Every command line; scripting

.bashrc

Per-shell startup config in ~

Aliases, functions, PATH, prompt —
loaded each shell

.profile

Login-shell startup config

Environment for SSH/console login
sessions

PS1

The prompt format variable

Customise what your prompt shows

function

A named block of shell code

Turn a repeated command sequence
into one word

export

Marks a variable for child processes

When a variable must be seen by
programs you launch

Files, directories & navigation
Term

What it is

When to use it

cd

Change directory

Move around the tree; cd alone goes
HOME

pwd

Print working directory

Confirm where you are before acting

ls

List directory contents

See what is here; -l detail, -a hidden,
-R recursive

mkdir -p

Make directories, parents included

Create a whole nested path in one
command

cp

Copy files/directories

-r for folders, -a to preserve metadata
(backups)

mv

Move or rename

Reorganise or rename; same
command for both





Term

What it is

When to use it

rm

Remove files

Delete; rm -r for folders — no undo,
check the path

touch

Create empty file / update time

Make test files; refresh a timestamp

~ (tilde)

Your home directory

Shorthand for /home/you in any path

. and ..

Current and parent directory

Relative paths; ./script.sh, cd ..

Globbing — shell filename patterns
Pattern

What it matches

When to use it

*

Any characters, any length

Broad matches: *.txt, back*

?

Exactly one character

Fixed-length parts: file?.log, *.???

[A-Z]

One character in a range/set

First letter uppercase: [A-Z]*

[^0-9]

One character NOT in the set

Exclude digits at a position

[jJ]

One of the listed characters

Case variations: *.[jJ][pP][gG]

TIP: Globs are expanded by the SHELL into filenames before the command runs. They are NOT regex — [A-Z]*
means 'uppercase letter then anything', while in regex it would mean something different. When a task needs true
'NOT' logic across a whole name, pipe to grep instead.

Redirection & pipes
Symbol

What it does

When to use it

&gt;

stdout to a file (overwrite)

Save output: date &gt; date.txt

&gt;&gt;

stdout to a file (append)

Add to a log without erasing it

2&gt;

stderr to a file

Capture only errors: cmd 2&gt;
err.log

&lt;

file as stdin

Feed input from a file: less &lt; file

2&gt;&amp;1

stderr follows stdout

Send both streams to one place

&lt;&lt; EOF

here-document

Feed inline multi-line text to a
command

|

stdout of one cmd to stdin of next

Compose tools: ls | grep conf | wc -l

TIP: Key insight for the tricky cases: the shell sets up ALL redirections BEFORE the command runs. That is why ls
< ls > ls truncates the file first. And a command only benefits from a pipe if it actually READS stdin — piping into ls
is pointless because ls ignores stdin.

Meta characters





Term

What it is

When to use it

$( )

Command substitution

Insert a command's output into a line

$VAR

Variable expansion

Use a value: echo $HOME

" " vs ' '

Double vs single quotes

Double allows $expansion; single is
literal

\

Escape / line continuation

Protect a special char, or split a long
command

Archiving & compression
Term

What it is

When to use it

gzip

Compress a single file

Shrink one file; -9 max, -d
decompress

tar

Bundle many files into one archive

Package a directory tree

-c / -x / -t

Create / extract / list

The three tar verbs

-z / -j

gzip / bzip2 compression

-z common, -j smaller but slower

-f

Names the archive file

Always present: tar -czf name.tgz dir

-C

Change to a directory first

Relative paths in, chosen extract
location out

Tool

What it is

When to use it

cut

Extract columns by delimiter

Pull fixed fields: cut -d',' -f1,3

awk

Field-aware mini language

Column math, $NF, conditional
printing

sort

Order lines

-n numeric, -r reverse, -k key, -t sep,
-u unique

uniq

Collapse adjacent duplicates

After sort; -c to count

nl

Number lines

Add line numbers; -ba includes
blanks

paste

Join files side by side

Merge columns from two files

tr

Translate/delete characters

Case change, strip \r, split on a char

wc

Count lines/words/bytes

-l lines is the common one

Text processing tools

Searching & editing streams





Tool / term

What it is

When to use it

grep

Search lines by pattern

Find text; -r recursive, -i ignore case,
-E regex

-E (ERE)

Extended regex mode

Use +, {n}, ( ), | without backslashes

[[:space:]]

POSIX class: whitespace

Portable, clear whitespace matching

[[:digit:]]

POSIX class: digits

Same as [0-9], clearer intent

^ and $

Line start / line end anchors

Pin a match to the beginning or end

sed

Stream editor

Search-replace, delete, reorder lines

s/a/b/g

Substitute command

Replace a with b, g = every match
per line

capture ( ) \1

Remember and reuse text

Reorder fields: swap First and Last

/pat/d

Delete matching lines

Remove entries by pattern

Term

What it is

When to use it

find

Walk a tree, test each entry, act

Locate files by any attribute

-type f / d

Regular file / directory

Restrict what you match

-name / -iname

Glob on the name / case-insensitive

Match by filename pattern

-size +10c

By size (c bytes, k, M)

Find big or small files; + more, - less

-mtime +1

By modification age in days

Find old/recent files

-perm -004

By permission bits

Audit world-readable, executable,
etc.

-o and \( \)

OR, and grouping

Combine several name patterns

-exec ... {} +

Run a command per match

Act on results: delete, chmod, ls

Finding files





1. Vim — Configuration and Editing
1.1 Vim configuration location
Where is the user's personal Vim configuration file?
~/.vimrc

1. ~ is your HOME directory; .vimrc is the personal config vim reads on startup. It holds all your personal settings. A
leading dot makes it hidden from a normal ls.

1.2 A useful .vimrc
Set common editing preferences, each explained inline with Vim comments (").
set ruler " show cursor position in status line
set nojoinspaces " no double space after punctuation on join
set showcmd " show partial commands bottom-right
set showmatch " highlight matching bracket
set incsearch " show matches while typing a search
set ignorecase " search ignores case...
set smartcase " ...unless the query has a capital
set nobackup " do not leave backup~ files
set autoindent " new lines keep the previous indent
set shiftwidth=4 " indent step is 4 columns
set softtabstop=4 " Tab key inserts 4 spaces
set nolist " do not draw whitespace symbols

1. In vim, a double quote begins a comment. Each set line toggles one option. ignorecase + smartcase together give the
smartest search behaviour: case-insensitive until you deliberately type an uppercase letter. autoindent, shiftwidth and
softtabstop are the three that make code editing comfortable.

1.3 Essential editing keys
The movements and edits you use constantly (press in Normal mode, Esc first).
0 -> beginning of line
$ -> end of line
dw -> delete a word
dd -> delete a line
dap -> delete a paragraph
gg -> go to first line
G -> go to last line
yy -> yank (copy) a line
yap -> yank a paragraph
:set number / :set nonumber -> line numbers on / off

1. These follow vim's verb+noun grammar: d (delete) or y (yank) combine with w (word), d (line, doubled), ap (a
paragraph). 0 and $ are line ends; gg and G are file ends. Colon commands like :set change settings live.

PRACTICE EXERCISES
1. Create ~/.vimrc with the settings from 1.2, open a file, and confirm ruler and line numbers behave.
2. Practice 1.3 on a throwaway file: delete a word, a line, a paragraph; copy and paste each.
3. Toggle numbers with :set number and :set nonumber; try relativenumber too.









2. Files & Directories
2.1 Create a directory structure
Build a nested hierarchy under ~/tmp in one command.
cd
mkdir -p ~/tmp/some/dir1 \
~/tmp/some/dir2/doc1 \
~/tmp/some/dir2/doc2/test/more \
~/tmp/some/dir3/html
ls -R ~/tmp/some

1. cd with no argument goes HOME. mkdir -p creates every missing parent in a path and never errors if something
already exists, so several deep branches are built at once. The backslash at line end continues one command across
lines. ls -R lists recursively to verify the whole tree.

2.2 Move files around
Reorganise files between directories with mv (setup shown first).
mkdir -p ~/tmp/tmp2
mv ~/tmp/dir1 ~/tmp/tmp2/
mv ~/tmp/dir2 ~/tmp/tmp2/
mv ~/tmp/tmp2/dir2/here/1.lst ~/tmp/tmp2/dir1/1.lst
mv ~/tmp/tmp2/dir1/1.txt ~/tmp/tmp2/dir2/1.txt
ls -R ~/tmp/tmp2

1. mv both moves and renames: give it a directory target to move into it, or a full new path to move-and-rename in one
step. Moving a directory carries all its contents. Build such reorganisations one line at a time and re-run ls -R after each
to confirm.

2.3 Reading the cp manual
The four cp options every backup uses (from man cp).
-v, --verbose explain what is being done
-u update: copy only if source is newer
-p preserve mode, ownership, timestamps
-R, -r copy directories recursively

1. -v narrates each copy. -u skips files already up to date, so re-running a big copy is cheap. -p keeps metadata intact,
which matters for backups and deploys. -r (or -R) is required to copy a directory and its contents.

2.4 A full recursive backup
Copy all of ~/tmp into ~/tmp.backup.
cp -r ~/tmp ~/tmp.backup

1. -r walks the whole tree and copies every file and subdirectory. For a backup that also preserves permissions and
timestamps, cp -a (archive) is the stronger choice, as covered in the main volume.

PRACTICE EXERCISES





1. Build the 2.1 tree from scratch, then use mv to swap two files between branches and verify with ls -R.
2. Read man cp and find one option not listed here (try --backup); explain what it does.
3. Make a backup with cp -r, then redo it with cp -a and compare timestamps using ls -l on both.





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

1. Each bracket offers both cases for one letter, so every combination of upper and lower case across the three letters is
covered by a single glob.

3.5 Suspicious filenames
List names containing anything other than letters, numbers, _ - or dot.
ls | grep -E '[^A-Za-z0-9_.-]'

1. Globbing alone can not express 'NOT these characters' across a whole name, so we pipe the listing to grep. Inside
the bracket the leading ^ means NEGATE, so this finds any name containing a character outside the allowed set:
spaces, quotes, and other troublemakers.

3.6 No digit in 2nd and 4th position
List names where characters two and four are not digits.





ls ?[^0-9]?[^0-9]*

1. Read position by position: ? any first char, [^0-9] a non-digit second char, ? any third char, [^0-9] a non-digit fourth
char, then * the rest. Inside a glob bracket, ^ also means negate.

PRACTICE EXERCISES
1. Create files: A1.txt b2.log C3.JPG d4d.md 'weird name.txt'. Run every glob above and predict each result first.
2. Write a glob for files whose name is exactly four characters plus any extension.
3. Explain why 3.5 needs grep while 3.1 to 3.4 do not.





4. Redirection — stdin, stdout, stderr
Every command has three streams: input (fd 0), normal output (fd 1), and errors (fd 2). Redirection sends
each stream to or from a file. Getting this precise is what separates confident users from hopeful ones.

4.1 Save output to a file
Write the current date into date.txt.
date > date.txt

1. > sends stdout (fd 1) to a file, creating or overwriting it. The terminal shows nothing because the output went to the
file instead.

4.2 Save only errors
Run a non-existent command and capture its error.
qwerty 2> error.log

1. 2> redirects stderr (fd 2) only. The shell's 'command not found' message is an error, so it lands in error.log while
stdout (empty here) is untouched.

4.3 A subtle one: echo 2 2>2
What does this create?
echo 2 2>2

1. echo writes the text 2 to stdout (the terminal). The 2>2 part redirects stderr to a file literally named 2. echo produces
no errors, so the file 2 is created but stays empty. A neat trap that tests whether you can separate the two streams.

4.4 Split output and errors
Send stdout and stderr to different files; order does not matter.
cat qwerty 2> error.log 1> file.tmp

1. cat on a missing file prints normal output nowhere and an error to stderr. 1> file.tmp catches stdout, 2> error.log
catches stderr. Writing them in either order gives the same result, so the error message reliably lands in error.log.

4.5 Feed a file as input
Page through a log by redirecting stdin.
less < /var/log/dpkg.log

1. < redirects stdin from a file. less with no filename argument reads stdin, so this is equivalent to less /var/log/dpkg.log.
Useful to know because many filters read stdin the same way.

4.6 The self-referential trap
With an empty file named ls present, what does ls < ls > ls do?





ls < ls > ls

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
1. Predict, then run, each of 4.3, 4.6: check with ls -l and cat what files were created and their contents.
2. Capture both streams of a mixed command (ls /etc /nope) into out.txt and err.txt separately.
3. Write a here-document that feeds three lines into cat and saves them to notes.txt.





5. Pipes — Composing Commands
5.1 Which pipelines make sense
Judge each; two are nonsense.
ls | cat | less # sensible
cat < file | less # sensible (= less file)
cat file | ls > file # nonsense: ls ignores stdin, and clobbers file
ls | less > cat file # nonsense: invalid syntax

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
1. Build a pipeline that lists /etc, keeps only lines containing conf, and counts them.
2. Use cut to pull the username (field 1) from three lines of /etc/passwd via a pipe.
3. Explain in one sentence why cat file | ls > file is meaningless.





6. Meta Characters — Command Substitution
6.1 Embed a command's result
Print a sentence that includes a computed line count.
echo "The result of this command is $(ls -la | wc -l)"

1. $( ) runs the inner command first and substitutes its output into the surrounding text. Inside it, ls -la lists the directory
and wc -l counts the lines. The shell replaces the whole $( ... ) with that number before echo prints the sentence.

6.2 Insert the current time
Display the time as HH:MM:SS using no variables.
echo "Time is $(date +%H:%M:%S)"

1. date +%H:%M:%S formats the current time. Wrapped in $( ), its output is pasted into the string, so echo prints a live
timestamp. The + introduces a custom format where %H %M %S are hours, minutes, seconds.

PRACTICE EXERCISES
1. Print: 'This directory holds N files' where N is computed with $(...) and wc.
2. Print today's date in YYYY-MM-DD form inside a sentence using date +%F.
3. Nest it: echo the number of lines in your .bashrc using command substitution.





7. Archiving — gzip & tar
7.1 Maximum compression
Compress file.txt as hard as gzip can.
gzip -9 file.txt

1. gzip replaces file.txt with file.txt.gz. -9 selects the strongest (slowest) compression level; -1 is fastest and weakest.
Note gzip works on a single file and removes the original by default.

7.2 Decompress
Restore file.txt from its .gz.
gzip -d file.txt.gz

1. -d decompresses, recreating file.txt and removing the .gz. gunzip file.txt.gz does exactly the same thing.

7.3 Create a tar.gz with relative paths
Archive ~/tmp so entries read tmp/... not /home/you/tmp/...
tar -C "$HOME" -czf "$HOME/package.tar.gz" tmp

1. -C changes into $HOME first, so the archived path is the relative tmp. -c create, -z gzip, -f names the output file.
Relative paths make archives safe to extract anywhere without overwriting absolute locations.

7.4 List an archive's contents
See what is inside without extracting.
tar -tzf "$HOME/package.tar.gz"

1. -t lists the table of contents, -z for gzip, -f the file. Always inspect an archive with -t before extracting so you know
what and where it will write.

7.5 Extract into a directory
Unpack the archive under /tmp.
tar -xzf ~/package.tar.gz -C /tmp

1. -x extract, -z gzip, -f file, and -C /tmp extracts INTO /tmp. Without -C it would extract into the current directory.

7.6 Use bzip2 compression
Create a .tar.bz2 instead of gzip.
tar -cjf ~/package.tar.bz2 -C ~ tmp

1. -j selects bzip2 instead of gzip (-z). bzip2 usually compresses a little smaller but slower. The rest of the flags mirror
7.3.





7.7 Extract a single file
Pull just one file out of a bz2 archive.
tar -xjf ~/package.tar.bz2 -C ~ tmp/dir2/here/1.lst

1. Naming a path after the archive extracts only that entry. -x extract, -j bzip2, -f file, -C ~ chooses where it lands. Handy
for recovering one file from a large backup.

PRACTICE EXERCISES
1. Archive your ~/tmp tree with gzip, list it with -t, then extract one file into /tmp.
2. Compare sizes: make both a .tar.gz and a .tar.bz2 of the same folder and ls -l them.
3. Explain why -C matters for portable, safe archives.





8. Data Tools — awk, cut, sort, nl, paste
8.1 Print the last field
Extract the final field of a line (here, the year from date).
date | awk '{print $NF}'

1. awk splits each line into fields $1, $2, and so on. NF is the number of fields, so $NF is always the LAST one
regardless of how many there are. This trick avoids counting columns.

8.2 Unique first names
List distinct first names from a space-separated file.
cut -d' ' -f1 names.txt | sort -u

1. cut takes field 1 using space as the delimiter. sort -u sorts and removes duplicates in one step (u = unique). Sorting is
required for uniqueness because duplicates must be adjacent.

8.3 Two columns from a CSV
Print columns 1 and 3 of a comma-separated file.
cut -d',' -f1,3 data.txt

1. -d',' sets comma as the separator; -f1,3 selects fields 1 and 3 together. cut is ideal when you simply need specific
columns and no computation.

8.4 File sizes with awk
Show just the size column of ls output for dotfiles.
ls -l .bash* | awk '{print $5}'

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
1. From any space-separated file, print the last field of every line with awk.
2. Get the sorted unique set of file extensions in a directory (hint: ls, cut or awk, sort -u).
3. Number a file with nl -ba and compare to cat -n.





9. Sorting in Depth
A shared data file helps here: lines like 'Lastname, Firstname area-local' with fields separated by commas,
spaces and hyphens.

9.1 Reverse by last name
Sort by the first field (before the comma), descending.
sort -t"," -k1,1 -r data.txt

1. -t sets the field separator to a comma; -k1,1 sorts by field 1 only (from key 1 to key 1); -r reverses to descending
order. Limiting the key with 1,1 stops sort from using the rest of the line as a tiebreaker in unexpected ways.

9.2 By whole phone number
Sort by the third whitespace field.
sort -k3,3 data.txt

1. With no -t, sort splits on whitespace. -k3,3 keys on the third field only. This orders the data by the complete phone
number string.

9.3 By local part, numerically
Split on hyphen and sort by the second piece as a number.
sort -t"-" -k2,2n data.txt

1. -t"-" makes the hyphen the separator; -k2,2n keys on field 2 and the trailing n forces NUMERIC sort, so 9 comes
before 10 (a plain text sort would put 10 first).

9.4 Sort a directory listing by name
Order ls -la output by filename.
ls -la | sort -k9,9

1. In ls -la, the ninth field is the filename. Keying on 9,9 sorts by name while keeping each full line intact. Piping ls into
sort lets you reorder by any column.

PRACTICE EXERCISES
1. Sort a CSV by a numeric column ascending, then descending.
2. Explain the difference between -k3 and -k3,3 by trying both on the same file.
3. Sort ls -la by size (field 5) numerically and confirm the biggest file is last.





10. grep — Pattern Searching
These use POSIX classes: [[:space:]] any whitespace, [[:digit:]] any digit. -E turns on extended regex so +,
{n}, ( ) and | work without backslashes.

10.1 Numbers starting with 4
Find phone numbers whose local part starts with 4.
grep -E "[[:space:]]+4-[[:digit:]]{4}$" data.txt

1. [[:space:]]+ matches the spaces before the number; 4- is a literal '4-'; [[:digit:]]{4} matches exactly four digits; $
anchors to end of line. Together: a number of the form 4-NNNN at the line's end.

10.2 Last name S, phone has a 2
Match lines where the last name starts with S and the number contains 2.
grep -E "^S[^,]*,.*[0-9-]*2" data.txt

1. ^S anchors an uppercase S at line start; [^,]* is the rest of the last name up to the comma; ,.* skips ahead; [0-9-]*2
requires a 2 somewhere in the digits. Anchors plus negated classes let you target a specific field.

10.3 First name contains lowercase a
Match people whose first name has an 'a'.
grep -E ",[[:space:]]*[A-Za-z]*a[A-Za-z]*[[:space:]]+" data.txt

1. After the comma and optional spaces, [A-Za-z]*a[A-Za-z]* matches a word that contains a lowercase a with letters
around it. The trailing whitespace marks the end of the first-name field.

10.4 Local numbers starting 5 or 6
Find numbers whose local part begins with 5 or 6.
grep -E "[[:space:]]+[[:digit:]]-([56])[[:digit:]]{3}$" data.txt

1. ([56]) matches a single 5 or 6 right after the area digit and hyphen; [[:digit:]]{3}$ requires three more digits to end the
line. Grouping with ( ) and the class [56] express 'either 5 or 6' cleanly.

PRACTICE EXERCISES
1. On any /etc file, grep -E lines that begin with a comment (^#) and count them with wc -l.
2. Write a pattern that matches lines ending in exactly four digits.
3. Rewrite 10.4 using {1} and explain why [56] and (5|6) are equivalent here.





11. sed — Stream Editing
11.1 Collapse extra spaces
Make every run of spaces a single space and trim trailing ones.
sed -E 's/[[:space:]]+/ /g; s/[[:space:]]+$//' names.txt

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

1. A leading /pattern/ restricts the s command to matching lines only. Here only lines beginning with 'Ike Deveron' and
containing 'phone' are edited, so 'Mike' (which does not start with 'Ike') is safe. Then the number pattern is replaced.

11.4 Delete matching lines
Remove every entry for Evelyn Jordan.
sed '/^Evelyn Jordan/d' names.txt

1. /pattern/d deletes lines matching the pattern. Anchoring with ^ ensures only lines that START with the name are
removed. This is the delete counterpart to substitution.

11.5 Swap two fields
Reformat 'First Last' into 'Last First'.
sed -E 's/^([A-Za-z]+)[[:space:]]+([A-Za-z]+)/\2 \1/' names.txt

1. Parentheses capture groups: group 1 is the first word, group 2 the second. In the replacement, \2 \1 prints them in
reversed order. Capture-and-reorder is one of sed's most useful patterns.

PRACTICE EXERCISES
1. Use sed to change all http: to https: in a copy of a config, then add -i and re-check with diff.
2. Delete all blank lines from a file with sed '/^$/d'.
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
1. Find every file over 1 MB under your home and list them with -exec ls -lh {} +.
2. Find files changed in the last day (-mtime -1) and count them.
3. Combine conditions: files named *.log AND larger than 10k, using -a or just stacking conditions.





13. Shell Environment
13.1 Two key variables
Explain PATH and HOME and how to set them.
export PATH="$HOME/bin:$PATH"
export HOME="/home/marahim34"

1. PATH is the colon-separated list of directories searched for commands; putting $HOME/bin first lets your own scripts
take priority. HOME is your home directory, used by ~ expansion and by cd with no argument. export makes a variable
visible to child processes. Add these lines to ~/.bashrc (interactive shells) or ~/.profile (login shells) to make them
permanent.

13.2 A custom prompt
Set PS1 to show host, history number, time and directory.
PS1="[\h \! \A] \w\$ "

1. PS1 defines the prompt. \h is the hostname, \! the history number, \A the time HH:MM, \w the current directory, and \$
shows $ for a normal user or # for root. Put it in ~/.bashrc and run source ~/.bashrc to apply without reopening the shell.

PRACTICE EXERCISES
1. Add $HOME/bin to your PATH permanently, create a script there, and run it by name from anywhere.
2. Design your own PS1 with colour and the git-free basics; reload with source ~/.bashrc.
3. Print your current PATH split onto separate lines with: echo $PATH | tr ':' '\n'.





14. User Commands — Shell Functions
A function is a named block of shell code. Define these in ~/.bashrc so they are available in every session.

14.1 List only directories
_lsd shows just the directories here.
_lsd() {
ls -p | grep '/$'
}

1. ls -p appends a slash to directory names. grep '/$' keeps only lines ENDING in a slash, which are exactly the
directories. Wrapping it in _lsd() { ... } makes it a reusable command.

14.2 List only files
_lsf shows just the regular files here.
_lsf() {
ls -p | grep -v '/$'
}

1. Same idea inverted: grep -v drops the lines ending in a slash, leaving non-directories. -v means 'invert the match'.

14.3 My processes
_ps shows processes owned by the current user.
_ps() {
ps -u "$USER" -f
}

1. ps -u "$USER" filters to processes owned by whoever is logged in; -f gives the full-format listing. $USER is a shell
variable holding your username, so the function works for anyone.

14.4 List by size
_lsize lists files sorted by size ascending.
_lsize() {
ls -la | sort -n -k 5
}

1. ls -la produces the detailed listing whose fifth column is the size. sort -n -k 5 sorts numerically on that column,
smallest first. Combining a listing with sort is a general pattern for ranking by any column.

PRO INSIGHT: Define all four in ~/.bashrc, then run source ~/.bashrc. From then on _lsd, _lsf, _ps and _lsize
behave like built-in commands in every terminal you open.
PRACTICE EXERCISES
1. Add the four functions to ~/.bashrc and use each in a real directory.
2. Write _lsize_desc that sorts largest first (add -r) and compare.





3. Write a function mkcd() that makes a directory and cd's into it in one step.

Work every exercise by hand. Reading the answer is learning; typing it is
remembering.
— End of Volume 3, The Practice Workbook —

Solutions to the Practice Exercises
Worked answers to every 'Practice Exercises' box in this workbook. Try each yourself first, then check here.
Where several answers are valid, one good approach is shown.

Section 1 — Vim
1a. Create ~/.vimrc and confirm behaviour
cp /dev/null ~/.vimrc # or: nano ~/.vimrc
printf 'set ruler\nset number\n' >> ~/.vimrc
vim testfile.txt

1. Create the file, add at least ruler and number, then open any file. The status line now shows the cursor position and
lines are numbered. Add the rest of the 1.2 settings the same way.

1b. Practice delete/copy/paste
vim scratch.txt
# in Normal mode: dw (word) dd (line) dap (paragraph)
# yy then p to copy a line and paste below

1. Open a throwaway file, enter some lines, press Esc to be sure you are in Normal mode, then try each verb. yy copies
the current line and p pastes it after the cursor.

1c. Toggle line numbers
:set number
:set relativenumber
:set nonumber

1. :set number shows absolute numbers, relativenumber shows distance from the cursor (handy with counts like 5j), and
nonumber turns them off.

Section 2 — Files & Directories
2a. Build the tree, swap two files





mkdir -p ~/tmp/some/dir1 ~/tmp/some/dir2
touch ~/tmp/some/dir1/a.txt ~/tmp/some/dir2/b.txt
mv ~/tmp/some/dir1/a.txt ~/tmp/some/dir2/a.txt
mv ~/tmp/some/dir2/b.txt ~/tmp/some/dir1/b.txt
ls -R ~/tmp/some

1. Create the structure, then move each file into the other directory. ls -R confirms the swap. Do one mv at a time and
re-list to stay oriented.

2b. An extra cp option
cp --backup=numbered file dest/

1. --backup keeps a numbered copy (file.~1~) instead of silently overwriting an existing destination. Useful when you
want to overwrite but keep the old version just in case.

2c. Compare cp -r and cp -a on timestamps
cp -r ~/tmp ~/tmp.r
cp -a ~/tmp ~/tmp.a
ls -l ~/tmp ~/tmp.r ~/tmp.a

1. cp -r may reset modification times to now; cp -a preserves the originals along with permissions and ownership.
Compare the ls -l times to see the difference.

Section 3 — File Globbing
3a. Create test files and predict results
touch A1.txt b2.log C3.JPG d4d.md 'weird name.txt'
ls [A-Z]* # A1.txt C3.JPG
ls *[0-9]*.log # b2.log
ls *.??? # A1.txt b2.log d4d.md (3-char ext)
ls *.[jJ][pP][gG] # C3.JPG

1. Make the files, then run each glob and compare to the predictions in the comments. Predicting first, then verifying, is
how glob intuition forms.

3b. Four characters plus any extension
ls ????.*

1. Four ? match exactly four name characters, the dot is literal, and * matches any extension. So it matches abcd.txt but
not abc.txt.

3c. Why 3.5 needs grep
ls | grep -E '[^A-Za-z0-9_.-]'

1. A glob can say 'one character not in this set' at a fixed position, but it cannot scan a whole variable-length name for
ANY disallowed character. grep with a negated class and -E does that across the entire name.





Section 4 — Redirection
4a. Predict and verify 4.3 and 4.6
echo 2 2>2 ; ls -l 2 ; cat 2 # file '2' exists but empty
: > ls ; ls < ls > ls ; cat ls # listing went into file 'ls'

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

1. The shell feeds the three lines to cat as stdin until EOF; > notes.txt captures them. A clean way to write a small file
from a script.

Section 5 — Pipes
5a. Count conf files in /etc
ls /etc | grep conf | wc -l

1. ls lists /etc, grep keeps names containing conf, wc -l counts them. Each stage reads the previous stage's output —
the essence of a pipeline.

5b. Usernames from /etc/passwd
head -3 /etc/passwd | cut -d':' -f1

1. head -3 takes the first three lines, then cut splits on colon and prints field 1, the username. /etc/passwd is
colon-separated.

5c. Why cat file | ls > file is meaningless
# ls ignores stdin, so the piped data is discarded,
# and > file empties the file before ls even runs.

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

1. Create with -c, inspect with -t before extracting, then extract only tmp/dir1 by naming it. -C sets the base directory
each time.

7b. Compare gzip vs bzip2 size
tar -czf a.tgz -C ~ tmp
tar -cjf a.tbz -C ~ tmp
ls -l a.tgz a.tbz

1. Same content, two compressors. bzip2 (.tbz) is usually a bit smaller but slower to create. ls -l shows the byte
difference.

7c. Why -C matters
# -C makes archived paths relative (tmp/...),
# so extraction cannot overwrite absolute system paths
# and works safely in any target directory.

1. Relative archives are portable and safe; absolute-path archives can clobber real system locations on extraction.

Section 8 — Data Tools





8a. Last field of every line
awk '{print $NF}' file

1. $NF is the last field on each line regardless of field count, so this prints the final column throughout the file.

8b. Sorted unique extensions
ls | sed -n 's/.*\.//p' | sort -u

1. sed strips everything up to the last dot, leaving the extension; sort -u gives the unique sorted set. Files without a dot
produce no output.

8c. nl -ba vs cat -n
nl -ba file
cat -n file

1. Both number lines and both include blank lines here (nl needs -ba to do so; cat -n always does). nl offers more
formatting control such as separators and starting number.

Section 9 — Sorting
9a. Numeric column ascending then descending
sort -t',' -k2,2n data.csv
sort -t',' -k2,2nr data.csv

1. -k2,2n sorts field 2 numerically ascending; adding r reverses to descending. Restricting the key to 2,2 avoids
surprises from later fields.

9b. -k3 versus -k3,3
sort -k3 file # from field 3 to END of line
sort -k3,3 file # field 3 ONLY

1. -k3 uses field 3 through the line's end as the sort key, so later fields act as tiebreakers. -k3,3 keys on exactly field 3.
The difference shows when field 3 values tie.

9c. ls sorted by size, biggest last
ls -la | sort -k5,5n

1. Field 5 is the byte size; numeric ascending puts the largest file at the bottom. Add r to put it on top.

Section 10 — grep
10a. Count comment lines
grep -E "^#" /etc/ssh/ssh_config | wc -l

1. ^# matches lines beginning with a hash (comments); wc -l counts them. Works on any config file.





10b. Lines ending in exactly four digits
grep -E "[0-9]{4}$" file

1. [0-9]{4}$ requires four digits immediately before end of line. Add a boundary like [^0-9] before it if you must exclude
longer runs.

10c. {1} and (5|6) equivalence
grep -E "[[:digit:]]-(5|6)[[:digit:]]{3}$" data.txt

1. [56] and (5|6) both mean 'a 5 or a 6' for a single character, so they are interchangeable here. {1} is implicit for a single
item, so writing it changes nothing.

Section 11 — sed
11a. http to https, then in place
sed 's/http:/https:/g' site.conf # preview
sed -i.bak 's/http:/https:/g' site.conf # apply, keep .bak
diff site.conf.bak site.conf

1. Preview first, then -i.bak edits in place while saving a backup. diff confirms exactly what changed.

11b. Delete blank lines
sed '/^$/d' file

1. ^$ matches a line that starts and immediately ends (empty); d deletes it. Add -i to modify the file.

11c. Swap two comma fields
sed -E 's/^([^,]+),([^,]+)/\2,\1/' data.csv

1. Capture group 1 is everything up to the first comma, group 2 the next field; the replacement prints them swapped.
[^,]+ means 'one or more non-comma characters'.

Section 12 — find
12a. Files over 1 MB, listed
find ~ -type f -size +1M -exec ls -lh {} +

1. -size +1M finds files larger than a megabyte; -exec ls -lh {} + lists them with human-readable sizes, batching many
files into each ls call for speed.

12b. Files changed in the last day, counted
find ~ -type f -mtime -1 | wc -l

1. -mtime -1 means modified within the last 24 hours; piping to wc -l counts them.





12c. Combine name and size
find ~ -type f -name "*.log" -size +10k

1. Stacking conditions is an implicit AND: a match must be a file, end in .log, AND exceed 10 kilobytes. No -a is needed,
though it is allowed.

Section 13 — Shell Environment
13a. Add ~/bin to PATH permanently
mkdir -p ~/bin
echo 'export PATH="$HOME/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
printf '#!/bin/bash\necho hello\n' > ~/bin/hi
chmod +x ~/bin/hi
hi

1. Create the directory, prepend it to PATH in .bashrc, reload, then drop an executable script in ~/bin. Because ~/bin is
first in PATH, typing hi runs your script from anywhere.

13b. A custom prompt
echo "PS1='[\u@\h \w]\$ '" >> ~/.bashrc
source ~/.bashrc

1. \u user, \h host, \w directory, \$ the prompt sign. Reload with source to see it immediately. Colour codes can be
added later once the basics feel comfortable.

13c. Print PATH one entry per line
echo $PATH | tr ':' '\n'

1. tr translates each colon into a newline, so every PATH directory prints on its own line, easy to read.

Section 14 — User Commands
14a. Add the four functions
# paste _lsd _lsf _ps _lsize into ~/.bashrc, then:
source ~/.bashrc
_lsd ; _lsf ; _lsize

1. Once defined in .bashrc and reloaded, they behave like built-in commands in every new shell.

14b. _lsize_desc (largest first)
_lsize_desc() {
ls -la | sort -k5,5nr
}

1. Same as _lsize but nr reverses the numeric sort, so the largest file appears at the top.