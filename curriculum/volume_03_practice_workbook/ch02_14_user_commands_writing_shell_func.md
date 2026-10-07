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