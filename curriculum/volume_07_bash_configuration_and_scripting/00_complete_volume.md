# Volume 7: Bash Configuration & Scripting

14c. mkcd — make and enter
mkcd() {
mkdir -p "$1" && cd "$1"
}

1. $1 is the first argument. mkdir -p creates the directory (and parents), and on success (&&) cd moves into it. A
daily-use convenience function.

Every answer here is a starting point, not the only route. If your working command
differs but produces the right result, you have understood it.
— End of Solutions —

LINUX MASTERY
VOLUME 7 — BASH:
CONFIGURATION & SCRIPTING
The Complete Shell Book — Startup Files, .bashrc, Aliases, Functions, the Prompt,
Environment & History, then Writing Real Programs: Variables, Loops, Conditionals,
Arguments, Error Handling & Debugging — with Worked Examples and Solutions

Everything about the shell you type into and program with · Prepared for MD Abdur
Rahim · 2026





Table of Contents — Volume 7
PART A — Configuring Your Shell
1. What Bash Is — Shell, Session & Startup
2. The Startup Files — Which Loads When (and Why It Confuses Everyone)
3. Building Your .bashrc — Aliases, Options & History
4. Functions in Your Shell — Beyond Aliases
5. The Prompt — Customising PS1
6. Environment Variables — the Complete Picture

PART B — Programming in Bash
7. Your First Scripts — Structure & Safety
8. Variables, Quoting & Expansion
9. Conditionals & Tests
10. Loops
11. Functions, Arguments & Exit Codes
12. Real-World Scripts — Input, Files & Error Handling
13. Debugging Bash & Best Practices
14. Worked Examples & Full Solutions





Part A — Configuring Your Shell
The shell is the program you type commands into. Before programming WITH it, make it comfortable to LIVE
in. Part A is about shaping your daily environment.

1. What Bash Is — Shell, Session & Startup
Shell, terminal, bash — three different things
People blur these, but they are distinct. A terminal is the window (or the console) that shows text. A shell is
the PROGRAM running inside it that reads your commands and runs them. Bash is the most common shell
(the 'Bourne Again SHell'). So: you type into a terminal, which runs a shell, which is usually bash.
echo $SHELL
bash --version
cat /etc/shells
ps -p $$

1. Your login shell's path — usually /bin/bash.
2. Which bash version you have.
3. All installed shells the system knows about.
4. $$ is the current shell's process ID; this shows which shell you are running RIGHT NOW (useful if you switched).

The distinction that controls startup: login vs interactive
Bash decides WHICH configuration files to read based on how it was started. There are two independent
questions, and the answers determine everything in Chapter 2.
Question

Yes means

Example

Is it a LOGIN shell?

Started by logging in (SSH, console)

ssh into a server

Is it INTERACTIVE?

You type commands at a prompt

Any terminal you type in

A terminal you open on your desktop is usually interactive but NOT login. An SSH connection is both login
AND interactive. A script runs in a shell that is neither. These combinations decide which startup files run,
which is the single most confusing thing about bash — and Chapter 2 makes it simple.
PRO INSIGHT: Why this matters in practice: if you put a setting in the wrong startup file, it works when you open a
local terminal but NOT over SSH, or vice versa. Almost every '.bashrc doesn't work over SSH' problem comes from
not understanding login vs interactive. Learn this distinction once and those mysteries vanish.
PRACTICE EXERCISES
1. Run echo $SHELL and ps -p $$ — confirm which shell you are in.
2. Open a terminal locally and note it is interactive but not login; SSH somewhere and note it is both.
3. Run bash --version and check whether you have bash 5.x.





2. The Startup Files — Which Loads When
The files
File

Read when

Purpose

/etc/profile

Any LOGIN shell, all users

System-wide login setup

~/.bash_profile

Your LOGIN shells

Your login setup (often just loads
.bashrc)

~/.profile

Login shells (if no .bash_profile)

Login setup, shell-neutral

~/.bashrc

Your INTERACTIVE non-login shells

Aliases, functions, prompt — 95% of
your config

/etc/bash.bashrc

Interactive shells, all users

System-wide interactive setup

~/.bash_logout

When a login shell exits

Cleanup on logout

The rule, stated simply
Interactive non-login shells (opening a terminal on your desktop) read ~/.bashrc. Login shells (SSH,
console) read ~/.bash_profile or ~/.profile, but NOT .bashrc automatically. This split is why the standard fix
exists:
# put this in ~/.bash_profile (or ~/.profile):
if [ -f ~/.bashrc ]; then
. ~/.bashrc
fi

1. In your login-shell file...
2. ...if a .bashrc exists...
3. ...SOURCE it (the dot means 'run this file's commands in the current shell'). This one block makes login shells ALSO
read .bashrc, so your settings work everywhere — over SSH and in local terminals alike.

PRO INSIGHT: The practical rule that ends all confusion: put ALL your real settings in ~/.bashrc, and make
~/.bash_profile source it with the block above. Then you have ONE file to edit, and it applies to every kind of shell.
This is what experienced users do, and it is why most people only ever touch .bashrc. Ubuntu's default .profile
already sources .bashrc for you — which is why it 'just works' there.

Applying changes without logging out
source ~/.bashrc
. ~/.bashrc
exec bash

1. After editing .bashrc, SOURCE it to apply changes to your current shell immediately.
2. The dot is a shorthand for source — identical effect.
3. Or replace your current shell with a fresh bash, which re-reads everything. Any of these avoids closing the terminal.

PRACTICE EXERCISES





1. Look at your ~/.bashrc and ~/.profile; find whether .profile already sources .bashrc.
2. Add a harmless line (echo 'bashrc loaded') to .bashrc, open a new terminal, and confirm it appears.
3. SSH to a server (or localhost) and check whether your .bashrc settings apply; if not, add the sourcing block.
4. Edit .bashrc, then apply it three ways: source, dot, exec bash.





3. Building Your .bashrc — Aliases, Options &
History
Aliases — short names for long commands
An alias replaces a typed word with a longer command. They live in .bashrc so they load in every shell. This
is the single highest-value customisation for daily comfort.
alias ll='ls -lah'
alias la='ls -A'
alias ..='cd ..'
alias ...='cd ../..'
alias grep='grep --color=auto'
alias gs='git status'
alias update='sudo apt update && sudo apt upgrade'
alias goodo='cd /mnt/d/GoOdo/GoOdo\ App'

1. The classic: ll gives a detailed listing.
2. Almost-all listing.
3. Go up one directory by typing two dots.
4. Up two directories.
5. Make grep always colour its matches — redefining a command's default via alias.
6. Git shortcut.
7. One word to update the whole system.
8. A project jump — the backslash escapes the space in the path. One word to reach GoOdo.

PRO INSIGHT: An important subtlety: aliases only do simple word-for-word replacement and cannot take
arguments in the middle. When you need to USE an argument, you need a FUNCTION (Chapter 4), not an alias.
Rule of thumb: no argument, or argument at the end only, use an alias; argument used in the middle, use a
function.

Useful shell options
shopt -s autocd
shopt -s cdspell
shopt -s checkwinsize
shopt -s globstar

1. Type a directory name alone (no cd) to enter it.
2. Auto-correct minor typos in cd paths.
3. Keep line-wrapping correct after you resize the window.
4. Enable ** to match files recursively (ls **/*.py finds all Python files at any depth).

A history setup that transforms your workflow





HISTSIZE=50000
HISTFILESIZE=100000
HISTCONTROL=ignoreboth
shopt -s histappend
HISTTIMEFORMAT="%F %T "
bind '"\e[A": history-search-backward'
bind '"\e[B": history-search-forward'

1. Remember 50,000 commands in this session...
2. ...and 100,000 on disk. Huge history is a searchable record of everything you have done.
3. ignoreboth = ignore duplicate commands AND commands starting with a space (for secrets).
4. Append to history rather than overwriting — so multiple terminals do not lose each other's history.
5. Timestamp every history entry — see WHEN you ran something.
6. Make the Up arrow search history matching what you have typed so far...
7. ...and Down arrow the reverse. Type 'ssh' then Up to cycle only past ssh commands. This one setting is
transformative.

PRO INSIGHT: The Ctrl+R companion: alongside these, pressing Ctrl+R lets you fuzzy-search your entire
command history as you type. Between a large history, the arrow-key prefix search above, and Ctrl+R, you rarely
retype a command twice. For someone running the same deploy and git commands daily, this saves hours over a
month.
PRACTICE EXERCISES
1. Add five aliases you will actually use to .bashrc; live with them for a week.
2. Enable the history settings above; then type a command prefix and press Up — watch prefix search work.
3. Turn on globstar and run ls **/*.md to find all markdown files under the current directory.
4. Add an alias that needs an argument in the middle and observe it fail — motivating Chapter 4.





4. Functions in Your Shell — Beyond Aliases
When an alias is not enough
A function is a named block of shell code that can take arguments and run multiple commands. Put
functions in .bashrc just like aliases. Use one whenever you need an argument in the middle, logic, or several
steps.
mkcd() {
mkdir -p "$1" && cd "$1"
}
extract() {
case "$1" in
*.tar.gz|*.tgz) tar -xzf "$1" ;;
*.tar.bz2) tar -xjf "$1" ;;
*.zip) unzip "$1" ;;
*.gz) gunzip "$1" ;;
*) echo "Cannot extract '$1'" ;;
esac
}
backup() {
cp "$1" "$1.$(date +%F).bak"
}

1. mkcd: make a directory AND enter it. $1 is the first argument. The && means 'cd only if mkdir succeeded'.
2. extract: one command for every archive type...
3. ...case matches the filename pattern...
4. ...and runs the right tar/unzip flags. Never memorise archive flags again.
5. backup: copy a file to a dated .bak — $(date +%F) inserts today's date. backup config.yaml makes
config.yaml.2026-07-03.bak.

PRO INSIGHT: Alias versus function decision: an alias is a nickname; a function is a small program. If you can write
it as 'replace this word with that phrase', use an alias. If you need to reference an argument like $1 in the middle,
run logic, or use multiple commands, use a function. Functions are strictly more powerful — when in doubt, write a
function.
PRACTICE EXERCISES
1. Add mkcd and extract to .bashrc; use each on a real directory and archive.
2. Write a function 'up' that takes a number N and cd's up N directories (hint: a loop, Chapter 10).
3. Write a function that greps your history for a pattern: qh() { history | grep "$1"; }.
4. Explain why extract must be a function and could not be an alias.





5. The Prompt — Customising PS1
What PS1 is
PS1 is the variable holding your prompt's format. Change it in .bashrc to show exactly the information you
want — directory, user, host, git branch, time. A good prompt gives context at a glance.
Code

Shows

Code

Shows

\u

username

\w

full current directory

\h

hostname (short)

\W

current directory
basename only

\H

hostname (full)

\$

$ for user, # for root

\t

time (24h HH:MM:SS)

\n

newline

\A

time (HH:MM)

\!

history number

\d

date

\j

number of background jobs

PS1='[\u@\h \w]\$ '
PS1='\[\e[32m\]\u@\h\[\e[0m\]:\[\e[34m\]\w\[\e[0m\]\$ '

1. A clean, informative prompt: [user@host /current/dir]$ — the standard useful layout.
2. The same with COLOUR: \e[32m starts green, \e[34m blue, \e[0m resets. The \[ \] wrappers tell bash these are
non-printing characters (crucial, or long commands wrap wrongly). Green user@host, blue directory.

PRO INSIGHT: The \[ \] wrappers around colour codes are not optional. They tell bash 'these characters take no
screen space'. Omit them and bash miscalculates the line length, causing the cursor and text to wrap and overwrite
themselves on long commands — a maddening bug with a trivial cause. Any colour code in PS1 must be wrapped
this way.

Adding the git branch
parse_git_branch() {
git branch 2>/dev/null | grep '^*' | sed 's/* //'
}
PS1='\w$(parse_git_branch)\$ '

1. A function that outputs the current git branch, or nothing if you are not in a repo (errors silenced).
2. Embed it in PS1 with $( ) so it runs each time the prompt draws. Now your prompt shows the branch whenever you
are inside a git project — invaluable for your GoOdo and eQuorum work.

PRACTICE EXERCISES
1. Set the plain [\u@\h \w]\$ prompt and confirm it shows your user, host, and directory.
2. Add colour, using \[ \] wrappers; deliberately omit them once to SEE the line-wrap bug.
3. Add the git-branch function and verify the branch appears inside a repo and vanishes outside one.
4. Design a prompt showing the time and history number.





6. Environment Variables — the Complete Picture
Shell variables versus environment variables
A shell variable exists only in the current shell. An environment variable is exported, so it is inherited by
every program the shell launches. This distinction decides whether a program you run can see your variable.
NAME="Abdur"
echo $NAME
export EDITOR="nano"
env | sort | less
printenv PATH

1. A plain shell variable — visible here...
2. ...and readable with $.
3. export makes EDITOR an ENVIRONMENT variable — now git, crontab, and other programs will use nano.
4. List ALL environment variables (the exported ones your programs inherit).
5. Print one specific environment variable.

The important ones
Variable

Controls

PATH

Where the shell looks for commands (Volume 6 Ch. 3)

HOME

Your home directory; where ~ points

EDITOR / VISUAL

Default editor for git, crontab, etc.

LANG / LC_*

Language and locale (dates, sorting, characters)

PS1

Your prompt (Chapter 5)

USER

Your username

PWD / OLDPWD

Current and previous directory

TERM

Your terminal type (affects colours)

Setting them permanently and safely





# in ~/.bashrc for interactive use:
export EDITOR="vim"
export PATH="$HOME/bin:$PATH"
# for a secret, load from a file, never hardcode:
export API_KEY="$(cat ~/.secrets/api_key)"
chmod 600 ~/.secrets/api_key

1. Persistent settings go in .bashrc (or .profile for login-wide).
2. The editor every tool will use.
3. Prepend your bin to PATH.
4. For secrets, read from a locked-down file rather than writing the value into .bashrc...
5. ...and restrict that file to yourself. Never commit secrets into a dotfile that might reach GitHub.

PRO INSIGHT: The export rule in one line: if a PROGRAM you run needs to see the variable, it must be exported; if
only the shell itself uses it, a plain variable suffices. This is exactly why DATABASE_URL and API_KEY must be
exported for your FastAPI app to read them, while a loop counter in a script needs no export. Understanding this
prevents the 'my program can't see the variable' confusion.
PRACTICE EXERCISES
1. Set a plain variable and a program that cannot see it, then export it and see the difference.
2. Set EDITOR permanently in .bashrc and confirm git uses it for a commit message.
3. Print your locale with locale; change LANG for one command and observe date output change.
4. Store a fake secret in a chmod 600 file and export it by reading the file, not hardcoding.





Part B — Programming in Bash
Now you configure the shell comfortably. Part B turns it into a programming language: automate anything,
from backups to deployments. Every concept has worked examples, and Chapter 14 solves every exercise.

7. Your First Scripts — Structure & Safety
The anatomy of a script
#!/usr/bin/env bash
set -euo pipefail
echo "Hello, this is my first script"
echo "Today is $(date +%F)"
echo "You are $USER in $PWD"

1. The SHEBANG: line 1 tells the system which interpreter runs this file. env finds bash wherever it lives.
2. The SAFETY TRIO — put this in every script: -e exit on any error, -u error on undefined variable, pipefail catch
failures inside pipes.
3. Plain output.
4. Command substitution inside a script, same as the shell.
5. Variables work identically to the interactive shell.

Making it run
chmod +x hello.sh
./hello.sh
bash hello.sh

1. Make the file executable (Volume 1 permissions) — required to run it directly.
2. Run it. The ./ says 'the script in THIS directory' (it is not in PATH).
3. Alternative: run it by passing to bash explicitly; no execute bit needed this way.

PRO INSIGHT: The safety trio 'set -euo pipefail' is the difference between amateur and professional bash. Without
it, a script whose command fails just keeps going, often making things worse (imagine a backup script that fails to
create the archive but then deletes the old one). With it, the script STOPS at the first sign of trouble. Type it at the
top of every script from now on, as a reflex.
PRACTICE EXERCISES
1. Write and run hello.sh with the shebang and safety trio; run it both ways (./ and bash).
2. Remove the execute bit and confirm ./hello.sh fails but bash hello.sh still works.
3. Add a deliberately failing command in the middle WITH and WITHOUT set -e; observe the difference.
4. Make a script print its own name and arguments (preview of Chapter 11).





8. Variables, Quoting & Expansion
The quoting rules that prevent 80% of bugs
name="Abdur Rahim"
echo "$name"
echo '$name'
echo $name
files="my file.txt"
rm "$files"
rm $files

1. Assign; NO spaces around the equals sign (bash is strict about this).
2. Double quotes: the variable EXPANDS to its value, kept as one piece.
3. Single quotes: LITERAL, no expansion — prints $name unchanged.
4. Unquoted: expands BUT splits on spaces — here bash sees two words 'Abdur' and 'Rahim'.
5. Quoted: rm sees one filename 'my file.txt'. Correct.
6. Unquoted: rm sees TWO arguments 'my' and 'file.txt' — deletes the wrong things. The classic space-in-filename
disaster.

PRO INSIGHT: The single most important bash rule: ALWAYS quote your variables — "$var", not $var. Unquoted
variables break on spaces and are the number-one source of bash bugs, from failed scripts to accidental deletions.
The only time you leave a variable unquoted is when you deliberately WANT word-splitting, which is rare. When in
doubt, add the quotes.

Parameter expansion — defaults and manipulation
echo "${name:-Guest}"
echo "${count:=0}"
echo "${file%.txt}"
echo "${file##*/}"
echo "${#name}"
echo "${path//\//-}"

1. Use $name, or 'Guest' if it is unset — providing a default.
2. Use $count, or set it to 0 if unset.
3. Strip .txt from the end — 'report.txt' becomes 'report'.
4. Strip everything up to the last slash — extracts the filename from a path.
5. The LENGTH of the string.
6. Replace every / with - in the value. These built-in manipulations avoid calling sed for simple jobs.

Command substitution and arithmetic





today=$(date +%F)
count=$(ls | wc -l)
total=$((5 + 3))
echo $((count * 2))

1. Capture a command's output into a variable.
2. Capture the file count.
3. $(( )) does integer arithmetic.
4. Arithmetic inline — no expr, no bc needed for integers.

PRACTICE EXERCISES
1. Assign a name with a space; echo it quoted and unquoted; explain the difference.
2. Use ${var:-default} to handle an unset variable gracefully.
3. Strip an extension and extract a basename using parameter expansion, not sed.
4. Compute and print the number of files times 3 using $(( )).





9. Conditionals & Tests
if and the test brackets
if [[ -f "config.yaml" ]]; then
echo "Config exists"
elif [[ -d "config/" ]]; then
echo "Config directory exists"
else
echo "No config found"
fi

1. [[ ]] is bash's test construct; -f asks 'is this a regular file?'. Always use double brackets in bash — safer than single [ ].
2. elif chains another test; -d asks 'is this a directory?'.
3. else for the fallback.
4. fi closes the if (if backwards).

The test operators worth memorising
Test

True if...

Test

True if...

-f FILE

regular file exists

-z STR

string is empty

-d DIR

directory exists

-n STR

string is non-empty

-e PATH

path exists (any type)

STR = STR

strings equal

-r / -w / -x

readable/writable/executab
le

STR != STR

strings differ

-s FILE

file exists and non-empty

N -eq M

numbers equal

A && B

both true

N -lt M

N less than M

A || B

either true

N -gt M

N greater than M

PRO INSIGHT: Two brackets that trip people up: use [[ ]] for strings and files, and (( )) for numbers. Inside (( )) you
write natural math: if (( count > 100 )). Inside [[ ]] you use -gt, -lt, -eq for numbers and = for strings. Mixing them up
('>' inside [[ ]] means redirection, not greater-than!) is a classic bug. Strings and files: [[ ]]. Pure numbers: (( )).

case — cleaner than many elifs





case "$1" in
start) echo "Starting..." ;;
stop) echo "Stopping..." ;;
restart) echo "Restarting..." ;;
*) echo "Usage: $0 {start|stop|restart}" ;;
esac

1. case matches $1 against patterns — far cleaner than a chain of elif for fixed choices.
2. Each pattern ends with ) and its block ends with ;;.
3. * is the catch-all default.
4. esac closes it. This is exactly how service-control scripts read their command.

PRACTICE EXERCISES
1. Write an if that checks whether a file exists and is readable, printing a message for each case.
2. Use (( )) to test whether a number variable exceeds 10.
3. Write a case statement handling start/stop/status with a usage default.
4. Deliberately use > inside [[ ]] and observe it create a file — then fix it with -gt.





10. Loops
for — iterate over a list
for name in Abdur Sara Ali; do
echo "Hello $name"
done
for f in *.log; do
gzip "$f"
done
for i in {1..5}; do
echo "Attempt $i"
done

1. Loop over an explicit list of words.
2. Loop over files matching a glob — compress each .log. Quote "$f" for safety.
3. {1..5} generates 1 2 3 4 5 — a numeric range loop.

while — loop until a condition changes
count=1
while [[ $count -le 3 ]]; do
echo "Count is $count"
count=$((count + 1))
done
while IFS= read -r line; do
echo "Line: $line"
done < input.txt

1. while repeats as long as the test is true.
2. Do the work...
3. ...and update the counter, or the loop never ends.
4. The correct way to read a file LINE BY LINE: IFS= preserves whitespace, -r prevents backslash mangling...
5. ...and < input.txt feeds the file in. This is the safe file-reading pattern.

PRO INSIGHT: The dangerous anti-pattern to avoid: for line in $(cat file). It breaks on spaces and is a classic bug.
The correct line-by-line read is the while IFS= read -r loop above. Similarly, prefer for f in *.log (a glob) over for f in
$(ls *.log) — the glob handles spaces and odd filenames safely. Loops that touch filenames must be written
carefully.
PRACTICE EXERCISES
1. Loop over three names and greet each.
2. Loop over all .txt files in a directory and print each filename and its line count.
3. Write a countdown from 5 to 1 using a while loop.
4. Read a file line by line with the safe while-read pattern and number each line.





11. Functions, Arguments & Exit Codes
Arguments — how scripts receive input
Variable

Means

$0

the script's name

$1, $2, ...

the first, second, ... argument

$#

the NUMBER of arguments

$@

ALL arguments, as separate quoted words

$*

all arguments as one string

$?

exit code of the last command

$$

the script's process ID

#!/usr/bin/env bash
set -euo pipefail
if [[ $# -lt 1 ]]; then
echo "Usage: $0 <name>" >&2
exit 1
fi
echo "Hello, $1"
echo "You gave $# argument(s)"

1. Guard clause: if fewer than 1 argument was given...
2. ...print usage to stderr (>&2)...
3. ...and exit with code 1 (failure). Every script should validate its input like this.
4. Use the first argument.
5. Report how many were given.

Functions with arguments and return values





greet() {
local name="$1"
echo "Hello, $name"
}
is_running() {
systemctl is-active --quiet "$1"
return $?
}
greet "Abdur"
if is_running nginx; then echo "nginx up"; fi

1. A function; $1 is ITS first argument (separate from the script's).
2. local keeps name inside the function — ALWAYS use local for function variables.
3. A function that returns an EXIT CODE (0 = success/true).
4. return $? passes along whether the service was active.
5. Call greet with an argument.
6. Use is_running as a condition — functions returning 0/non-zero work directly in if.

PRO INSIGHT: Exit codes are how the whole shell communicates success and failure: 0 means success, any other
number means failure. $? holds the last command's code. This is why if command works — it tests whether the
command exited 0. Your functions should follow the same convention: return 0 for success. This single convention
underlies all shell automation, error handling, and the && / || operators.
PRACTICE EXERCISES
1. Write a script that requires two arguments and prints a usage message to stderr if fewer are given.
2. Write a function that takes a filename and prints its line count, using local.
3. Write a function returning success (0) if a file exists, and use it in an if.
4. Print all arguments using "$@" in a loop.





12. Real-World Scripts — Input, Files & Error
Handling
Reading user input
read -p "Enter your name: " name
echo "Hello, $name"
read -sp "Password: " pass; echo
read -p "Continue? [y/N] " ans
[[ "$ans" == "y" ]] || exit 0

1. read -p prompts and stores the reply in a variable.
2. -s hides input (for passwords); the echo adds the missing newline.
3. A yes/no prompt...
4. ...proceed only if the answer is y, otherwise exit cleanly.

Error handling with traps
#!/usr/bin/env bash
set -euo pipefail
tmpdir=$(mktemp -d)
trap 'rm -rf "$tmpdir"' EXIT
trap 'echo "Failed at line $LINENO" >&2' ERR
# work using $tmpdir...
echo "Working in $tmpdir"

1. Create a safe temporary directory.
2. The EXIT trap runs when the script ends FOR ANY REASON — success, failure, or crash — cleaning up the temp
dir. Temp files never leak.
3. The ERR trap fires on any error, reporting WHICH line failed ($LINENO) — invaluable for debugging.

A complete, realistic script
#!/usr/bin/env bash
set -euo pipefail
readonly SRC="${1:?Usage: backup.sh <dir>}"
readonly DEST="$HOME/backups"
readonly STAMP=$(date +%Y%m%d-%H%M%S)
log() { echo "[$(date +%T)] $*"; }
mkdir -p "$DEST"
log "Backing up $SRC"
tar -czf "$DEST/backup-$STAMP.tar.gz" "$SRC"
log "Removing backups older than 7 days"
find "$DEST" -name "backup-*.tar.gz" -mtime +7 -delete
log "Done. Current backups:"
ls -lh "$DEST"





1. Safety trio.
2. readonly constant; ${1:?...} ABORTS with the message if no argument is given — input validation in one line.
3. Where backups go.
4. A timestamp for unique filenames.
5. A logging helper with timestamps.
6. Ensure the destination exists.
7. The dated compressed archive.
8. Auto-cleanup: delete backups older than a week, so the disk never fills.
9. Confirm with a listing. This script combines everything: validation, constants, functions, dated files, retention.

PRACTICE EXERCISES
1. Write a script that asks for a name and a yes/no confirmation before proceeding.
2. Add an EXIT trap that removes a temp file, and prove it fires even on Ctrl+C.
3. Adapt the backup script to back up your own project directory.
4. Add an ERR trap reporting the failing line, then trigger it deliberately.





13. Debugging Bash & Best Practices
The debugging tools
bash -x script.sh
bash -n script.sh
set -x # inside a script: start tracing here
set +x # stop tracing
shellcheck script.sh

1. -x TRACES execution: prints every command with variables expanded, as it runs. The single most useful bash
debugging tool.
2. -n checks SYNTAX without running — catch errors before execution.
3. Turn tracing on for a specific SECTION of a script...
4. ...and off again, to debug just the tricky part.
5. shellcheck is a LINTER that catches bugs, bad quoting, and dangerous patterns automatically. Install with apt install
shellcheck.

PRO INSIGHT: shellcheck is the closest thing bash has to a compiler checking your work. It flags unquoted
variables, useless constructs, common mistakes, and genuine bugs before they bite. Run it on every script you
write. Combined with bash -x for tracing runtime behaviour, these two tools turn bash debugging from guesswork
into a systematic process. No professional writes bash without shellcheck.

The best-practices checklist
Practice

Why

#!/usr/bin/env bash + set -euo pipefail

Portable interpreter, fail fast and loud

Quote every variable: "$var"

Prevents word-splitting bugs and disasters

Use local in functions

Stops variables leaking and clashing

Validate input with ${1:?...} or guards

Fail clearly instead of doing damage

Use $( ) not backticks

Readable and nestable

Use [[ ]] for tests, (( )) for math

The safe, modern constructs

trap for cleanup

Temp files and state cleaned up on any exit

Run shellcheck

Catches bugs automatically before they run

Prefer functions over long linear scripts

Readable, testable, reusable

PRACTICE EXERCISES
1. Run bash -x on any script and read the traced execution.
2. Introduce a syntax error and catch it with bash -n before running.
3. Install shellcheck and run it on your backup script; fix any warnings.
4. Add set -x / set +x around one section to trace only that part.





14. Worked Examples & Full Solutions
Complete answers to the practice exercises across both parts. Try each yourself first, then check your
reasoning here.

Part A — Configuration
Ch.3 — An alias needing a mid-argument (why it fails)
# This alias does NOT work as hoped:
alias backup='cp $1 $1.bak' # $1 is NOT substituted in aliases
# The fix is a function:
backup() { cp "$1" "$1.bak"; }

1. Aliases do simple text replacement and do not handle $1 — it is taken literally, not as your argument. Only a function
can use an argument in the middle. This is the concrete reason functions exist alongside aliases.

Ch.4 — 'up N' function to climb directories
up() {
local n="${1:-1}"
local path=""
for ((i=0; i<n; i++)); do path="../$path"; done
cd "$path" || return 1
}

1. Default to 1 level if no argument. Build a path of N '../' segments with a loop, then cd once. up 3 climbs three
directories. || return 1 handles failure safely.

Ch.5 — Prompt with time and history number
PS1='[\A \!] \w\$ '

1. \A is the time HH:MM, \! the history number, \w the directory. The result looks like [14:30 512] ~/project$ — context
plus a command number you can recall with !512.

Ch.6 — Prove export is needed
MSG="hi"
bash -c 'echo "child sees: $MSG"' # prints: child sees:
export MSG
bash -c 'echo "child sees: $MSG"' # prints: child sees: hi

1. A child process (the inner bash) cannot see MSG until it is exported. Before export, the child prints nothing for $MSG;
after export, it sees 'hi'. This is exactly why your app needs exported env vars.

Part B — Scripting
Ch.8 — Quoting a name with a space





name="Abdur Rahim"
echo "$name" # Abdur Rahim (one piece)
echo $name # Abdur Rahim (two words to any command)

1. Quoted, the value stays one argument. Unquoted, bash splits it on the space into two words — harmless for echo, but
disastrous for rm or cp. Always quote.

Ch.8 — Strip extension and get basename
file="/home/abdur/report.txt"
echo "${file##*/}" # report.txt (basename)
echo "${file##*/%.txt}" # WRONG: cannot chain like this
base="${file##*/}"; echo "${base%.txt}" # report

1. ${file##*/} strips the longest leading match up to the last slash, giving the basename. To also drop the extension, do it
in two steps: first the basename, then %.txt removes the trailing extension. Parameter expansions do not chain in one
expression.

Ch.9 — case for start/stop/status
case "$1" in
start) systemctl start goodo ;;
stop) systemctl stop goodo ;;
status) systemctl status goodo ;;
*) echo "Usage: $0 {start|stop|status}" >&2; exit 1 ;;
esac

1. Each action maps to one command; the * default prints usage to stderr and exits with failure. This is the exact shape
of real service-control scripts.

Ch.10 — Files with line counts
for f in *.txt; do
[[ -e "$f" ]] || continue
printf '%s: %s lines\n' "$f" "$(wc -l < "$f")"
done

1. Loop the glob (safe for spaces). The -e check skips the case where no .txt files exist (the glob would otherwise pass
the literal '*.txt'). wc -l < file counts without printing the name, which we supply ourselves.

Ch.10 — Safe line-by-line read with numbering
n=1
while IFS= read -r line; do
printf '%d: %s\n' "$n" "$line"
n=$((n+1))
done < input.txt

1. IFS= and -r preserve the line exactly; feeding the file with < avoids a subshell so n survives. This is the correct,
whitespace-safe way to process a file line by line.

Ch.11 — Script requiring two arguments





#!/usr/bin/env bash
set -euo pipefail
if [[ $# -lt 2 ]]; then
echo "Usage: $0 <src> <dest>" >&2
exit 1
fi
echo "Copying $1 to $2"

1. $# is the argument count; if fewer than 2, print usage to stderr and exit 1. Validating input up front is the mark of a
robust script.

Ch.11 — Function returning success if file exists
exists() { [[ -e "$1" ]]; }
if exists /etc/hostname; then echo "present"; fi

1. The function's body is just the test; its exit code becomes the function's return value. So exists works directly in an if,
reading naturally. No explicit return needed — the last command's status is returned automatically.

Ch.12 — Confirmation before proceeding
read -p "Delete all logs? [y/N] " ans
[[ "${ans,,}" == "y" ]] || { echo "Cancelled"; exit 0; }
echo "Deleting..."

1. ${ans,,} lowercases the reply so Y and y both work. If it is not y, print Cancelled and exit cleanly. A safe confirmation
pattern for destructive actions.

Ch.13 — Trace a section only
echo "normal part"
set -x
result=$(( 6 * 7 ))
echo "$result"
set +x
echo "normal again"

1. set -x begins printing each command with expansions; set +x stops it. This isolates tracing to the tricky calculation
without flooding the whole run with debug output.

You can now configure the shell to fit your hands and program it to do your work.
That is the whole of bash.
— End of Volume 7, Bash: Configuration & Scripting —