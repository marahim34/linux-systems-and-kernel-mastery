# Grep Sed Awk Mastery Complete

GREP, SED & AWK MASTERY
The Complete, Self-Contained Guide to the Text-Processing Trio
Everything About the Three Tools That Make You Powerful on the Command Line
—
Regular Expressions, Searching, Stream Editing, and Field Processing, From First
Principles to Advanced One-Liners, With Hundreds of Real Examples

The skills that separate Linux users from Linux masters · For MD Abdur Rahim ·
2026

Linux Mastery — From User to Expert

Page 1

Contents
Part 1 — Foundations
1. The Trio — What Each Tool Is For
2. Regular Expressions — the Shared Language

Part 2 — grep (Searching)
3. grep — Fundamentals & Every Useful Flag
4. grep — Regex, Context & Real-World Searching

Part 3 — sed (Stream Editing)
5. sed — Fundamentals & Substitution
6. sed — Addresses, Commands & Advanced Editing

Part 4 — awk (Field Processing)
7. awk — Fundamentals & Fields
8. awk — Patterns, Variables & Logic
9. awk — Arrays, Functions & Real Programs

Part 5 — Mastery
10. Combining the Trio & Real DevOps One-Liners
12. sed — Real Mistakes & How to Never Repeat Them
13. awk — the $ vs Variable Rule (the One That Trips Everyone)
14. sort & wc — the Companions That Complete the Trio
15. Reference Cheat-Sheets for All Three

Linux Mastery — From User to Expert

Page 2

Part 1 — Foundations
1. The Trio — What Each Tool Is For
grep, sed, and awk are three Unix text-processing tools that work on streams of text — files, command
output, logs. They share the regular-expression language but each has a distinct job. Knowing WHICH to
reach for is the first skill.

The division of labour
Tool

Its job

Reach for it when...

grep

FIND lines matching a pattern

You want to SEARCH / filter lines

sed

EDIT a stream (substitute, delete,
insert)

You want to TRANSFORM text, esp.
find-and-replace

awk

PROCESS text by FIELDS/columns
with logic

You want COLUMNS, calculations,
or reports

A one-line taste of each
grep "ERROR" app.log # show lines containing ERROR
sed 's/ERROR/CRITICAL/' app.log # replace ERROR with CRITICAL
awk '{print $1, $4}' app.log # print the 1st and 4th columns

1. grep FINDS: it prints only the lines that contain 'ERROR'.
2. sed EDITS: it substitutes 'ERROR' with 'CRITICAL' as the text streams through.
3. awk PROCESSES FIELDS: it splits each line into columns and prints the 1st and 4th — something grep and sed
cannot do naturally.

PRO INSIGHT: The mental model that tells you which tool to use: grep answers 'which LINES match?' (searching
and filtering), sed answers 'change THIS to THAT in the stream' (editing, especially substitution), and awk answers
'do something with the COLUMNS/fields, possibly with logic and math' (structured processing and reports). They
overlap — awk can search like grep, sed can do some field work — but each is BEST at its own job. A rough rule: if
you are filtering lines, grep; if you are transforming text, sed; if you are working with columns or need programming
logic, awk. Together they handle almost any text-processing task on the command line, which is why they appear in
every serious Linux workflow, every log analysis, and every DevOps interview. Master all three and text stops being
an obstacle.

All three read from files OR from standard input (a pipe), so they chain naturally with each other and every
other command — the Unix philosophy of small tools combined via pipes (your Volume 7 knowledge).

Linux Mastery — From User to Expert

Page 3

2. Regular Expressions — the Shared Language
Regular expressions (regex) are patterns for matching text, and they are the shared foundation of all three
tools. Learn regex once and it powers grep, sed, and awk (and countless other tools and languages). This is
the highest-leverage chapter in the book.

Literal characters and metacharacters
Most characters match themselves (literals): 'cat' matches the text 'cat'. But some characters are SPECIAL
(metacharacters) with a meaning — these are the power of regex.
Metachar

Meaning

Example matches

.

Any single character

c.t matches cat, cot, c9t

*

Zero or more of the previous

ab* matches a, ab, abb, abbb

+

One or more (ERE)

ab+ matches ab, abb (not a)

?

Zero or one (ERE)

colou?r matches color, colour

^

Start of line

^The matches lines starting with The

$

End of line

end$ matches lines ending with end

[]

Any ONE character in the set

[aeiou] matches any vowel

[^ ]

Any ONE char NOT in the set

[^0-9] matches any non-digit

()

Grouping (ERE)

(ab)+ matches ab, abab

|

OR / alternation (ERE)

cat|dog matches cat or dog

\

Escape a metacharacter

\. matches a literal dot

Character classes and quantifiers
Pattern

Matches

[0-9]

Any digit

[a-z]

Any lowercase letter

[A-Za-z0-9]

Any letter or digit

[[:digit:]]

Any digit (POSIX class)

[[:alpha:]]

Any letter (POSIX class)

[[:space:]]

Any whitespace

{n}

Exactly n times: a{3} = aaa

{n,m}

Between n and m times: a{2,4}

{n,}

n or more times

BRE vs ERE — the crucial distinction
Linux Mastery — From User to Expert

Page 4

There are two regex flavours, and confusing them is the #1 source of frustration:
BRE (Basic)

ERE (Extended)

Used by

grep, sed (default)

grep -E, sed -E, awk

+?|(){}

Must be ESCAPED: \+ \? \|

Work directly: + ? |

Example

grep 'ab\+' or grep -E 'ab+'

grep -E 'ab+'

PRO INSIGHT: Regex is the single most valuable skill in this book because it transfers everywhere — grep, sed,
awk, your code editor, Python, JavaScript, and virtually every tool that touches text. The core concepts: LITERALS
match themselves, METACHARACTERS (. * + ? ^ $ [ ] etc.) have special powers, CHARACTER CLASSES [ ]
match one-of-a-set, ANCHORS (^ $) tie matches to line start/end, and QUANTIFIERS (* + ? { }) control repetition.
The one gotcha that catches everyone: BRE vs ERE. In BASIC regex (grep and sed by default), the characters + ? |
( ) { } are LITERAL and must be escaped with backslash to get their special meaning. In EXTENDED regex (grep
-E, sed -E, awk), they work directly. When a pattern 'should work but doesn't', it is almost always a BRE/ERE
mismatch — the fix is usually adding -E (or escaping). Learn regex deeply here and the three tools become easy;
they are mostly just regex plus a little glue.

WARNING: The most common regex frustration: you write 'grep 'a+b'' expecting + to mean 'one or more', but in
BASIC regex (grep's default) + is a LITERAL plus sign, so it matches the text 'a+b', not 'aab'. Either escape it ('grep
'a\+b'') or, far better, use EXTENDED regex with -E ('grep -E 'a+b''). The modern habit: use 'grep -E' by default so +,
?, |, (), {} all work as you expect from other languages. This single confusion — why doesn't my +, ?, or | work in
grep/sed? — is solved by remembering they need -E (ERE) or escaping in the default BRE.

TIP: TRY IT: Test regex safely with grep and echo: 'echo "color colour" | grep -oE "colou?r"' — the -o shows only
matches, -E enables +/?/|. Change the pattern and re-run to build intuition. This echo-into-grep loop is the fastest
way to learn regex without touching real files.

Linux Mastery — From User to Expert

Page 5

Part 2 — grep (Searching)
3. grep — Fundamentals & Every Useful Flag
grep (Global Regular Expression Print) searches text and prints lines that MATCH a pattern. It is the tool you
reach for constantly — finding errors in logs, locating text in code, filtering command output.

Basic usage
grep "pattern" file.txt # lines containing pattern
grep "pattern" file1 file2 # search multiple files
grep "pattern" *.log # search all .log files
command | grep "pattern" # filter another command's output
grep -r "pattern" /path/ # search recursively in a directory

1. The basic form: print every line in file.txt containing 'pattern'.
2. Search several files — grep prefixes matches with the filename.
3. Wildcards work — search every .log file.
4. grep as a FILTER on a pipe — extremely common (e.g. 'ps aux | grep nginx').
5. -r searches recursively through a whole directory tree.

Every flag worth knowing
Flag

What it does

-i

Case-INSENSITIVE match

-v

INVERT — show lines that do NOT match

-r / -R

Recursive (search directories)

-n

Show line NUMBERS

-c

COUNT matching lines (not print them)

-l

List only FILENAMES with matches

-L

List filenames with NO matches

-w

Match whole WORDS only

-x

Match whole LINES only

-o

Print ONLY the matched part, not the whole line

-E

Extended regex (+ ? | ( ) work directly)

-F

Fixed strings (no regex — literal, fast)

-A n

Show n lines AFTER each match

-B n

Show n lines BEFORE each match

-C n

Show n lines of CONTEXT around each match

--color

Highlight matches

Linux Mastery — From User to Expert

Page 6

Flag

What it does

-q

Quiet — no output, just exit status (for scripts)

-e

Multiple patterns: -e p1 -e p2

PRO INSIGHT: A handful of grep flags cover most real use, and they cluster by purpose. SEARCH CONTROL: -i
(ignore case), -w (whole words), -v (invert — 'show what does NOT match', hugely useful), -E (extended regex).
OUTPUT CONTROL: -n (line numbers), -c (count), -l (just filenames), -o (only the match). CONTEXT: -A/-B/-C
(lines after/before/around a match — essential for logs, where you want the lines surrounding an error). SCOPE: -r
(recursive). SCRIPTING: -q (quiet, for use in if-statements). The combination you will type most: 'grep -rn pattern .'
(recursive, with line numbers, from here) for searching code, and 'grep -i -C3 error log' (case-insensitive, 3 lines of
context) for logs. Learn these and grep becomes second nature.

WARNING: Remember from Chapter 2: -i means case-INSENSITIVE in grep, but the SAME letter means
'interactive' in rm/cp. And grep's default is BASIC regex, so +, ?, |, () need -E to work as expected. Two more traps:
grep treats its pattern as regex by default, so searching for a literal string with special characters (like an IP
'192.168.1.1' where . is 'any char', or a path with slashes) can match more than you intend — use -F (fixed strings)
for a literal search. And 'grep pattern' with no file just waits for keyboard input (reading stdin) — people think it
'hung'; it is waiting for you to type or pipe input.

TIP: TRY IT: Find how many times each log level appears: 'grep -c ERROR app.log', 'grep -c WARN app.log'. Then
see errors with context: 'grep -B2 -A2 ERROR app.log' shows two lines on each side. Then find files containing a
secret you must not commit: 'grep -rl "API_KEY" .' lists them. These three patterns — count, context, locate — are
daily grep.

Linux Mastery — From User to Expert

Page 7

4. grep — Regex, Context & Real-World Searching
Now grep with real regex power and the patterns you will actually use in DevOps work.

Practical regex searches
grep -E "error|warning|critical" log # any of several words
grep -E "^[0-9]{3}-[0-9]{4}" file # lines starting with 123-4567
grep -oE "[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+" log # extract IP addresses
grep -E "^#" config # comment lines (start with #)
grep -Ev "^#|^$" config # NON-comment, NON-blank lines
grep -iE "fail(ed|ure)?" log # fail, failed, failure

1. -E with | matches ANY of several patterns — one search, multiple terms.
2. Anchored pattern with quantifier — lines starting with a phone-like number.
3. -oE extracts just the IP addresses from a log (the -o prints only the match). Note . is escaped to mean a literal dot.
4. Find comment lines (starting with #).
5. The powerful cleanup idiom: -v inverts, and '^#|^$' matches comments OR blank lines, so this shows only the REAL
config lines. Used constantly.
6. Optional groups: matches fail, failed, or failure.

Worked example — analysing a web server log
You have an access log and want insight. Count total errors: 'grep -c " 500 " access.log'. See all 404s with
the requested URL: 'grep " 404 " access.log'. Extract every unique IP that hit the server: 'grep -oE "^[0-9.]+"
access.log | sort -u'. Find requests from a specific IP: 'grep "^192.168.1.50" access.log'. Show errors with
surrounding context: 'grep -C2 "500" access.log'. This is real log analysis — grep filters and extracts, and
piping to sort/uniq (next) turns it into a report. These patterns handle a huge share of day-to-day operational
investigation.

Combining grep with sort and uniq (a preview of power)
grep -oE "[0-9.]+" access.log | sort | uniq -c | sort -rn
# extract IPs -> sort -> count duplicates -> sort by count (top talkers)

1. A classic pipeline: grep EXTRACTS the IPs, sort groups them, 'uniq -c' counts each unique one, and 'sort -rn' ranks
by count — instantly showing which IPs hit your server most. grep starts the pipeline; the Unix toolchain finishes it. This
'extract | sort | uniq -c | sort -rn' pattern is one of the most useful in all of Linux.

PRO INSIGHT: Real grep mastery is grep PLUS the pipeline. grep's job is to FIND and EXTRACT (especially with
-o to pull out just the matching text — IPs, error codes, timestamps), and then you pipe to sort, uniq -c, wc -l, and
friends to turn matches into reports. The two idioms to burn into memory: 'grep -Ev "^#|^$" config' (show only real
config lines, hiding comments and blanks — you will use this on every config file), and 'grep -oE PATTERN file | sort
| uniq -c | sort -rn' (extract, count, and rank — the instant 'top offenders' report for IPs, errors, or anything). grep
rarely works alone; it is the first stage that feeds the Unix toolchain. This is why grep is so central: it is the gateway
from raw text to structured insight.

TIP: TRY IT: Clean up a config file view: 'grep -Ev "^#|^$" /etc/ssh/sshd_config' shows only the ACTIVE settings,
hiding all the comment clutter. Try it on any config file — it instantly reveals what is actually configured. This one
command changes how you read config files forever.

Linux Mastery — From User to Expert

Page 8

Part 3 — sed (Stream Editing)
5. sed — Fundamentals & Substitution
sed (Stream EDitor) transforms text as it flows through — it reads line by line, applies your editing
commands, and outputs the result. Its most common use by far is SUBSTITUTION (find-and-replace), but it
can delete, insert, and much more.

The substitution command — sed's bread and butter
sed 's/old/new/' file # replace FIRST 'old' per line with 'new'
sed 's/old/new/g' file # replace ALL (global) on each line
sed 's/old/new/2' file # replace the 2nd occurrence per line
sed 's/old/new/gi' file # global + case-insensitive
sed 's/old/new/3g' file # from the 3rd occurrence onward

1. The s command: s/PATTERN/REPLACEMENT/. Without a flag, it replaces only the FIRST match on each line.
2. The g flag = GLOBAL: replace EVERY occurrence on each line, not just the first. The most common flag.
3. A number replaces only the Nth occurrence.
4. Flags combine: g (all) + i (case-insensitive).
5. A number plus g: replace from the Nth occurrence to the end of the line.

WARNING: By default 'sed s/old/new/' replaces only the FIRST occurrence on each line — beginners expect it to
replace all and are confused when duplicates remain. Add the 'g' flag ('s/old/new/g') to replace ALL occurrences.
This first-vs-all default is the single most common sed surprise. Remember: no g = first only; g = all.

In-place editing — changing the actual file
sed 's/old/new/g' file # prints result, file UNCHANGED
sed -i 's/old/new/g' file # EDITS THE FILE directly (careful!)
sed -i.bak 's/old/new/g' file # edits file, keeps file.bak backup

1. By default sed prints to the screen and does NOT change the file — safe for testing.
2. -i (in-place) actually MODIFIES the file. Powerful but irreversible — test WITHOUT -i first.
3. -i.bak makes the edit but saves the original as file.bak — the safe way to edit in place. Always use a backup suffix
when editing important files.

WARNING: 'sed -i' modifies the file PERMANENTLY with no undo — a wrong pattern can corrupt a config file
instantly. ALWAYS test your sed command WITHOUT -i first (see the output, confirm it is right), THEN add -i. And
when editing important files, use '-i.bak' to keep a backup. Also note: -i means 'in-place' in sed, but 'interactive' in
rm/cp and 'case-insensitive' in grep — the same letter, three different meanings (the flags-decoder lesson). A
rushed 'sed -i' on a production config with a bad regex is a classic self-inflicted outage.

Using different delimiters

Linux Mastery — From User to Expert

Page 9

sed 's/old/new/g' file # / is the usual delimiter
sed 's|/usr/local|/opt|g' file # use | when the text has slashes
sed 's#/path/one#/path/two#g' file # or # — any char works

1. The / is the traditional delimiter.
2. But if your pattern contains slashes (like file paths), using / forces ugly escaping. Instead, use a DIFFERENT delimiter
like |...
3. ...or #, or any character. sed uses whatever character follows 's' as the delimiter. This trick makes path substitutions
readable instead of a mess of backslashes.

PRO INSIGHT: sed's substitution 's/pattern/replacement/flags' is the command you will use 90% of the time, and
mastering its details makes you fast. Key points: the 'g' flag replaces ALL matches per line (without it, only the first);
'-i' edits the file in place (test without it first, and use '-i.bak' for a backup); and you can swap the '/' delimiter for '|' or
'#' when your text contains slashes (essential for editing file paths cleanly). The pattern is a regex (BASIC by default
— use 'sed -E' for extended, so +/?/| work directly). The workflow that keeps you safe and effective: write the
substitution, run it WITHOUT -i to see the result, confirm it is correct, then add -i (with .bak) to apply it. This 'preview
then apply' habit prevents the corrupted-file disasters that catch careless users.

TIP: TRY IT: Safely preview an edit: 'sed "s/localhost/127.0.0.1/g" config.txt' shows what WOULD change, file
untouched. Happy with it? Add -i.bak to apply: 'sed -i.bak "s/localhost/127.0.0.1/g" config.txt'. The .bak file lets you
undo with 'mv config.txt.bak config.txt'. This preview-then-apply-with-backup flow is how professionals use sed on
real files.

Linux Mastery — From User to Expert

Page 10

6. sed — Addresses, Commands & Advanced Editing
sed does far more than substitute. ADDRESSES target specific lines, and other COMMANDS delete, insert,
print, and transform. This chapter unlocks sed's full power.

Addresses — targeting specific lines
sed '3s/old/new/' file # only on line 3
sed '1,5s/old/new/g' file # only on lines 1-5
sed '/ERROR/s/old/new/g' file # only on lines matching /ERROR/
sed '$s/old/new/' file # only on the LAST line
sed '2,$d' file # delete from line 2 to the end

1. A number before s targets ONE line — substitute only on line 3.
2. A range 'start,end' targets a span of lines.
3. A /regex/ address targets only lines MATCHING that regex — 'on lines containing ERROR, do the substitution'. Very
powerful.
4. $ means the last line.
5. Addresses work with any command — here 'd' (delete) from line 2 to the end.

The other essential commands
Command

What it does

Example

s

Substitute

sed 's/a/b/g'

d

Delete matching lines

sed '/^#/d' (delete comments)

p

Print (with -n, print only matches)

sed -n '/error/p'

a

Append a line AFTER

sed '/pattern/a new line'

i

Insert a line BEFORE

sed '/pattern/i new line'

c

Change (replace) the line

sed '/pattern/c new line'

y

Transliterate characters

sed 'y/abc/xyz/'

q

Quit after a line

sed '10q' (first 10 lines)

Powerful practical examples

Linux Mastery — From User to Expert

Page 11

sed '/^#/d' config # delete all comment lines
sed '/^$/d' file # delete all blank lines
sed -n '/ERROR/p' app.log # print ONLY error lines (like grep)
sed -n '10,20p' file # print lines 10-20 only
sed '/^#/d; /^$/d' config # multiple commands: no comments/blanks
sed 's/ */ /g' file # squeeze multiple spaces to one

1. Delete comment lines (those starting with #) — cleaning a config.
2. Delete blank lines.
3. With -n (suppress auto-print) and p, sed prints only matching lines — behaving like grep.
4. -n with a range and p prints just those lines — extract a section.
5. Chain commands with ; — here removing both comments AND blanks in one pass.
6. Squeeze runs of spaces into single spaces — a common cleanup.

Back-references — reusing matched text
sed -E 's/([0-9]+)-([0-9]+)/\2-\1/' file # swap two numbers
sed -E 's/(.*)/[\1]/' file # wrap each line in brackets
sed 's/\(.*\):.*/\1/' /etc/passwd # keep text before first colon

1. Parentheses CAPTURE groups; \1, \2 refer back to them in the replacement. Here it swaps 'A-B' into 'B-A'. (-E for
extended regex so () work without escaping.)
2. \1 is the whole matched line, wrapped in brackets.
3. In BASIC regex the groups need escaping \(...\). This extracts the username (text before the first colon) from each
passwd line. Back-references are how you REARRANGE text, not just replace it.

PRO INSIGHT: sed's full power comes from ADDRESSES + COMMANDS + BACK-REFERENCES. Addresses
target WHERE to act — a line number, a range (1,5), the last line ($), or a regex (/ERROR/) so you edit only
matching lines. Commands do WHAT — s (substitute), d (delete), p (print, with -n to show only matches), a/i/c
(append/insert/change lines). Back-references (\1, \2 from captured groups) let you REARRANGE text, reusing
matched pieces in the replacement — swapping fields, extracting parts, reformatting. Combining these, sed
becomes a precise text surgeon: 'delete every comment line' (/^#/d), 'print only the error lines' (-n /error/p), 'extract
usernames from passwd' (back-reference before the colon), 'reformat dates' (back-references). This is why sed is
indispensable for automated, scriptable text transformation — it does in one line what would take a loop in most
languages.

TIP: TRY IT: Extract all usernames from your system: 'sed 's/\(.*\):.*/\1/' /etc/passwd' takes each line's text before
the first colon. Or clean a config to its essence: 'sed '/^#/d; /^$/d' /etc/ssh/sshd_config' removes comments and
blanks in one pass (compare to the grep -Ev version — sed and grep can both do this, different styles).

Linux Mastery — From User to Expert

Page 12

Part 4 — awk (Field Processing)
7. awk — Fundamentals & Fields
awk is the most powerful of the three — a complete text-processing LANGUAGE. Its speciality is working
with FIELDS (columns): it automatically splits each line into fields and lets you process them with full
programming logic. If your data has columns, awk is the tool.

The awk model — fields and records
awk reads input line by line (each line is a RECORD), and automatically splits each line into FIELDS by
whitespace. The fields are named $1, $2, $3... and $0 is the whole line. This automatic field-splitting is awk's
superpower.
awk '{print $1}' file # print the 1st field of every line
awk '{print $3}' file # the 3rd field
awk '{print $NF}' file # the LAST field (NF = number of fields)
awk '{print $0}' file # the whole line
awk '{print $1, $3}' file # fields 1 and 3, space-separated
awk '{print $1 $3}' file # fields 1 and 3, NO separator (joined)

1. $1 is the first whitespace-separated field (column) of each line.
2. $3 is the third field.
3. $NF is the LAST field — NF is a built-in variable holding the field COUNT, so $NF means 'the last one'. Extremely
useful.
4. $0 is the entire line.
5. A COMMA between fields inserts the output separator (a space) — '$1, $3' prints them spaced.
6. NO comma concatenates them directly — '$1 $3' joins with nothing between. This comma-or-not distinction matters.

The structure of an awk program
awk 'pattern { action }' file
awk '{ print $1 }' file # no pattern: action runs on EVERY line
awk '/ERROR/ { print $0 }' file # pattern: action runs on matching lines
awk '$3 > 100 { print $1 }' file # condition: lines where field 3 > 100

1. An awk program is PATTERN { ACTION }: for each line, IF the pattern matches, DO the action.
2. No pattern means 'every line' — here print field 1 of all lines.
3. A /regex/ pattern runs the action only on matching lines (like grep, but then you can process fields).
4. The pattern can be a CONDITION on fields — 'where the 3rd field exceeds 100, print the 1st'. This is where awk
surpasses grep and sed: it makes DECISIONS based on column values.

Changing the field separator

Linux Mastery — From User to Expert

Page 13

awk -F: '{print $1}' /etc/passwd # split on COLON, print username
awk -F, '{print $2}' data.csv # split on comma (CSV)
awk -F'\t' '{print $1}' file # split on TAB
awk 'BEGIN{FS=":"} {print $1}' file # set separator via FS variable

1. -F sets the field separator — here a colon, so /etc/passwd (colon-separated) splits correctly and $1 is the username.
2. -F, handles CSV files — split on commas.
3. -F with a tab for tab-separated data.
4. You can also set FS (Field Separator) in a BEGIN block — equivalent to -F. Use whichever reads clearer.

PRO INSIGHT: awk's defining feature is automatic FIELD SPLITTING: every line is broken into columns ($1, $2, ...
$NF for the last), and you process them with a PATTERN { ACTION } model — for each line, if the pattern matches,
run the action. This is why awk beats grep and sed for COLUMNAR data: it can print specific columns ($1, $3),
make decisions based on column VALUES ($3 > 100), and reformat by rearranging fields. The essentials: $1..$NF
are the fields, $0 is the whole line, NF is the field count, -F sets the separator (colon for /etc/passwd, comma for
CSV). The moment your data has columns — logs, CSVs, command output, /etc/passwd — awk is the right tool.
'awk '{print $1}'' to grab a column, 'awk '$3>100'' to filter by a column's value, 'awk -F: '{print $1}'' to handle custom
separators: these three patterns already make you productive.

TIP: TRY IT: Print all usernames from /etc/passwd (colon-separated): 'awk -F: '{print $1}' /etc/passwd'. Print the last
field of each line in any file: 'awk '{print $NF}' file'. From 'ls -l', print just filenames (the last field): 'ls -l | awk '{print
$NF}''. Feel how awk grabs columns effortlessly — something grep and sed cannot do naturally.

Linux Mastery — From User to Expert

Page 14

8. awk — Patterns, Variables & Logic
awk is a real programming language. This chapter adds conditions, built-in variables, arithmetic, and control
flow — turning awk from a column-printer into a data-processing engine.

Built-in variables
Variable

Meaning

$1, $2...

The fields (columns)

$0

The entire current line

NF

Number of Fields in the current line

NR

Number of the current Record (line number, running)

FNR

Line number within the CURRENT file

FS

Field Separator (input)

OFS

Output Field Separator

RS

Record Separator

ORS

Output Record Separator

Conditions and comparisons
awk 'NR > 1' file # skip the header (line 1)
awk 'NR % 2 == 0' file # even-numbered lines only
awk '$3 > 100' file # lines where field 3 exceeds 100
awk '$1 == "ERROR"' file # lines where field 1 is exactly ERROR
awk 'NF > 5' file # lines with more than 5 fields
awk '$2 ~ /error/' file # field 2 MATCHES regex /error/
awk '$2 !~ /ok/' file # field 2 does NOT match /ok/
awk 'length($0) > 80' file # lines longer than 80 characters

1. NR is the running line number; 'NR > 1' skips the first line (a header) — a constant need with CSVs.
2. Arithmetic on NR — even lines only.
3. Numeric comparison on a field.
4. String equality (note == for compare, quotes for strings).
5. Filter by field COUNT.
6. ~ tests whether a field MATCHES a regex (field-specific matching — more precise than grep).
7. !~ is 'does not match'.
8. Built-in length() function — find long lines.

The BEGIN and END blocks

Linux Mastery — From User to Expert

Page 15

awk 'BEGIN {print "Report:"} {print $1} END {print "Done"}' file
awk '{sum += $1} END {print sum}' file # total a column
awk '{sum += $3} END {print sum/NR}' file # average a column
awk 'END {print NR}' file # count lines (like wc -l)

1. BEGIN runs ONCE before any input (setup, headers); END runs ONCE after all input (summaries, totals). The main
block runs per line.
2. The classic awk power move: accumulate a running SUM of column 1, then print the total in END. awk does math
grep/sed cannot.
3. Sum divided by line count = AVERAGE. Real calculation on your data.
4. In END, NR holds the total line count — awk as a line counter.

PRO INSIGHT: awk becomes a data engine with three additions: BUILT-IN VARIABLES (NR = current line number,
NF = field count, FS/OFS = separators), CONDITIONS (numeric $3 > 100, string $1 == "X", regex $2 ~ /re/, all
field-specific), and the BEGIN/END blocks (BEGIN for setup before input, END for summaries after — where totals
and averages are printed). The killer capability grep and sed lack: awk does ARITHMETIC and AGGREGATION.
'{sum += $1} END {print sum}' totals a column; add '/NR' for an average; count with END{print NR}. Combined with
per-field regex matching ($2 ~ /error/, more precise than grep's whole-line match) and NR-based line selection (skip
headers with NR>1), awk handles reporting tasks that would need a full script in other languages. This is why awk is
the heavyweight of the trio — it is a complete language optimised for tabular text.

Worked example — summing and reporting from a log
You have a log where field 5 is a response size in bytes. Total bytes served: 'awk '{total += $5} END {print
total}' access.log'. Average response size: 'awk '{total += $5} END {print total/NR}' access.log'. Largest
response: 'awk '$5 > max {max = $5} END {print max}' access.log'. Bytes served only for successful (200)
requests, if status is field 6: 'awk '$6 == 200 {sum += $5} END {print sum}' access.log'. Each is a one-line
report that would take a loop and accumulator variables in most languages. This aggregation power — sum,
average, max, conditional totals, straight from columns — is exactly why awk is beloved for log and data
analysis.

Linux Mastery — From User to Expert

Page 16

9. awk — Arrays, Functions & Real Programs
The final awk chapter: arrays (for grouping and counting), built-in functions, control flow, and writing real
multi-line awk programs. This is awk at full power.

Arrays — counting and grouping
awk '{count[$1]++} END {for (k in count) print k, count[k]}' file
awk '{sum[$1] += $2} END {for (k in sum) print k, sum[k]}' file

1. The single most useful awk pattern: 'count[$1]++' uses field 1 as an array KEY and increments its counter — so you
count occurrences of each unique value. The END loop prints each key and its count. This is 'group by and count' in one
line — like a database GROUP BY.
2. 'sum[$1] += $2' groups by field 1 and SUMS field 2 for each group — 'total sales per region', 'bytes per IP'. Grouping
plus aggregation, the heart of data analysis, in one line.

Worked example — count requests per IP from a log
The classic real task: which IPs hit your server most? 'awk '{count[$1]++} END {for (ip in count) print
count[ip], ip}' access.log | sort -rn | head'. awk groups by IP (field 1) and counts each, END prints count and
IP, then sort -rn ranks them and head shows the top. This replaces the grep|sort|uniq -c pipeline from earlier
with pure awk — and it is more flexible because you can add conditions (count only errors: add '$9==500' as
a pattern). The 'array[key]++ then loop in END' pattern is the awk technique that handles a huge share of real
log and data analysis. Master this one pattern above all.

Control flow and functions
awk '{ if ($3 > 90) print $1, "HIGH"; else print $1, "ok" }' file
awk '{ for (i=1; i<=NF; i++) total += $i } END {print total}' file
awk '{ print toupper($1), length($2) }' file
awk '{ gsub(/error/, "ERROR"); print }' file

1. Full if/else logic — categorise each line by a field's value.
2. A for loop over ALL fields (1 to NF) — here summing every number on every line.
3. Built-in functions: toupper() uppercases, length() gives string length.
4. gsub() is global substitution WITHIN awk (like sed's s///g) — replace all 'error' with 'ERROR' in each line, then print.
awk can do sed's job too when you are already in awk.

Useful awk built-in functions
Function

Does

length(s)

Length of string s (or $0)

substr(s,i,n)

Substring of s from position i, n chars

index(s,t)

Position of t in s

split(s,arr,sep)

Split s into array arr by sep

toupper/tolower(s)

Change case

gsub(re,repl)

Global substitute in $0 (or given field)

Linux Mastery — From User to Expert

Page 17

Function

Does

sub(re,repl)

Substitute first match

printf(fmt,...)

Formatted output (like C)

A real multi-line awk program
awk '
BEGIN { print "=== Log Summary ===" }
/ERROR/ { errors++ }
/WARN/ { warns++ }
{ total++ }
END {
print "Total lines:", total
print "Errors:", errors
print "Warnings:", warns
printf "Error rate: %.1f%%\n", errors/total*100
}' app.log

1. A full awk program (readable across lines). BEGIN prints a header.
2. Count ERROR lines...
3. ...and WARN lines...
4. ...and all lines.
5. END prints a formatted report with a calculated error-rate percentage (printf for formatting). This is a complete, useful
log-analysis program in a few lines — the kind of thing awk excels at and that would be far longer in most languages.

PRO INSIGHT: awk arrays are the feature that elevates it from a column tool to a data-analysis language. The
pattern 'array[$key]++' (count per key) and 'array[$key] += $value' (sum per key), followed by a 'for (k in array)' loop
in END, gives you GROUP-BY-and-aggregate — counting requests per IP, summing bytes per user, tallying errors
per service — in a single line, no database needed. Add control flow (if/else, for loops), string functions (substr,
split, gsub, toupper), and printf formatting, and awk writes complete reports. The multi-line program form (with
BEGIN, per-pattern blocks, and END) is genuinely a small program. For a DevOps engineer analysing logs, this
awk power is transformative: questions that seem to need a script or a spreadsheet become one-liners. Learn the
array-counting pattern first; it alone justifies learning awk.

Linux Mastery — From User to Expert

Page 18

Part 5 — Mastery
10. Combining the Trio & Real DevOps One-Liners
The three tools shine together, piped into each other and with the wider Unix toolkit. Here are real one-liners
you will actually use.

Real-world pipelines
# Top 10 IPs hitting a web server
grep -oE "^[0-9.]+" access.log | sort | uniq -c | sort -rn | head
# Count errors by type in a log
grep ERROR app.log | awk '{print $5}' | sort | uniq -c | sort -rn
# Extract and total response sizes for 200 responses
awk '$9 == 200 {sum += $10} END {print sum}' access.log
# Show active config (no comments/blanks) then substitute a value
grep -Ev "^#|^$" config | sed 's/port 8080/port 9090/'
# Find failed SSH logins and the offending IPs
grep "Failed password" /var/log/auth.log | awk '{print $(NF-3)}' | sort | uniq -c | sort
-rn
# Replace a string across many files
grep -rl "oldname" . | xargs sed -i.bak 's/oldname/newname/g'

1. grep extracts IPs, the sort/uniq/sort/head chain ranks the top 10 — the classic top-talkers report.
2. grep filters to errors, awk pulls the error-type field, then count and rank — error breakdown.
3. Pure awk: sum column 10 only where column 9 is 200 — conditional aggregation.
4. grep cleans the config to real settings, sed makes an edit — the tools chained.
5. grep finds failed logins, awk extracts the IP field (counting back from the end with NF-3), then rank — a security
report of attackers.
6. grep -rl LISTS files containing the string, xargs feeds them to sed for an in-place replace across all of them — mass
find-and-replace across a codebase.

PRO INSIGHT: The trio's real power is COMBINATION — each does its job and pipes to the next, plus the wider
toolkit (sort, uniq, head, xargs). The division holds even in pipelines: grep FILTERS/EXTRACTS the relevant lines
or fields, sed TRANSFORMS text (substitutions, cleanup), and awk PROCESSES FIELDS and AGGREGATES
(counts, sums, reports). The two patterns that recur endlessly: 'grep ... | sort | uniq -c | sort -rn' (extract, count, rank
— top offenders of anything) and 'grep -rl STRING . | xargs sed -i STRING-REPLACE' (find files containing
something, edit them all). For a DevOps engineer, these pipelines ARE daily work — analysing logs, auditing
configs, mass-editing code, investigating security events. You do not need to memorise them; you need to
understand each tool well enough to BUILD the pipeline you need. That fluency — reaching for grep, sed, or awk
and chaining them by instinct — is the mark of someone who commands Linux rather than merely uses it.

Linux Mastery — From User to Expert

Page 19

TIP: TRY IT: Build a security report from your auth log (if accessible): 'grep "Failed password" /var/log/auth.log |
awk '{print $(NF-3)}' | sort | uniq -c | sort -rn' shows which IPs are attacking your SSH, ranked. This one pipeline —
grep to find, awk to extract the IP, sort/uniq/sort to rank — is real operational security work, and it uses all your new
skills together.

Linux Mastery — From User to Expert

Page 20

12. sed — Real Mistakes & How to Never Repeat
Them
These are the actual errors people hit when learning sed — drawn from real terminal sessions. Each one
taught a lasting lesson. Study them and you will skip the painful trial-and-error, because you will recognise
the mistake before you make it.

The Golden Rules of sed (memorise these first)
Rule

Why it matters

Always include the closing /

s/old/new WITHOUT the final / is 'unterminated s
command'

No space after s

's /old/new/' is invalid — the space breaks it

Test WITHOUT -i first, then add -i

sed without -i only PREVIEWS; -i makes permanent
changes

g replaces all; without g, first-per-line only

The #1 'why didn't it change everything?' surprise

Make a backup: -i.bak

One bad regex can corrupt a file with no undo

Mistake 1 — 'it printed the change but didn't save'
sed 's/INFO/INFORMATION/' file.txt # only PRINTS, file unchanged
sed -i 's/INFO/INFORMATION/g' file.txt # actually SAVES to the file
sed -i.bak 's/INFO/INFORMATION/g' file.txt # saves + keeps file.bak backup

1. The classic first confusion: sed WITHOUT -i writes the result to the screen only — the file is never modified. People
run it, see the change scroll past, then find the file untouched.
2. -i (in-place) is what actually edits the file.
3. -i.bak edits AND keeps a backup — the safe habit. The lesson: sed without -i = preview; sed -i = modify.

Mistake 2 — the 'g' flag: only the first match changed
echo "INFO INFO INFO" | sed 's/INFO/X/' # -> X INFO INFO (first only!)
echo "INFO INFO INFO" | sed 's/INFO/X/g' # -> X X X (all)

1. Without g, sed replaces only the FIRST occurrence on each line — so duplicates remain and people think sed
'missed' them.
2. The g flag (global) replaces EVERY occurrence on each line. Whenever you want all matches, remember the g.

Mistake 3 — the \b word-boundary disaster
A real, instructive failure. Trying to replace whole-word INFO but not the INFO inside INFORMATION,
someone reached for \b (word boundary) — and it went wrong twice.

Linux Mastery — From User to Expert

Page 21

# The intent: change standalone INFO, leave INFORMATION alone.
echo "SYSTEM INFORMATION" | sed 's/\bINFO/X/' # -> SYSTEM XRMATION (!!)
# \b ALSO matches the boundary at the start of INFORMATION,
# so 'INFO' inside 'INFORMATION' matched -> 'XRMATION'.
# A later typo turned \b into a literal 'b':
# s/\bINFORMATION/b\INFORMATION/ produced 'SYSTEM bINFORMATION'

1. The \b matched the boundary right before the INFO inside INFORMATION, so the replace fired where it should not
have — turning INFORMATION into XRMATION.
2. A second attempt mistyped the escaping and literally inserted a 'b', creating 'SYSTEM bINFORMATION'. Two
lessons: \b matches boundaries INSIDE words too, and \b escaping is fiddly.

WARNING: \b (word boundary) is treacherous for this kind of job because it matches the boundary at the START of
a longer word too — 'INFO' inside 'INFORMATION' has a word boundary right before it, so 's/\bINFO/X/' hits it. If
you truly want the WHOLE word INFO and nothing else, anchor BOTH sides: 's/\bINFO\b/X/' (INFO with a boundary
on each side won't match inside INFORMATION). Even better for exact known targets, match the surrounding
context you actually want: 's/\[INFO\]/[INFORMATION]/g' for '[INFO]', or 's/ INFO: / INFORMATION: /g' for 'INFO:'.
Precise, context-aware patterns beat clever \b tricks and avoid corrupting words like INFORMATION.

Mistake 4 — 'INFORMATIONRMATION' (matching inside a word)
echo "SYSTEM INFORMATION" | sed 's/INFO/INFORMATION/'
# -> SYSTEM INFORMATIONRMATION
# 'INFO' matched INSIDE 'INFORMATION' and got expanded,
# leaving the leftover 'RMATION'.

1. Replacing INFO with INFORMATION blindly also matches the INFO that BEGINS the word INFORMATION,
expanding it to INFORMATION + the leftover RMATION = INFORMATIONRMATION. The fix is the same: target the
exact pattern you mean ('[INFO]', 'INFO:', 'value="INFO"'), not the bare substring INFO that also lives inside other
words.

Mistake 5 — syntax errors that produce 'unterminated s command'
sed '58, s/\bINFO/\bINFORMATION' file # unexpected ',' — bad range
sed '58 s/\bINFO/\bINFORMATION' file # unterminated 's' — no closing /
sed '/FATAL/ s /FATAL/CRITICAL/' file # space after s — invalid
# CORRECT:
sed '58 s/\bINFO\b/INFORMATION/' file # single line, both boundaries, closed
sed '58,60 s/INFO/INFORMATION/g' file # a real range needs TWO numbers

1. '58,' has a comma but no second address — a range needs both ends (58,60).
2. Missing the closing / gives 'unterminated s command' — the single most common sed error message.
3. A space after s ('s /...') is invalid syntax.
4. The corrected forms: a single line address is just '58 s/.../.../ ', a range is '58,60 s/.../.../g', and every s command
needs its closing /.

Linux Mastery — From User to Expert

Page 22

PRO INSIGHT: Nearly every sed error a learner hits falls into a handful of categories, and recognising the error
MESSAGE tells you the fix instantly. 'unterminated s command' = you forgot the closing / (or a space after s broke
it). 'unexpected ,' = you wrote a range with only one number (58, instead of 58,60). A result that 'didn't save' = you
forgot -i. A result where 'only the first one changed' = you forgot g. A word like INFORMATION getting mangled into
INFORMATIONRMATION or XRMATION = your pattern matched INSIDE a longer word, so make it context-specific
('[INFO]', 'INFO:') or anchor both boundaries (\bINFO\b). Keep the Golden Rules in view — closing /, no space after
s, test without -i, use g for all, back up with .bak — and sed stops fighting you. These lessons come from real
sessions; internalise them and you skip the frustration entirely.

Linux Mastery — From User to Expert

Page 23

13. awk — the $ vs Variable Rule (the One That Trips
Everyone)
The single most common awk confusion, worth its own chapter: WHEN to use $ and when not to. Getting this
wrong silently prints nothing or the wrong thing. Once it clicks, a huge class of awk bugs disappears.

The Golden Rule
$ + NUMBER (or NF, or 0) -> FIELD reference (data FROM the input)
NO $ -> a VARIABLE (something YOU calculate)

1. $1, $2, $NF, $0 read VALUES from the current input line — the columns. The $ means 'the field whose number
follows'.
2. sum, count, total, arr[key] are YOUR OWN variables — no $ — holding things you compute. NR and NF are also
used WITHOUT $ (they are variables holding the line number and field count).

The mistake — $sum instead of sum
# WRONG - prints nothing:
awk -F',' 'NR>1 {sum += $5} END {print "Total: " $sum}' data
# -> Total: (blank!)
# RIGHT:
awk -F',' 'NR>1 {sum += $5} END {print "Total: " sum}' data
# -> Total: 15

1. '$sum' means 'the field NUMBERED by the value of sum'. Since sum holds something like 15, '$sum' tries to print
field 15 (which usually does not exist) — so you get nothing. This is the exact bug that stumps everyone once.
2. Dropping the $ prints the VARIABLE sum's value (the total you accumulated). The rule: your own variable, no $.

The comparison table — burn this in
What you want

Correct

Wrong

First field

$1

$one

Last field

$NF

NF (that's the field COUNT)

Entire line

$0

0 (that's the number zero)

Field number held in i

$(i)

$i (usually not what you mean)

Your sum variable

sum

$sum

Your count variable

count

$count

Line number

NR

$NR

Field count

NF

$NF is the last FIELD, not the count

Array element

arr[key]

$arr[key]

String length

length($1)

$length(...)

Linux Mastery — From User to Expert

Page 24

Two memory tricks that make it stick
Trick

How to remember

The Goldfish rule

$ = 'from the pond' (input data). No $ = 'your bucket' (your
variables).

The Wallet rule

$ = money already IN your wallet (input fields). No $ =
money you EARN/calculate (your variables).

The decision is always: is this value coming FROM the input line, or am I calculating it myself? From
the input → use $ (it is a field). Calculating it myself → no $ (it is my variable).
PRO INSIGHT: The $-vs-variable rule is the awk equivalent of a rite of passage — everyone writes '$sum' once,
sees blank output, and is baffled. The fix is a single clear principle: $ ALWAYS means 'a field from the input' ($1, $2,
$NF, $0, or $(expression) that evaluates to a field number), and everything you compute yourself — sum, count,
totals, arrays — takes NO $. The special names NR (line number) and NF (field count) are variables too, so they go
WITHOUT $ (but $NF means 'the last field', because there the $ turns the count into a field reference — a subtle,
important distinction). Anchor it with the Goldfish/Wallet trick: $ is what came from the pond/wallet (the input), no-$
is your own bucket (your calculations). Once this rule is reflexive, an entire category of silent awk bugs simply stops
happening, and you can read and write awk with confidence.

TIP: TRY IT: Prove it to yourself: 'printf "5\n10\n" | awk '{s+=$1} END{print $s}'' prints blank (because $s tries to
read a field), while '...END{print s}' prints 15. Run both back to back and the rule becomes unforgettable — the $
turned your total into a field lookup.

Linux Mastery — From User to Expert

Page 25

14. sort & wc — the Companions That Complete the
Trio
grep, sed, and awk rarely work alone — they pipe into sort (ordering) and wc (counting). These two small
tools turn matches and fields into ranked, counted reports. You have seen them in pipelines; here they are
properly.

wc — counting lines, words, characters
Command

Counts

wc -l file

Lines (the most-used option)

wc -w file

Words

wc -c file

Bytes

wc -m file

Characters

wc -L file

Length of the longest line

grep -c ERROR app.log # grep's own line count
grep ERROR app.log | wc -l # same idea via wc
awk -F, 'NR>1' data.csv | wc -l # count data rows (excluding header)
grep -o ERROR file | wc -l # count OCCURRENCES, not lines

1. grep -c already counts matching lines.
2. Piping to 'wc -l' counts lines from any command's output — universal.
3. Count real data rows by skipping the header first.
4. A key distinction: 'grep -o' prints each MATCH on its own line, so 'wc -l' then counts total occurrences (even multiple
per line), not just matching lines.

sort — ordering, and the options that matter
Option

Does

sort

Alphabetical (default)

sort -n

NUMERIC (so 10 comes after 9, not before)

sort -r

Reverse

sort -u

Unique (dedupe while sorting)

sort -k N

Sort by column N

sort -t C

Use C as the field separator

sort -h

Human-readable numbers (1K, 2M, 3G)

WARNING: The classic sort trap: the DEFAULT sort is ALPHABETICAL, so numbers sort wrong — '10' comes
BEFORE '9' because it compares character by character ('1' < '9'). For numbers you MUST use 'sort -n'. This bites
everyone ranking by count or salary: 'sort' gives 1, 10, 2, 3...; 'sort -n' gives the correct 1, 2, 3... 10. Whenever you
sort numbers, reach for -n (and -nr for numeric high-to-low).

Linux Mastery — From User to Expert

Page 26

The pattern that ties everything together
# The single most useful pipeline in Linux:
grep -oE "[0-9.]+" access.log | sort | uniq -c | sort -nr | head
# By department, count employees:
awk -F, 'NR>1 {print $4}' data.csv | sort | uniq -c | sort -nr
# Count log levels:
awk '{print $3}' app.log | sort | uniq -c | sort -nr

1. extract (grep/awk) -> sort (group identical together) -> uniq -c (count each group) -> sort -nr (rank by count) -> head
(top few). This 'extract, sort, count, rank' chain answers a huge fraction of real questions: top IPs, most common errors,
busiest endpoints, employees per department.
2. The same pattern with awk extracting a field — count per department, ranked.
3. And again for log levels. Learn this ONE pipeline shape and you can answer 'what are the most common X?' about
anything.

PRO INSIGHT: sort and wc are the small tools that COMPLETE grep/sed/awk, and one pipeline shape unifies them
all: EXTRACT the thing you care about (grep -o or awk to pull a field), sort to bring identical values together, 'uniq -c'
to count each group, then 'sort -nr' to rank by count, and 'head' for the top few. This 'extract | sort | uniq -c | sort -nr'
chain is the workhorse of log and data analysis — top talkers, most frequent errors, counts per category — and you
will type it constantly. Two things to remember: use 'sort -n' for NUMBERS (the default alphabetical sort mis-orders
them), and 'grep -o' + 'wc -l' counts occurrences while 'grep -c' counts matching lines. With grep and awk to find and
extract, sed to transform, and sort/uniq/wc to order and count, you have the complete Unix text-processing toolkit —
and the fluency to turn any pile of text into an answer.

Linux Mastery — From User to Expert

Page 27

15. Reference Cheat-Sheets for All Three
grep cheat-sheet
grep "pat" file # find lines matching pat
grep -i / -v / -r # ignore-case / invert / recursive
grep -n / -c / -l # line numbers / count / filenames
grep -o # print only the match
grep -E "a|b" / -F # extended regex / fixed string
grep -A2 -B2 -C2 # context after/before/around
grep -w / -x # whole word / whole line

1. The grep essentials on one screen — search control, output control, and context flags.

sed cheat-sheet
sed 's/old/new/' # replace first per line
sed 's/old/new/g' # replace all per line
sed -i.bak 's/o/n/g' # edit file in place, keep backup
sed -n '/pat/p' # print only matching lines
sed '/pat/d' # delete matching lines
sed '3,5s/o/n/' # substitute only on lines 3-5
sed -E 's/(.)(.)/\2\1/' # back-references (swap)
sed 's|/a|/b|' # alternate delimiter for paths

1. The sed essentials — substitution, in-place editing, line addressing, delete, print, and back-references.

awk cheat-sheet
awk '{print $1}' # first field
awk '{print $NF}' # last field
awk -F: '{print $1}' # custom separator
awk '$3 > 100' # filter by field value
awk '/re/ {print $2}' # regex pattern + action
awk '{s+=$1} END{print s}' # sum a column
awk '{c[$1]++} END{for(k in c)print k,c[k]}' # count per key
awk 'NR>1' # skip header
awk 'BEGIN{...} {...} END{...}' # setup / per-line / summary

1. The awk essentials — fields, separators, filtering, aggregation, the group-by-count pattern, and program structure.
These cover the vast majority of real awk use.

PRO INSIGHT: You now have complete, self-contained mastery of grep, sed, and awk — the regular-expression
foundation they share, grep for searching and filtering (with every useful flag), sed for stream editing and
substitution (with addresses, commands, and back-references), awk for field processing and data analysis (with
variables, logic, arrays, and functions), and the pipelines that combine all three into real DevOps power. This trio is
genuinely enough to handle almost any command-line text task without other resources, and it is tested in virtually
every Linux and DevOps interview. The path to fluency is use: next time you face a log, a config, or a CSV, reach
for these tools instead of opening an editor — grep to find, sed to change, awk to analyse. Start with the patterns
you will use daily (grep -rn, sed -i.bak s///g, awk '{print $N}' and the array-count idiom) and expand from there.
Mastering this trio is one of the highest-leverage things you can do on the command line: it makes you faster, more
capable, and visibly more expert. You now command text, not just read it.

Linux Mastery — From User to Expert

Page 28

grep finds, sed changes, awk analyses — together they make text obey you.
— End of grep, sed & awk Mastery —

Linux Mastery — From User to Expert

Page 29

