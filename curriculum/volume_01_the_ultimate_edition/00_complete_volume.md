# Volume 1: The Ultimate Edition

LINUX MASTERY
THE ULTIMATE EDITION
The Full Beginner-to-Expert Book — 23 Chapters, Worked Examples, Expected
Outputs,
Real Troubleshooting Scenarios, Exercises, Quick Reference, Interview Questions
& Glossary

Prepared for MD Abdur Rahim · Tampere, Finland · 2026





Table of Contents
1. Foundations — What Linux Actually Is
2. The Terminal & the Shell — Your Cockpit
3. The Filesystem — Deep Dive
4. Core Commands — Working with Files Like a Pro
5. Text Processing Mastery — pipes, grep, sed, awk, regex
6. Users, Groups & Permissions — Complete
7. Processes, Signals & systemd — Complete
8. Package Management — Complete
9. Storage, Disks & Filesystems — Complete
10. Networking — Complete
11. Bash Scripting — From Zero to Automation Engineer
12. Environment, Variables & Dotfiles
13. Logs, Monitoring & Performance Debugging
14. Security Hardening — The Professional Standard
15. The Boot Process & the Kernel
16. Terminal Multiplexing — tmux
17. Vim — Editing at the Speed of Thought
18. WSL Mastery — Linux Inside Windows
19. Containers — Docker on Linux
20. Database Administration — PostgreSQL on Linux
21. Advanced Networking & Firewalls
22. Debugging Like an Expert — strace, lsof, /proc
23. Troubleshooting Scenarios — Ten Real Incidents
24. Capstone — Deploy a Real Production Server
25. The 90-Day Plan & Beyond
Appendix A: Command Reference · B: Interview Questions · C: Glossary





1. Foundations — What Linux Actually Is
The layers
Linux is technically only the kernel — the core program that talks to hardware, schedules processes, and
manages memory. What you install (Ubuntu, Debian, Fedora) is a distribution: the kernel plus thousands of
tools, a package manager, and defaults. On top of the kernel sits the shell (usually bash), the program that
reads your typed commands and runs them.
Layer

What it does

Example

Hardware

CPU, RAM, disk, network card

Your Hetzner VPS or laptop

Kernel

Talks to hardware, runs processes

Linux 6.x

Shell

Interprets your commands

bash, zsh

Utilities

The commands themselves

ls, grep, systemctl

Applications

What you actually run

nginx, PostgreSQL, Python

Why servers run Linux
Over 90% of cloud servers run Linux for concrete reasons: it is free, it runs for years without reboot,
everything is automatable text, resource usage is tiny (a full server OS in 500 MB of RAM), and security
patching is fast and transparent. When you rent a Hetzner VPS or spin up cPouta, you get a blank Linux
machine and full control — this book teaches you to command it.

Distributions — which one to master
Family

Members

Package tool

Choose when

Debian

Debian, Ubuntu, Mint

apt / .deb

Servers, beginners, most
tutorials — LEARN THIS
FIRST

RedHat

RHEL, Fedora, Rocky

dnf / .rpm

Enterprise jobs, RHCSA
certification

Arch

Arch, Manjaro

pacman

Enthusiasts who want
bleeding edge

Alpine

Alpine

apk

Tiny Docker container
images

Skills transfer ~90% between families — only the package manager and a few paths differ. This book uses
Ubuntu/Debian conventions, matching your WSL and cPouta environments.

Where to practice safely
1. WSL (you have it) — perfect daily driver for chapters 1–12. 2. A VM (VirtualBox) — for chapters where we
deliberately break things. 3. A cheap VPS — for the server chapters; a €4/month Hetzner CX22 is the ideal
lab because mistakes cost nothing: destroy and recreate in 60 seconds.





PRO INSIGHT: Beginners fear breaking things, so they never touch anything — and never learn. The fix is not
caution, it is disposable environments. In a VM or cheap VPS, breaking things is the curriculum.
PRACTICE EXERCISES
1. Find out your kernel version with: uname -r — then explain each part of the version number using: man uname
2. Run: cat /etc/os-release — identify your distribution and its Debian/Ubuntu base version.
3. Run: echo $SHELL — confirm which shell you are using.





2. The Terminal & the Shell — Your Cockpit
Anatomy of the prompt
abdur@tampere-laptop:~/projects$ _

1. Read it as: user abdur, on machine tampere-laptop, currently in ~/projects (~ = your home folder), and $ means
normal user. A # prompt means you are root — every keystroke is now dangerous.

Anatomy of a command
ls -lh --sort=size /var/log

1. Four parts: the command (ls), short options (-l -h combined as -lh), a long option with a value (--sort=size), and the
argument (/var/log — what to act on). Nearly every Linux command follows this grammar.

The keyboard shortcuts that triple your speed
Shortcut

Action

Tab

Autocomplete file/command names — press twice to list
all options. USE CONSTANTLY.

Ctrl + R

Search command history as you type — recall any past
command in seconds

Ctrl + C

Cancel the running command

Ctrl + L

Clear screen (same as the clear command)

Ctrl + A / Ctrl + E

Jump to start / end of the line

Ctrl + W

Delete the word before the cursor

Ctrl + D

Logout / end of input

↑/↓

Walk through command history

!!

Repeat last command — the classic: sudo !! after a
permission error

History as a tool
history
history | grep ssh
!105
!!

1. Shows your numbered command history.
2. Finds every ssh command you have ever typed in this shell.
3. Re-runs command number 105 from the list.
4. Re-runs the last command — combine with sudo when you forgot privileges: sudo !!





OUTPUT

$ apt install htop
E: Permission denied
$ sudo !!
sudo apt install htop
[sudo] password for abdur:

Editing files in the terminal — nano and vim survival
nano config.txt
vim config.txt

1. Beginner-friendly editor: type freely, Ctrl+O saves, Ctrl+X exits. Shortcuts are listed at the bottom of the screen.
2. The professional's editor. Survival minimum: press i to type (insert mode), Esc to stop typing, then :wq to save+quit
or :q! to quit without saving. Learn vim properly later with the built-in tutor: run vimtutor (30 minutes, worth it).

TIP: The world's most asked Linux question is 'how do I exit vim'. Now you know: Esc then :q! — you are already
ahead of millions.
PRACTICE EXERCISES
1. Press Ctrl+R and type 'ls' — cycle through past ls commands with repeated Ctrl+R.
2. Type mkd then press Tab — verify it completes to mkdir.
3. Run vimtutor and complete lesson 1.
4. Deliberately run a command without sudo that needs it, then recover with sudo !!





3. The Filesystem — Deep Dive
One tree to rule them all
Windows thinks in drive letters (C:, D:). Linux thinks in one tree rooted at /. A second disk does not get a
letter — it gets mounted onto a directory, becoming part of the same tree. This is why your Windows D: drive
appears at /mnt/d inside WSL: it has been grafted onto the tree.
ls /
ls /mnt/d

1. Shows the top of the tree: bin, etc, home, var, usr...
2. In WSL: your Windows D: drive, mounted into the Linux tree — where your GoOdo project lives.

Every directory, explained properly
Path

Name origin

What lives there &amp; when you visit

/bin, /usr/bin

binaries

The commands themselves. which ls shows you: /usr/bin/ls

/etc

et cetera

ALL system config as text files: ssh, nginx, fstab, users. Your most-edited directory as
an admin

/home

—

One folder per user. Your personal universe: ~/ = /home/abdur

/root

—

Root's home. NOT the same as / itself

/var

variable

Data that grows: /var/log (logs), /var/lib (databases), /var/www (websites)

/tmp

temporary

Scratch space, world-writable, wiped on reboot

/usr

Unix system
resources

Installed software: binaries, libraries, docs

/opt

optional

Self-contained third-party apps — a good home for /opt/goodo

/dev

devices

Hardware as files: /dev/sda (disk), /dev/null (black hole), /dev/urandom (randomness)

/proc, /sys

process/system

Virtual windows into the kernel: not real files, generated live when read

/boot

—

Kernel images and bootloader — look, don't touch

/srv, /media,
/mnt

—

Served data; auto-mounted USB drives; manual mounts

Absolute vs relative paths — get this into muscle memory





cd /var/log
cd nginx
cd ..
cd ../..
cd ./scripts
cd ~
cd -

1. Absolute path: starts with /, works from anywhere.
2. Relative path: resolved from where you stand — this enters /var/log/nginx.
3. .. is the parent directory — now back in /var/log.
4. Two levels up — now in /.
5. . is the current directory — mostly used when running scripts: ./deploy.sh
6. Home, from anywhere.
7. The previous directory — toggle between two work locations.

Hidden files and dotfiles
ls -a ~
ls -d ~/.*

1. -a reveals entries starting with a dot: .bashrc, .ssh, .gitconfig — hidden by convention, not security. These 'dotfiles'
hold your personal configuration.
2. -d lists the dot-entries themselves without descending into them.

Links — two kinds of shortcuts
ln -s /opt/goodo/config.yaml ~/config.yaml
ln /data/report.pdf /backup/report.pdf
ls -l ~/config.yaml

1. Symbolic (soft) link: a pointer to a path. If the target moves, the link breaks. Used everywhere — e.g. nginx
sites-enabled.
2. Hard link: a second name for the SAME data on disk. Delete one name, data survives under the other. Only works
within one filesystem.
3. Symlinks show as: config.yaml -> /opt/goodo/config.yaml with an 'l' as the first permission character.
OUTPUT

lrwxrwxrwx 1 abdur abdur 24 Jul 2 10:15 /home/abdur/config.yaml -> /opt/goodo/config.yaml

Common beginner mistakes
Mistake 1: Spaces in names break commands — my file.txt is two arguments. Fix: quote it ("my file.txt") or
Tab-complete which auto-escapes. Mistake 2: Confusing / (root of tree) with ~ (your home). Mistake 3:
Working as root 'because permissions are annoying' — one typo can end the system. Mistake 4: Case
matters: File.txt and file.txt are different files.
PRACTICE EXERCISES
1. From your home, reach /var/log using only relative paths (cd ../../var/log).
2. Create a symlink in ~ pointing to your GoOdo project folder; verify with ls -l.





3. Run: file /dev/sda /dev/null /etc/passwd — read what the file command says each one is.
4. Explore /proc: cat /proc/uptime, /proc/cpuinfo, /proc/meminfo — three system dashboards, no tools needed.





4. Core Commands — Working with Files Like a Pro
Listing — reading ls -l fluently
ls -lah /etc/ssh

1. The workhorse listing: -l long format, -a all files, -h human sizes.
OUTPUT

-rw-r--r-- 1 root root 3.2K Jun 30 09:14 ssh_config
drwxr-xr-x 2 root root 4.0K Jun 30 09:14 sshd_config.d
-rw------- 1 root root 505 Jun 30 09:14 ssh_host_ed25519_key

Column by column: type+permissions (d=directory, -=file, l=link), link count, owner, group, size, modified
time, name. Notice the host key: -rw------- (600) — only root can read the server's private key. Permissions
tell stories.

Copy and move — the flags that matter
cp report.pdf report_v2.pdf
cp -r project/ project_backup/
cp -a /etc/nginx /root/nginx-backup
cp -i data.csv /backup/
mv *.log old_logs/
mv -n new.conf /etc/app.conf

1. Simple copy in place.
2. -r required for directories (recursive).
3. -a = archive: recursive AND preserves permissions, owners, timestamps — the correct flag for backups.
4. -i asks before overwriting — train yourself to use it until careful habits form.
5. Wildcards work: moves every .log file at once.
6. -n never overwrites — safe deploys.

Deleting — respect the gun
rm draft.txt
rm -i *.tmp
rm -r old_project/
rm -rf node_modules/
rmdir empty_dir/

1. Deletes one file. Gone. No recycle bin.
2. Interactive confirmation per file — good with wildcards.
3. Recursive delete of a directory tree (asks nothing).
4. -f adds force: no prompts even for protected files. The famous, dangerous combo — always re-read the path before
Enter.
5. Only deletes EMPTY directories — a built-in safety when that is what you intend.

PRO INSIGHT: Expert habit: before any rm with a wildcard, run ls with the SAME pattern first. ls *.tmp shows
exactly what rm *.tmp will destroy. Two seconds of checking, years of regret avoided.





Viewing files — choosing the right tool
Tool

Best for

Key moves

cat

Short files, feeding pipes

cat -n adds line numbers

less

Anything long

/search, n next, G end, g start, q quit

head / tail

First/last N lines

tail -n 50; tail -f = live follow

watch

Repeating a command

watch -n 2 df -h — live disk
dashboard

diff

Comparing files

diff -u old.conf new.conf — what
changed?

tail -f /var/log/nginx/access.log
diff -u nginx.conf nginx.conf.bak
watch -n 1 "ss -tulpn | grep 8000"

1. Watch web requests arrive live. Ctrl+C to stop. Add | grep 404 to watch only errors.
2. Unified diff: lines starting with - were removed, + were added. Exactly like git diff — same format.
3. Re-runs the check every second — watch your port appear as the backend starts.

find — the interrogator
find walks a directory tree and tests every entry against your conditions — then optionally acts on matches.
Grammar: find WHERE CONDITIONS ACTION.
find /var/log -name "*.log"
find . -iname "readme*"
find /home -type d -name ".ssh"
find . -type f -size +100M
find /opt -mtime -2
find . -name "*.pyc" -delete
find . -name "*.sh" -exec chmod +x {} \;
find /tmp -type f -mtime +7 -exec rm {} +

1. Name match with wildcard (quote it so the shell doesn't expand it first).
2. -iname = case-insensitive.
3. Only directories (-type d) named .ssh — audit who has keys.
4. Files over 100 MB — disk-hog hunting.
5. Modified in the last 2 days — 'what changed recently?'
6. Built-in delete action for matches.
7. -exec runs a command per match; {} is the filename, \; ends the command. Makes every script executable.
8. The + variant batches many files into one command — much faster. This line: clean week-old temp files.

Wildcards (globs) — the shell's pattern language
Pattern

Matches

Example

*

anything, any length

*.py — all Python files





Pattern

Matches

Example

?

exactly one character

log?.txt — log1.txt, logA.txt

[abc]

one char from the set

report[12].pdf

[0-9]

one char in range

backup-202[0-6]*

{a,b}

either alternative

cp app.{py,py.bak} — expands to two
names

**

recursive (bash: shopt -s globstar)

ls **/*.md — all markdown, any depth

PRACTICE EXERCISES
1. List everything in /etc modified in the last 24 hours (find /etc -mtime -1 -type f).
2. Find the 5 largest files in your home directory (find ~ -type f -size +10M -exec ls -lh {} + | sort -k5 -rh | head -5).
3. Copy your GoOdo lib/ folder with permissions preserved using cp -a; verify timestamps match.
4. Use diff to compare two versions of any config file and read the -/+ lines aloud.





5. Text Processing Mastery
The philosophy: small tools, composed
Unix's founding idea: each program does one thing well and reads/writes plain text, so any output can feed
any input through a pipe. Mastering five tools — grep, sed, awk, sort, uniq — plus pipes gives you a
data-processing engine more flexible than most GUI software.

The three streams
command < input.txt
command > output.txt
command 2> errors.txt
command >> log.txt
command > /dev/null 2>&1
command | tee output.txt

1. stdin (stream 0): feed a file as input.
2. stdout (stream 1): capture normal output (overwrite).
3. stderr (stream 2): capture only errors — they are separate streams, which is why error messages 'escape' your
redirects.
4. Append instead of overwrite.
5. Silence everything: output to the void, errors follow output (2>&1 = 'send stream 2 where 1 goes').
6. tee splits the stream: show on screen AND save to file simultaneously — watch and log at once.

grep — complete treatment
grep -i "error" app.log
grep -rn "OdometerManager" lib/
grep -l "TODO" *.py
grep -A 3 -B 1 "Traceback" app.log
grep -w "port" nginx.conf
grep -o "https://[^ ]*" page.html
grep -E "^(GET|POST)" access.log

1. Case-insensitive search.
2. Recursive with line numbers — grep your GoOdo codebase for a class.
3. -l prints only FILE NAMES containing a match — 'which files mention TODO?'
4. Context lines: 3 After and 1 Before each match — see the whole Python traceback, not just its first line.
5. -w whole words only: matches 'port' but not 'export' or 'important'.
6. -o prints only the matching part, not the whole line — extracts every URL from a page.
7. -E enables extended regex: lines beginning (^) with GET or POST.

Regex in 10 minutes — the 20% you use 95% of the time
Symbol

Means

Example

^$

start / end of line

^root — lines starting with root

.

any single character

b.t matches bat, bit, but





Symbol

Means

Example

*+?

0+, 1+, 0-or-1 of previous

go+gle matches google, gooogle

[abc] [^abc]

set / negated set

[0-9]+ — one or more digits

(|)

grouping and OR

(jpg|png|gif)$

\.

literal dot (escape specials)

192\.168\. — an IP prefix

{n,m}

repetition count

[0-9]{1,3} — 1 to 3 digits

grep -E "^[a-zA-Z0-9._]+@[a-z]+\.[a-z]{2,}$" emails.txt

1. A practical email validator: start, allowed name characters (one or more), @, domain letters, a literal dot, a 2+ letter
TLD, end. Read regex left to right like a sentence and it stops being scary.

sed — complete treatment
sed reads line by line, applies your instruction, prints the result. Its core instruction is s/find/replace/flags —
but it can also delete, insert, and slice.
sed 's/localhost/127.0.0.1/' app.conf
sed 's/old/new/g' file.txt
sed -i.bak 's/DEBUG = True/DEBUG = False/' settings.py
sed -n '/server {/,/}/p' nginx.conf
sed '/^$/d' data.txt
sed '3i\# inserted comment' script.sh
sed 's|/opt/old|/opt/new|g' paths.txt

1. Replaces the FIRST occurrence per line.
2. g flag: ALL occurrences per line.
3. -i.bak edits in place but first saves file.txt.bak — the professional's seatbelt. The Django go-live edit, done safely.
4. Range printing: from the line matching 'server {' to the line matching '}' — extract one config block.
5. Deletes empty lines (^$ = start immediately followed by end).
6. Inserts a line before line 3.
7. Any delimiter works — use | when your pattern is full of slashes (paths), avoiding escape soup.

awk — complete treatment
awk sees every line as columns ($1, $2...; $0 = whole line) and runs pattern { action } rules on each. It has
variables, math, and even functions — a mini programming language for tabular text.





awk '{print $1, $9}' access.log
awk -F: '{print $1}' /etc/passwd
awk '$9 >= 500' access.log
awk '{bytes[$1] += $10} END {for (ip in bytes) print bytes[ip], ip}' access.log | sort -rn
| head -5
df -h | awk '$5+0 > 80 {print $6, "is", $5, "full"}'
awk 'NR==5,NR==10' file.txt

1. Print columns 1 and 9 (IP and status code in nginx logs).
2. -F: sets colon as separator — lists every username on the system.
3. A pattern with no action prints matching lines whole: all server errors (status ≥ 500).
4. Associative array: sum bytes per IP, then print totals — top-5 bandwidth consumers in one line. This is where awk
becomes a superpower.
5. Practical monitoring: warn for any partition over 80% used ($5+0 converts '82%' to number 82).
6. NR is the line number — print lines 5 through 10.
OUTPUT

184729342 203.0.113.42
99182811 198.51.100.7
41230010 192.0.2.19

sort, uniq, cut, tr, xargs — the supporting cast
sort -t',' -k3 -n sales.csv
cut -d',' -f1,3 data.csv
tr 'a-z' 'A-Z' < names.txt
tr -d '\r' < windows.txt > unix.txt
cat urls.txt | xargs -n1 curl -sI | grep HTTP

1. Sort a CSV by column 3 numerically (-t separator, -k key column, -n numeric).
2. Extract columns 1 and 3 — lighter than awk when no logic is needed.
3. Translate characters: uppercase everything.
4. Delete carriage returns — THE fix for 'bad interpreter ^M' errors when scripts were edited on Windows. You will need
this in WSL someday.
5. xargs turns input lines into command arguments: check the HTTP status of every URL in a file.

Worked example — full log investigation
# Question: which URLs caused the most 404s yesterday?
grep "$(date -d yesterday +%d/%b/%Y)" access.log \
| awk '$9 == 404 {print $7}' \
| sort | uniq -c | sort -rn | head

1. A real investigation, built step by step:
2. Filter to yesterday's date (date command generates '01/Jul/2026' in nginx's format).
3. Keep only 404 lines, extract the URL column.
4. Count each unique URL, rank, top 10. Build such pipelines incrementally — run after each pipe, verify, add the next.

PRO INSIGHT: The incremental method is THE way pros build one-liners: never write a 5-stage pipeline at once.
Run stage 1, look, add stage 2, look. Each pipe is a checkpoint.





PRACTICE EXERCISES
1. From /etc/passwd, print usernames whose shell is /bin/bash (awk -F: '$7=="/bin/bash" {print $1}').
2. Count how many unique words are in any text file (tr ' ' '\n' < file | sort -u | wc -l).
3. Use sed -i.bak to change a value in a copy of some config, then diff the .bak against the new version.
4. Write the 404-investigation pipeline against any nginx/Apache log (sample logs are easy to find online).





6. Users, Groups & Permissions — Complete
The model
Every file carries: an owner (user), a group, and three permission triplets — what the owner may do, what
group members may do, what everyone else may do. Each triplet is rwx: read, write, execute. That's the
whole model; everything else is detail.

What rwx really means — files vs directories
Permission

On a file

On a directory

r (4)

read contents

list the names inside (ls)

w (2)

modify contents

create/delete/rename entries inside

x (1)

run as a program

enter it (cd) and access things inside

WARNING: Directory subtlety that trips everyone: to delete a file you need w on its DIRECTORY, not on the file
itself. A read-only file inside a writable directory can still be deleted.

Numeric permissions — do the math once
Each triplet sums: r=4, w=2, x=1. So rwx=7, r-x=5, rw-=6, r--=4. Three triplets → three digits: 754 = rwxr-xr-(owner everything, group read+exec, others read only).
chmod 644 index.html
chmod 755 deploy.sh
chmod 600 ~/.ssh/id_ed25519
chmod 700 ~/.ssh
chmod -R 755 /var/www/html
chmod u+x,go-w script.sh
chmod +x script.sh

1. Web content: world readable, only owner edits.
2. Executable script or any directory.
3. Private key: owner only — SSH REFUSES keys with looser permissions.
4. The .ssh directory itself must be 700.
5. -R applies recursively down the tree.
6. Symbolic form: add execute for user, remove write from group and others — surgical changes without recalculating
full numbers.
7. Shorthand: executable for everyone allowed by umask — the everyday 'make my script runnable'.

Ownership





sudo chown deploy app.py
sudo chown deploy:www-data app.py
sudo chown -R www-data:www-data /var/www/goodo
sudo chgrp developers shared_folder/

1. Change the owner.
2. Owner and group in one shot (user:group).
3. The standard web deployment fix: the web server user must own web files.
4. Change only the group.

Groups — collaboration without chaos
sudo groupadd developers
sudo usermod -aG developers abdur
groups abdur
sudo mkdir /srv/shared
sudo chgrp developers /srv/shared
sudo chmod 2775 /srv/shared

1. Create a team group.
2. Add a member. -aG = append to groups. Log out/in for it to take effect.
3. Verify membership.
4. A shared workspace...
5. ...owned by the team group...
6. ...with 2775: the leading 2 is the setgid bit — every file created inside automatically inherits the 'developers' group.
Without it, shared folders slowly rot into permission chaos.

The special bits and umask
Bit

Number

Effect

Seen in the wild

setuid

4xxx

File runs with OWNER's
privileges

/usr/bin/passwd (must edit
root's shadow file)

setgid

2xxx

Dir: new files inherit group

Shared team directories

sticky

1xxx

Dir: only owners delete
their own files

/tmp is 1777 — shared but
safe

umask
umask 027

1. Shows the default-permission mask, usually 0022. It SUBTRACTS from 666 (files) / 777 (dirs): so new files get 644,
new dirs 755.
2. A stricter mask for servers: new files 640, dirs 750 — others get nothing by default.

sudo — how it actually works





sudo systemctl restart nginx
sudo -u postgres psql
sudo visudo
# inside sudoers:
deploy ALL=(ALL) NOPASSWD: /usr/bin/systemctl restart goodo

1. Run one command as root; your own password; logged to auth.log.
2. Run as a DIFFERENT user — how you enter PostgreSQL's admin account.
3. The ONLY safe way to edit /etc/sudoers — it syntax-checks before saving (a broken sudoers can lock everyone out
of root).
4. Fine-grained rule: the deploy user may restart exactly one service without a password — perfect for CI/CD pipelines,
and nothing more.

PRACTICE EXERCISES
1. Translate to numbers: rwxr-x---, rw-rw-r--, r--------. Then reverse: 711, 640, 4755.
2. Create /tmp/team with setgid, make two test users, verify files created by one carry the shared group.
3. Break your own SSH key on purpose (chmod 644), watch ssh refuse it with -v, then fix it.
4. Read /etc/sudoers with sudo cat — find the line granting the sudo group its power (%sudo ALL=(ALL:ALL) ALL).





7. Processes, Signals & systemd — Complete
What a process is
A process = a running program + its memory + open files + an ID (PID) + a parent (PPID). Everything running
descends from PID 1 — which on modern Linux is systemd itself. Kill a parent shell and its children usually
die too; that's why nohup and systemd exist.
ps aux --sort=-%mem | head -8
pstree -p | head -20
pgrep -af uvicorn

1. All processes sorted by memory, top 8. Columns: USER, PID, %CPU, %MEM, START, COMMAND.
2. The family tree with PIDs — see how sshd spawns your bash which spawns your commands.
3. Find PIDs by command-line pattern, showing the full command (-a).

Signals — the process control vocabulary
Signal

Number

Meaning

Can be ignored?

SIGTERM

15

Please shut down cleanly
(default of kill)

Yes — apps catch it to
save state

SIGKILL

9

Die immediately, no
cleanup

NO — kernel enforces it

SIGHUP

1

Terminal closed; many
daemons treat it as 'reload
config'

Yes

SIGINT

2

Ctrl+C from keyboard

Yes

SIGSTOP/SIGCONT

19/18

Pause / resume (Ctrl+Z
uses TSTP)

STOP cannot be ignored

kill 4321
kill -9 4321
killall python3
pkill -f "uvicorn main:app"
kill -HUP $(pgrep nginx | head -1)

1. Polite termination — ALWAYS the first attempt; the app can close files and connections.
2. The sledgehammer — only when TERM was ignored. Data in memory is lost.
3. By process name — all matching processes.
4. By full command-line match.
5. Send reload-config to nginx's master process — zero-downtime config change (systemctl reload does this for you).

Job control and priorities





python3 heavy_job.py &
disown -h %1
nice -n 10 tar -czf huge.tar.gz /data
sudo renice -5 -p 4321
ionice -c3 backup.sh

1. Background it.
2. Detach from the shell so logout won't kill it (nohup's cousin, applied after the fact).
3. Start at lower CPU priority (niceness +10; range -20 highest to +19 lowest) — heavy jobs that shouldn't slow the
server.
4. Raise priority of a running process (negative = higher; needs root).
5. Idle-class disk I/O — the backup only uses the disk when nothing else wants it.

systemd — the complete practical tour
systemctl list-units --type=service --state=running
systemctl status postgresql
systemctl cat nginx
sudo systemctl edit goodo
systemctl list-timers
systemd-analyze blame | head

1. Everything currently running as a service — know your machine.
2. Deep status: active state, uptime, PID, memory, recent log lines.
3. Shows the ACTUAL unit file in effect, including overrides.
4. Creates a safe override file for your changes — survives package upgrades that would overwrite the original.
5. systemd timers — the modern cron alternative, with logging built in.
6. Which services slow down your boot — performance forensics.

A production-grade unit file, annotated
[Unit]
Description=GoOdo API
After=network-online.target postgresql.service
Wants=network-online.target
[Service]
Type=simple
User=deploy
Group=deploy
WorkingDirectory=/opt/goodo/backend
EnvironmentFile=/opt/goodo/.env
ExecStart=/opt/goodo/venv/bin/uvicorn main:app --port 8000
Restart=on-failure
RestartSec=5
NoNewPrivileges=true
ProtectSystem=full
[Install]
WantedBy=multi-user.target

1. Human label.
2. Ordering: start after network AND the database.





3. Soft dependency on real network connectivity.
4. simple = ExecStart IS the main process (the normal case).
5. Never root.
6. Where relative paths resolve.
7. Secrets loaded from a 600-permission env file — never inline in the unit.
8. Absolute path always; systemd has no shell PATH.
9. Restart on crashes but NOT on clean exit — smarter than 'always'.
10. Grace period between restarts.
11. Security: the process can never gain new privileges...
12. ...and sees /usr and /etc as read-only. Free hardening in two lines.
13. Ties into normal boot for systemctl enable.
sudo cp goodo.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now goodo
systemctl status goodo
journalctl -u goodo -n 50

1. Install the unit.
2. Make systemd re-read unit files — required after every edit.
3. Enable at boot AND start now, one command.
4. Verify it's running.
5. Last 50 log lines if anything looks wrong.

systemd timers — cron's successor
# backup.timer
[Timer]
OnCalendar=*-*-* 03:00:00
Persistent=true
[Install]
WantedBy=timers.target

1. A .timer unit triggers a matching .service unit (backup.service).
2. Calendar syntax: daily at 03:00. Also valid: 'Mon *-*-* 09:00' or 'hourly'.
3. Persistent=true runs a MISSED job at next boot — cron silently skips jobs if the machine was off; timers don't. This is
why timers win for laptops and VPSs that reboot.

PRACTICE EXERCISES
1. Run sleep 300 &, find its PID three ways (jobs -l, pgrep, ps aux | grep), then TERM it.
2. Start a CPU-heavy loop (yes > /dev/null &), watch it in top, renice it to 19, observe %CPU under load.
3. Write and install a unit file for any small Python script; verify it survives kill -9 (systemd restarts it) and a reboot.
4. Convert your backup cron idea into a .service + .timer pair; check it with systemctl list-timers.





8. Package Management — Complete
What a package manager actually does
A package is a compressed archive of files + metadata (version, dependencies, install scripts). The manager
keeps a database of every file it installed, resolves dependency graphs, and verifies signatures. This is why
apt install is safe and curl | sudo bash is a leap of faith.

The apt workflow, properly understood
sudo apt update
apt list --upgradable
sudo apt upgrade
sudo apt full-upgrade
sudo apt install nginx=1.24.*
apt-mark hold postgresql-16
apt depends nginx
dpkg -L nginx
dpkg -S /usr/sbin/nginx

1. Downloads fresh package INDEXES from repositories listed in /etc/apt/sources.list.d/. Installs nothing.
2. Preview what would change before committing.
3. Upgrades installed packages, but never removes anything to do it.
4. Also allowed to remove/replace packages when dependencies demand — used for release upgrades.
5. Pin a version pattern when you need reproducibility.
6. Freeze a package at its current version — protect a database from surprise major upgrades.
7. Show the dependency tree.
8. List every file a package installed — 'where did its config go?'
9. Reverse lookup: which package owns this file?

Adding third-party repositories — safely
curl -fsSL https://download.docker.com/linux/ubuntu/gpg \
| sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
echo "deb [signed-by=/etc/apt/keyrings/docker.gpg] \
https://download.docker.com/linux/ubuntu noble stable" \
| sudo tee /etc/apt/sources.list.d/docker.list
sudo apt update && sudo apt install docker-ce

1. Download the vendor's signing key and store it in the keyring directory.
2. Register the repository, explicitly bound to that key (signed-by) — packages are cryptographically verified against the
vendor.
3. Refresh indexes; install. This is the modern, correct pattern (the old apt-key is deprecated).

Python, Node and language packages — avoiding the classic traps





python3 -m venv ~/venvs/goodo
source ~/venvs/goodo/bin/activate
pip install -r requirements.txt
deactivate
pipx install httpie

1. Create an isolated environment — NEVER pip install into the system Python on a server; apt and pip will fight and
both lose.
2. Activate it (your prompt gains a (goodo) prefix).
3. Install project dependencies inside the sandbox.
4. Leave the environment.
5. pipx: for TOOLS (not libraries) — each gets its own hidden venv, available globally. Best of both worlds.

Cleaning and system maintenance
sudo apt autoremove --purge
sudo apt clean
du -sh /var/cache/apt
sudo journalctl --vacuum-time=14d

1. Remove orphaned dependencies and their configs.
2. Delete downloaded .deb files from cache.
3. Check how much the cache was holding.
4. While cleaning: cap journal logs to two weeks — small-VPS hygiene.

PRACTICE EXERCISES
1. Find which package owns /etc/ssh/sshd_config (dpkg -S), then list every file that package installed.
2. Hold a package, run apt upgrade, observe it being kept back, then unhold it.
3. Create a venv, install requests inside, verify with pip list that the system Python is untouched.
4. Add the official nginx repo following the signed-by pattern (nginx.org documents it) on a test VM.





9. Storage, Disks & Filesystems — Complete
From metal to files — the storage stack
The chain: physical disk (/dev/sda) → partitions (/dev/sda1) → optionally LVM volumes → a filesystem
(ext4/xfs) written onto them → mounted into the tree. Understanding this chain lets you debug any storage
problem by asking 'which layer is broken?'
lsblk -f

1. The one command that shows the whole chain: devices, partitions, filesystem types, labels, UUIDs, and mount points
in a tree.
OUTPUT

NAME FSTYPE LABEL UUID MOUNTPOINT
sda
■■sda1 ext4 1f2e3d4c-... /
■■sda2 swap 9a8b7c6d-... [SWAP]
sdb
■■sdb1 ext4 data 5e6f7a8b-... /mnt/data

Adding a new disk — the full ritual
sudo fdisk /dev/sdb
# inside fdisk: n (new), p (primary), Enter x3, w (write)
sudo mkfs.ext4 -L data /dev/sdb1
sudo mkdir /mnt/data
sudo mount /dev/sdb1 /mnt/data
df -h /mnt/data

1. Interactive partitioner on the NEW disk (triple-check it's sdb, not sda!).
2. Create one partition using the whole disk; w writes the table.
3. Format with ext4, giving it a label for humans.
4. Create the mount point directory.
5. Attach it.
6. Confirm the space is available.

fstab — done correctly
sudo blkid /dev/sdb1
# /etc/fstab
UUID=5e6f7a8b-... /mnt/data ext4 defaults,nofail 0 2
sudo mount -a && findmnt /mnt/data

1. Get the UUID — device names (sdb) can change between boots; UUIDs never do. ALWAYS use UUIDs in fstab.
2. The entry: UUID, mountpoint, fs type, options (nofail = a missing disk won't block boot), dump=0, fsck order=2 (root is
1).
3. mount -a applies fstab now AND validates syntax; findmnt confirms. Test BEFORE reboot — a bad fstab drops the
server into emergency mode.





Swap — the safety net
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
sudo sysctl vm.swappiness=10

1. Reserve a 2 GB file.
2. Root-only — swap can contain memory secrets.
3. Format it as swap space.
4. Activate immediately (verify with free -h).
5. Persist across reboots.
6. Tune: swappiness 10 = 'use swap only under real pressure' — right for servers (default 60 is desktop-tuned). Persist
in /etc/sysctl.d/.

PRO INSIGHT: Small-VPS survival: 2 GB RAM + no swap means one traffic spike triggers the OOM-killer and your
backend 'mysteriously' dies at 3 AM. Swap converts a crash into mere slowness. Always add it.

LVM in one page — why clouds love it
LVM inserts a flexible layer: physical volumes (PV) pool into a volume group (VG), from which logical
volumes (LV) are carved. The payoff: resize live, add disks to the pool, snapshot before risky changes.
sudo lvs
sudo lvextend -r -L +10G /dev/ubuntu-vg/root

1. List logical volumes — cloud images often ship with LVM already.
2. Grow the root volume by 10 GB AND (-r) resize the filesystem inside, live, no reboot. This is how you use that extra
disk space your VPS provider just granted.

Filesystem health
sudo smartctl -H /dev/sda
sudo fsck -n /dev/sdb1
sudo tune2fs -l /dev/sda1 | grep -i "mount count"

1. Disk hardware self-test verdict (apt install smartmontools) — catch dying disks early.
2. Check filesystem consistency read-only (-n). NEVER fsck a mounted filesystem for real repairs — unmount first or
use a live/rescue boot.
3. ext4 metadata: how many mounts since last check.

PRACTICE EXERCISES
1. Map your entire machine with lsblk -f and explain every line.
2. In a VM: add a virtual disk, partition, format, mount, add a UUID fstab entry with nofail, reboot, verify.
3. Create and enable a 1 GB swapfile; run a memory-hungry command and watch free -h during it.
4. In a VM with LVM: extend the root LV by 1 GB live and verify with df -h — no reboot allowed.





10. Networking — Complete
The mental model
A connection = source IP:port → destination IP:port over TCP or UDP. Your server has interfaces (eth0)
with IPs; services listen on ports; a firewall filters what may pass; DNS translates names to IPs. Every
network problem is one of these four layers failing — diagnose in order: interface up? → DNS resolves? →
route exists? → port open?

Layer-by-layer diagnosis — the professional sequence
ip -br a
ping -c2 1.1.1.1
ping -c2 google.com
dig +short api.goodo.app
curl -v https://api.goodo.app/health 2>&1 | tail -15

1. Brief interface view: is eth0 UP with an address? If not, nothing else matters.
2. Raw IP reachability, bypassing DNS. Works → internet is fine.
3. Same test WITH a name. This fails but step 2 worked → it's a DNS problem, look at /etc/resolv.conf.
4. What does the name resolve to? Wrong IP → your DNS record is the bug.
5. -v shows the whole conversation: TCP connect, TLS handshake, request, response. The line where it stalls names
the guilty layer.

Ports and listening services
sudo ss -tulpn
sudo ss -tn state established
nc -zv 86.50.20.210 22
curl ifconfig.me

1. The listening map: every open port and which process owns it. Anything you don't recognize deserves investigation.
2. Current live connections — who is talking to your server right now?
3. netcat port probe: is port 22 reachable from HERE? Distinguishes 'service down' from 'firewall blocking'.
4. Your public IP as the internet sees it (differs from ip a behind NAT).

SSH — the complete professional setup
ssh-keygen -t ed25519 -C "abdur@laptop-2026"
ssh-copy-id -i ~/.ssh/id_ed25519.pub deploy@server
ssh -v deploy@server

1. Modern key. Use a passphrase; ssh-agent means you type it once per session.
2. Appends your public key to the server's ~/.ssh/authorized_keys with correct permissions.
3. -v debug mode — when login fails, the answer is ALWAYS in this output (key offered? accepted? permissions
complaint?).





# ~/.ssh/config
Host hetzner
HostName 95.216.x.x
User deploy
IdentityFile ~/.ssh/id_ed25519
ServerAliveInterval 60
Host *.tuni.fi
User marahim34

1. Alias: ssh hetzner instead of the full incantation. rsync/scp/git all honor it.
2. Keepalive every 60 s — no more frozen sessions after laptop sleep.
3. Patterns work: any tuni.fi host automatically uses your student username.

Tunnels — SSH's superpower
ssh -L 5432:localhost:5432 hetzner
ssh -L 8080:internal-db:80 jumphost
ssh -R 9000:localhost:8000 hetzner
ssh -D 1080 hetzner

1. Local forward: your localhost:5432 becomes the server's PostgreSQL — develop against production-like data with
the DB never exposed to the internet.
2. Through a bastion: reach a machine only the jumphost can see.
3. Reverse: the SERVER's port 9000 forwards back to YOUR laptop's 8000 — demo your local GoOdo backend to
someone remotely.
4. Dynamic: a SOCKS proxy — route a browser through your server (an instant poor-man's VPN).

Transferring files
scp -r ./dist hetzner:/opt/goodo/
rsync -avz --progress ./backend/ hetzner:/opt/goodo/backend/
rsync -avzn --delete ./site/ hetzner:/var/www/

1. Simple recursive copy over SSH.
2. The better tool: only differences travel; resume-friendly; -a preserves everything.
3. -n = DRY RUN with --delete: see what WOULD be deleted before mirroring. Always dry-run destructive syncs first.

PRACTICE EXERCISES
1. Run the 5-step diagnosis sequence on your own machine and narrate each result.
2. Set up ~/.ssh/config aliases for cPouta and one other host; achieve passwordless login to both.
3. Tunnel a remote port to your laptop and prove it with curl localhost:PORT.
4. Use nc -l 9999 on one machine and nc IP 9999 on another — chat over raw TCP to demystify sockets.





11. Bash Scripting — From Zero to Automation
Engineer
Your first real script, line by line
#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'
readonly LOG_FILE="/var/log/myscript.log"
main() {
log "Starting"
check_requirements
do_work "$@"
log "Done"
}
log() { printf '%s %s\n' "$(date '+%F %T')" "$*" | tee -a "$LOG_FILE"; }
main "$@"

1. Interpreter line.
2. The safety trio (exit on error / undefined vars are errors / pipeline failures propagate).
3. Safer word-splitting: only newlines and tabs split words — spaces in filenames stop breaking loops.
4. readonly prevents accidental reassignment of constants.
5. A main() function keeps top-level clean and makes order obvious.
6. "$@" forwards all script arguments, properly quoted.
7. Timestamped logging to screen AND file via tee -a.
8. The only top-level statement: run main with the original arguments. This skeleton scales from 10 lines to 1000.

Variables and quoting — where 80% of bugs live
name="Abdur Rahim"
echo "Hello, $name"
echo 'Hello, $name'
file_count=$(ls | wc -l)
echo "There are ${file_count} files"
default="${1:-/tmp}"
: "${API_KEY:?API_KEY must be set}"

1. No spaces around = — bash is strict.
2. Double quotes: variables expand.
3. Single quotes: literal text, no expansion — prints $name as-is.
4. $( ) command substitution captures output.
5. Braces disambiguate: ${file_count}s vs $file_counts.
6. Parameter default: first argument, or /tmp if none given.
7. Guard clause: abort with a message if a required env variable is missing — fail fast, fail loud.





Tests and branching — the full toolkit
if [[ -f "$conf" && -r "$conf" ]]; then
source "$conf"
fi
if (( count > 100 )); then echo "high"; fi
case "$1" in
start) systemctl start goodo ;;
stop) systemctl stop goodo ;;
logs) journalctl -u goodo -f ;;
*) echo "Usage: $0 {start|stop|logs}"; exit 1 ;;
esac

1. [[ ]] for strings/files: -f exists-and-file, -r readable, combined with &&.
2. source executes another file in THIS shell — loading config variables.
3. (( )) for arithmetic: natural math syntax, no -gt needed.
4. case: the clean way to build subcommands...
5. * is the catch-all; this five-liner is a complete service control wrapper.

Arrays and loops that don't break on spaces
servers=("hetzner" "cpouta" "backup-host")
for s in "${servers[@]}"; do
ssh "$s" 'df -h /' || echo "FAILED: $s"
done
while IFS= read -r file; do
gzip "$file"
done < <(find /var/log -name "*.log" -mtime +7)

1. Array literal.
2. "${arr[@]}" is THE correct expansion — each element stays one word even with spaces.
3. Run a health check on each; || catches per-host failure without killing the loop (careful: set -e is relaxed inside
conditions).
4. The process-substitution pattern < <(...) feeds find results line-by-line safely — the professional replacement for the
broken `for f in $(find ...)`.

Arguments like a real CLI tool — getopts





while getopts "e:vh" opt; do
case $opt in
e) ENV="$OPTARG" ;;
v) VERBOSE=1 ;;
h) usage; exit 0 ;;
*) usage; exit 1 ;;
esac
done
shift $((OPTIND - 1))

1. Declares options: -e takes a value (the colon), -v and -h are flags.
2. OPTARG holds the value given to -e.
3. Remove parsed options so $1 becomes the first positional argument. Now your script runs as: deploy.sh -e prod -v
target1 target2

Traps — cleaning up no matter what
tmpdir=$(mktemp -d)
trap 'rm -rf "$tmpdir"' EXIT
trap 'echo "Interrupted"; exit 130' INT

1. Safe unique temp directory.
2. The EXIT trap runs on ANY exit — success, failure, or crash. Temp files never orphan again.
3. Handle Ctrl+C gracefully: message, conventional exit code 130.

Worked example — a deployment script with everything
#!/usr/bin/env bash
set -euo pipefail
readonly APP="goodo" HOST="hetzner"
readonly RELEASE="/opt/$APP/releases/$(date +%Y%m%d%H%M%S)"
log() { printf '\033[32m[deploy]\033[0m %s\n' "$*"; }
fail() { printf '\033[31m[error]\033[0m %s\n' "$*" >&2; exit 1; }
git diff --quiet || fail "Uncommitted changes — commit first"
log "Testing..."
./run_tests.sh || fail "Tests failed"
log "Uploading to $RELEASE"
ssh "$HOST" "mkdir -p $RELEASE"
rsync -az --exclude '.git' ./ "$HOST:$RELEASE/"
log "Switching symlink + restarting"
ssh "$HOST" "ln -sfn $RELEASE /opt/$APP/current \
&& sudo systemctl restart $APP"
sleep 3
curl -fsS "https://api.goodo.app/health" >/dev/null \
|| fail "Health check FAILED — investigate now"
log "Deployed successfully ✔"

1. Constants up top.
2. Timestamped release directory — every deploy is kept, enabling instant rollback.





3. Colored log helpers (32=green, 31=red); errors go to stderr.
4. Guard: refuse to deploy uncommitted code.
5. Gate on tests.
6. Upload the new release beside the old ones.
7. The atomic switch: ln -sfn repoints 'current' instantly — this is the zero-downtime trick...
8. ...then restart the service (allowed passwordless via the sudoers rule from Ch. 6).
9. The verdict: hit the health endpoint; -f makes curl fail on HTTP errors.
10. Rollback if needed = repoint the symlink to the previous release. One command.

PRO INSIGHT: Run shellcheck on every script you write (apt install shellcheck). It catches quoting bugs, dangerous
patterns and typos instantly — the closest thing to a bash compiler. Non-negotiable professional habit.
PRACTICE EXERCISES
1. Write the case-based service wrapper for any systemd unit and use it for a week.
2. Write a script that takes -d DIR and -n DAYS via getopts and archives files older than N days from DIR.
3. Add an EXIT trap to any script and prove it fires on Ctrl+C.
4. Adapt the deployment script skeleton to your GoOdo backend on a test VPS — including the health-check gate.





12. Environment, Variables & Dotfiles
How environment variables flow
FOO=bar python3 -c "import os; print(os.environ['FOO'])"
export DATABASE_URL="postgres://..."
env | sort | less
echo $PATH | tr ':' '\n'

1. Prefix form: the variable exists ONLY for that one command — clean and safe for secrets in tests.
2. export makes it inherited by every child process started from this shell.
3. Inspect your full environment.
4. PATH readable: the ordered list of directories searched for commands. First match wins — which is how a venv
'takes over' python.

Which file loads when — end the confusion
File

Loaded when

Put here

~/.bashrc

every interactive shell

aliases, functions, prompt, PATH
additions — 95% of your config

~/.profile

login shells (SSH, console)

environment vars needed by
GUI/login sessions

/etc/environment

system-wide, all users

global variables (no shell syntax
allowed!)

/etc/profile.d/*.sh

system-wide login

admin-installed additions for
everyone

A starter ~/.bashrc worth having





alias ll='ls -lah'
alias gs='git status'
alias ..='cd ..'
alias goodo='cd /mnt/d/GoOdo/GoOdo\ App'
mkcd() { mkdir -p "$1" && cd "$1"; }
extract() {
case "$1" in
*.tar.gz) tar -xzf "$1" ;;
*.zip) unzip "$1" ;;
*.gz) gunzip "$1" ;;
*) echo "unknown archive: $1" ;;
esac
}
export EDITOR=nano
export HISTSIZE=50000 HISTCONTROL=ignoredups

1. Aliases: short names for long commands.
2. Project shortcuts — one word to jump to GoOdo.
3. Functions beat aliases when arguments are needed: make-and-enter a directory.
4. A universal extractor — never google tar flags again.
5. Default editor for git/crontab prompts.
6. Huge history, no duplicate entries — makes Ctrl+R phenomenal. Apply changes with: source ~/.bashrc

PRACTICE EXERCISES
1. Add five aliases you'll actually use; live with them a week; delete the ones you didn't.
2. Trace your PATH and explain where python3 is found before and after activating a venv (use: type -a python3).
3. Write an alias vs a function for the same task with an argument — observe why the alias fails.





15. The Boot Process & the Kernel
What happens when you press power — the full chain
Stage

What happens

Where problems appear

1. UEFI/BIOS

Firmware self-tests hardware, finds a
boot disk

No disk found / boot order wrong

2. GRUB

The bootloader shows a menu, loads
the kernel into RAM

grub rescue> prompt after disk
changes

3. Kernel + initramfs

Kernel starts, uses a mini root
filesystem to load disk/LVM drivers

'Cannot find root device' —
fstab/UUID errors

4. systemd (PID 1)

Mounts real root, starts services in
dependency order

Boot hangs waiting for a failed unit

5. Targets reached

multi-user.target (server) or
graphical.target (desktop)

Login prompt appears

systemd-analyze
systemd-analyze critical-chain
systemctl get-default
sudo systemctl set-default multi-user.target
sudo systemctl reboot --boot-loader-entry=...

1. Total boot time split by stage (firmware / loader / kernel / userspace).
2. The dependency chain of the slowest path — which unit is holding up your boot.
3. Which target the system boots into.
4. Servers don't need a GUI target — save the RAM.
5. Advanced: reboot into a specific boot entry (older kernel) — recovery after a bad kernel update.

Rescue modes — your parachutes
# From the GRUB menu (hold Shift/Esc while booting):
# 'Advanced options' -> select older kernel
# Or edit an entry (e key) and append to the linux line:
systemd.unit=rescue.target
systemd.unit=emergency.target
init=/bin/bash

1. A previous kernel is kept precisely for the day the new one fails.
2. Rescue: minimal services, root shell, filesystems mounted — fix broken units/config.
3. Emergency: almost nothing started, root filesystem read-only — fix a broken fstab.
4. Nuclear option: bash as PID 1. Remount root writable with: mount -o remount,rw / — then repair passwd/fstab, and
reboot.

The kernel at runtime — modules and sysctl





uname -r
lsmod | head
sudo modprobe br_netfilter
lsmod | grep br_netfilter
sysctl net.ipv4.ip_forward
sudo sysctl -w net.ipv4.ip_forward=1
echo 'net.ipv4.ip_forward=1' | sudo tee /etc/sysctl.d/99-forward.conf

1. Running kernel version.
2. Loaded kernel modules — drivers loaded on demand.
3. Load a module manually (this one is needed by Docker/Kubernetes networking).
4. Verify.
5. Read a live kernel tunable — is this machine allowed to route packets?
6. Change it now (lost at reboot)...
7. ...and persist it. sysctl.d is where server tuning lives: swappiness, network buffers, file limits.
ulimit -n
# /etc/security/limits.d/goodo.conf
deploy soft nofile 65535
deploy hard nofile 65535

1. Max open files for your session — the default 1024 chokes busy servers ('Too many open files' errors).
2. Raise it per user via limits.d (for systemd services, set LimitNOFILE=65535 in the unit instead).

PRACTICE EXERCISES
1. Run systemd-analyze critical-chain and identify your slowest boot unit.
2. In a VM: deliberately add a bogus fstab line WITHOUT nofail, reboot into emergency mode, repair it, reboot
clean. This drill has saved countless real servers.
3. In a VM: boot with init=/bin/bash and change a user's password from there — now you know why physical access
= root access (and why disk encryption exists).
4. Persist vm.swappiness=10 via sysctl.d and verify it survives a reboot.





16. Terminal Multiplexing — tmux
Why tmux changes remote work
Problem: you SSH into a server, start a long job, your WiFi hiccups — the job dies with the connection. tmux
runs your terminal sessions on the server, detached from the connection. Disconnect, reconnect from
another machine, and everything is exactly where you left it: running processes, split panes, scrollback. It is
non-negotiable for server work.

The core workflow
tmux new -s deploy
# ... work happens, connection dies ...
tmux ls
tmux attach -t deploy
tmux kill-session -t deploy

1. Create a named session — always name them.
2. The processes inside keep running through any disconnect.
3. List sessions on this machine after you reconnect.
4. Re-enter exactly where you were. This resilience alone justifies tmux.
5. Clean up when finished.

The prefix and the essential keys
Every tmux command starts with the prefix: Ctrl+b, then a key. Muscle memory forms within two days of
forced use.
Keys (after Ctrl+b)

Action

d

Detach — leave everything running, return to your normal
shell

c

New window (like a browser tab)

n / p / 0-9

Next / previous / jump to window number

%

Split pane vertically (side by side)

"

Split pane horizontally (stacked)

arrow keys

Move between panes

z

Zoom: current pane fullscreen; z again to restore

x

Kill current pane

[

Scroll mode — arrows/PgUp to read history, q to exit

s

Interactive session switcher

A practical layout for server work





tmux new -s goodo
# pane 1: Ctrl+b % -> journalctl -u goodo -f
# pane 2: Ctrl+b " -> htop
# pane 3: your working shell

1. One session per project.
2. Left pane: live application logs.
3. Bottom-right: system monitor.
4. Main pane: where you actually type. The whole cockpit survives disconnects and is waiting tomorrow.

A sane ~/.tmux.conf starter
set -g mouse on
set -g history-limit 50000
set -g base-index 1
setw -g mode-keys vi
bind r source-file ~/.tmux.conf \; display "Reloaded"

1. Mouse selects panes, resizes, scrolls — eases the learning curve.
2. Deep scrollback for reading long logs.
3. Windows numbered from 1 (matches keyboard layout).
4. vi keys in scroll mode — /search your scrollback like in less.
5. Prefix+r reloads config without restarting.

WARNING: Long operations on servers — database migrations, big rsyncs, apt full-upgrades over SSH — belong
inside tmux, always. An upgrade killed halfway by a dropped connection can leave a system unbootable.
PRACTICE EXERCISES
1. Create a session, start ping google.com, detach, close your terminal ENTIRELY, reopen, attach — verify ping
never stopped.
2. Build the three-pane cockpit for any service and use it during one real work session.
3. Practice prefix+z zoom while reading logs — it becomes your most-used binding.
4. Install the config above and reload it live with prefix+r.





17. Vim — Editing at the Speed of Thought
The philosophy: a language, not shortcuts
Vim commands compose like grammar: verb + count + noun. d=delete, 3=three, w=words → d3w deletes
three words. Learn ~10 verbs and ~10 nouns and you can speak hundreds of edits. This is why vim survives
30+ years: it isn't memorization, it's a language.

The modes
Mode

Enter with

For

Normal

Esc

Navigating and editing commands —
HOME BASE, return here constantly

Insert

iaoO

Actually typing text

Visual

v V Ctrl+v

Selecting (character / line / block)

Command

:

Save, quit, search-replace, settings

Movement (the nouns)
h j k l
w b e
0 ^ $
gg G 42G
{ }
f, t)
Ctrl+d Ctrl+u
/error n N

1. Left, down, up, right — hands never leave home row.
2. Word forward / word back / end of word.
3. Line start / first character / line end.
4. File top / file bottom / jump to line 42.
5. Previous / next empty line (paragraph jumps).
6. Jump onto the next comma / just before the next ) — surgical.
7. Half-page down / up.
8. Search forward; n = next match, N = previous. Navigation IS search in vim.

Editing (verbs + grammar in action)





dw d$ dd 3dd
cw ciw ci" ci(
yy yw p P
u Ctrl+r .
x r" >> <<

1. Delete: word / to line end / whole line / three lines.
2. Change (delete+insert): word / inner word (anywhere inside it!) / inside quotes / inside parentheses — ci" edits a
string's contents in one stroke regardless of cursor position within it.
3. Yank (copy): line / word; paste after / before cursor.
4. Undo / redo / and the mighty dot: REPEAT the last change — fix one, then press . at each next spot.
5. Delete char / replace char with " / indent / unindent line.

Command-mode power
:w :q :wq :q!
:%s/localhost/127.0.0.1/g
:%s/DEBUG/INFO/gc
:g/^#/d
:5,20y
:!ls
:r !date

1. Save / quit / both / quit discarding changes.
2. Search-replace across the whole file (% = all lines) — sed, inside your editor.
3. c flag: confirm each replacement interactively.
4. Delete every comment line — :g runs a command on all matching lines.
5. Yank lines 5–20.
6. Run any shell command without leaving.
7. Insert a command's output at the cursor — pull dates, IPs, file lists straight into your document.

A humane ~/.vimrc
set number relativenumber
set tabstop=4 shiftwidth=4 expandtab
set ignorecase smartcase
set hlsearch incsearch
syntax on
set undofile

1. Absolute number on current line, relative elsewhere — makes counts like 5j effortless.
2. 4-space indentation, spaces not tabs (Python-friendly).
3. Case-insensitive search UNLESS you type a capital.
4. Highlight matches; search as you type.
5. Colors.
6. Persistent undo — undo history survives closing the file. A quiet superpower.

PRO INSIGHT: The 30-day method: week 1 use vim only for git commit messages and tiny configs. Week 2 add ci(,
ci", and the dot command. Week 3 do real edits on the server. Week 4 you stop thinking about it. Speed follows
automatically.





PRACTICE EXERCISES
1. Complete vimtutor lessons 1–4 (it ships with vim; ~40 minutes total).
2. Open any config and practice: ci" on a value, dd + p to move a line down, %s to rename something everywhere.
3. Edit three values on separate lines using ONLY: /search, ciw, Esc, n, and the dot command.
4. Install the .vimrc and test persistent undo: change a file, :wq, reopen, press u.





18. WSL Mastery — Linux Inside Windows
What WSL2 actually is
WSL2 runs a real Linux kernel in a lightweight VM, with deep Windows integration: shared clipboard,
network, and cross-mounted filesystems. It is a genuine Linux — everything in this book applies — with a few
boundary rules worth mastering since it is your daily GoOdo development environment.

Managing WSL from Windows (PowerShell)
wsl --list --verbose
wsl --shutdown
wsl --terminate Ubuntu
wsl --export Ubuntu D:\backups\ubuntu.tar
wsl --import Ubuntu-Dev D:\wsl\dev D:\backups\ubuntu.tar
wsl --update

1. Installed distros, their state, and WSL version.
2. Full restart of the WSL VM — the fix for most WSL weirdness (network gone, clock drift after sleep).
3. Stop one distro only.
4. FULL BACKUP of your entire Linux system into one tar — do this before risky experiments.
5. Restore as a clone — instant disposable lab that mirrors your real setup.
6. Update the WSL kernel itself.

The filesystem boundary — the #1 performance rule
Location

What it is

Speed for Linux tools

~ (ext4, inside WSL)

Native Linux filesystem

FAST — keep code, git repos,
node_modules here

/mnt/c, /mnt/d

Windows drives via 9P bridge

SLOW for many-small-files work (git
status, builds can be 10x slower)

\\wsl$\Ubuntu\home\...

Linux files seen from Windows
Explorer

How Windows apps reach your Linux
files

PRO INSIGHT: Your GoOdo project lives at /mnt/d — Flutter builds and git operations there pay the 9P tax on
every file. Ideal setup: repo cloned inside ~ for speed; Windows-side tools access it via \\wsl$. If you must keep it on
D:, at least run flutter pub get and gradle builds from Windows-side tooling.

Windows ↔ Linux interop tricks





explorer.exe .
code .
notepad.exe file.txt
cmd.exe /c dir
cat report.md | clip.exe
powershell.exe -c "Get-Process" | head
wslpath 'D:\GoOdo\GoOdo App'
adb devices

1. Open the CURRENT Linux directory in Windows Explorer — the dot matters.
2. VS Code with the WSL extension: Windows UI, Linux backend — the best of both.
3. Any .exe runs from bash.
4. Even cmd built-ins.
5. Pipe Linux output straight into the Windows clipboard.
6. PowerShell output flows back into Linux pipes — the two worlds compose.
7. Convert Windows paths to WSL paths ( → /mnt/d/GoOdo/GoOdo App).
8. Windows-side adb is visible in PATH — how your OnePlus connects to Flutter inside WSL.

systemd, services and networking in WSL
# /etc/wsl.conf
[boot]
systemd=true
[automount]
options = "metadata"
# Windows side: %UserProfile%\.wslconfig
[wsl2]
memory=6GB
processors=4
localhostForwarding=true

1. Per-distro config, inside Linux:
2. Enable real systemd — systemctl, services and timers work exactly as in this book (restart WSL after).
3. metadata lets chmod/chown work properly on /mnt drives.
4. Global VM config, on the Windows side:
5. Cap WSL's RAM (it happily eats everything for file cache).
6. CPU cores for the VM.
7. localhost:8000 in a Windows browser reaches your FastAPI dev server inside WSL automatically.

WSL gotchas and their fixes
Symptom

Cause

Fix

bad interpreter: ^M

Script saved with Windows line
endings

dos2unix file.sh (or the tr -d '\r' trick
from Ch. 5)

Clock wrong after laptop sleep

VM clock drift

sudo hwclock -s or wsl --shutdown

Permissions all 777 on /mnt/d

Windows drives don't store Linux
perms

metadata option in wsl.conf (above)





Symptom

Cause

Fix

git thinks every file changed

Line-ending translation

git config --global core.autocrlf input

DNS broken on some VPNs

resolv.conf regeneration conflicts

See [network] generateResolvConf
option in wsl.conf

PRACTICE EXERCISES
1. Export a full backup of your Ubuntu distro to D:\backups (then you may experiment fearlessly forever).
2. Benchmark truth: time (git status) for a repo in ~ vs the same repo on /mnt/d.
3. Enable systemd in wsl.conf and install a working systemd timer from Ch. 7 inside WSL.
4. Import a clone as Ubuntu-Lab and break it on purpose — practice Ch. 15's emergency-mode repair there.





19. Containers — Docker on Linux
What a container really is (now you can understand it)
A container is not a VM. It is a normal Linux process that the kernel isolates using namespaces (its own
view of PIDs, network, filesystem mounts, hostname) and limits using cgroups (CPU/RAM caps). One
kernel, many isolated userspaces. That's why containers start in milliseconds and why everything you've
learned — processes, permissions, networking — applies inside them.
docker run -d --name web -p 8080:80 nginx
docker ps
docker exec -it web bash
docker logs -f web
docker stats
docker stop web && docker rm web

1. Run detached, name it, map host port 8080 → container port 80. Image auto-downloads.
2. Running containers (add -a for stopped ones).
3. A shell INSIDE the container — note the alien hostname and lonely process list: namespaces made visible.
4. The container's stdout is its log — follow live.
5. Live CPU/RAM per container — cgroups made visible.
6. Graceful stop (SIGTERM, then KILL after 10 s) and removal.

Images and Dockerfiles — a production FastAPI example
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN useradd -m appuser
USER appuser
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

1. Base image: slim = Debian minus the fat.
2. Working directory inside the image.
3. Copy ONLY requirements first...
4. ...so this expensive layer is CACHED and re-runs only when requirements change — the single most important
Dockerfile optimization.
5. Now the code (changes often, cheap layer).
6. Create a non-root user...
7. ...and drop privileges — Ch. 14's principles apply inside containers too.
8. Documented port.
9. The process to run. Exec-form (JSON array) lets signals reach uvicorn properly for clean shutdowns.





docker build -t goodo-api:1.2 .
docker image ls
docker run --rm --env-file .env -p 8000:8000 goodo-api:1.2

1. Build and tag with a version.
2. Your local image library with sizes.
3. --rm auto-cleans on exit; --env-file injects secrets the 12-factor way (never bake them into images).

Compose — whole stacks as one file
# docker-compose.yml
services:
api:
build: .
ports: ["8000:8000"]
env_file: .env
depends_on: [db]
restart: unless-stopped
db:
image: postgres:16
environment:
POSTGRES_PASSWORD: ${DB_PASS}
volumes:
- pgdata:/var/lib/postgresql/data
volumes:
pgdata:

1. Your app, built from the local Dockerfile.
2. Start order hint: db first.
3. Docker's own supervisor — the container equivalent of Restart= in systemd units.
4. Official PostgreSQL, pinned to major version 16.
5. Variable interpolated from a .env file next to the compose file.
6. THE critical line: a named volume keeps database files when containers are rebuilt. No volume = data dies with the
container.
docker compose up -d
docker compose logs -f api
docker compose exec db psql -U postgres
docker compose down
docker compose down -v

1. The whole stack, one command. This is how eQuorum ships to bank servers.
2. Follow one service's logs.
3. psql straight into the containerized database.
4. Stop and remove containers — volumes SURVIVE.
5. -v also deletes volumes — the data-destroying flag; respect it like rm -rf.

Housekeeping and debugging





docker system df
docker system prune -a
docker inspect web | jq '.[0].NetworkSettings.IPAddress'
docker run -it --entrypoint bash goodo-api:1.2

1. How much disk images/containers/volumes consume — Docker silently eats tens of GB over months.
2. Reclaim it: removes stopped containers, unused images and networks (add --volumes carefully).
3. Everything Docker knows about a container, queryable with jq.
4. Debug an image that crashes at startup: override the entrypoint and poke around inside.

PRACTICE EXERCISES
1. Run nginx, enter it with exec, and compare ps aux inside vs outside — see namespace isolation with your own
eyes.
2. Containerize any FastAPI app with the Dockerfile above; verify a code-only change rebuilds in seconds (layer
cache).
3. Bring up the compose stack, write a row to Postgres, docker compose down, up again — prove the volume kept
your data.
4. Cap a container with --memory=100m, stress it, and watch Docker's OOM handling in docker inspect.





20. Database Administration — PostgreSQL on Linux
Install and first contact
sudo apt install postgresql
systemctl status postgresql
sudo -u postgres psql
postgres=# \l
postgres=# \du
postgres=# \q

1. The database plus its systemd service, auto-started and enabled.
2. It runs as a service like anything else — everything from Ch. 7 applies.
3. Postgres trusts the LOCAL UNIX USER 'postgres' — so you become that user to enter as superuser (peer
authentication).
4. List databases (backslash commands are psql's control language).
5. List roles (users) and their privileges.
6. Leave.

Creating an application database — the correct minimal-privilege setup
sudo -u postgres psql <<'SQL'
CREATE ROLE goodo_app LOGIN PASSWORD 'use-a-long-random-one';
CREATE DATABASE goodo OWNER goodo_app;
\c goodo
REVOKE ALL ON SCHEMA public FROM PUBLIC;
GRANT ALL ON SCHEMA public TO goodo_app;
SQL

1. A heredoc feeds SQL from a script — automatable setup.
2. One dedicated role per application, never superuser.
3. The app owns only ITS database.
4. Switch into it...
5. ...and remove the historic default that let any role create tables in public.
6. The app role gets its schema. Least privilege from day one.

The two files that control access





# postgresql.conf
listen_addresses = 'localhost'
max_connections = 100
# pg_hba.conf (read top-down, first match wins)
local all postgres peer
host goodo goodo_app 127.0.0.1/32 scram-sha-256
sudo systemctl reload postgresql

1. Both live in /etc/postgresql/16/main/.
2. Bind local only — remote access via SSH tunnel (Ch. 10), never an open 5432.
3. Connection cap — each one costs RAM.
4. HBA = host-based authentication, the door policy:
5. Local socket, postgres role, trusted by Unix identity.
6. TCP from localhost, only the goodo db, only its role, modern password hashing.
7. reload (not restart) applies HBA changes with zero downtime.

Backups — the part that defines you as an admin
sudo -u postgres pg_dump -Fc goodo > /backups/goodo_$(date +%F).dump
sudo -u postgres pg_dumpall --globals-only > /backups/roles.sql
pg_restore -l /backups/goodo_2026-07-02.dump | head
sudo -u postgres createdb goodo_restore
sudo -u postgres pg_restore -d goodo_restore /backups/goodo_2026-07-02.dump

1. -Fc = compressed custom format: smaller, and restorable table-by-table.
2. Roles and passwords are NOT in pg_dump — capture them separately or restores land on a system with no users.
3. Peek inside a dump without restoring — also verifies it isn't corrupt.
4. Restore drill into a scratch database...
5. ...because an untested backup is a hope, not a backup. Schedule the dump with a systemd timer (Ch. 7) and
test-restore monthly.

Health and performance queries every admin knows
SELECT pid, state, now()-query_start AS age, left(query,50)
FROM pg_stat_activity WHERE state != 'idle' ORDER BY age DESC;
SELECT pg_size_pretty(pg_database_size('goodo'));
SELECT relname, n_live_tup, n_dead_tup
FROM pg_stat_user_tables ORDER BY n_dead_tup DESC LIMIT 5;
SELECT pg_terminate_backend(12345);

1. Who is running what, for how long — find the stuck query behind 'the app is slow'.
2. Database size, human readable.
3. Dead tuples = bloat awaiting autovacuum; huge numbers explain slow tables.
4. Kill one misbehaving query by pid — the database's kill command.





PRO INSIGHT: The same skills run inside Docker (Ch. 19): docker compose exec db pg_dump... The tools are
identical; only the doorway differs. For eQuorum's on-premise installs at banks, this chapter IS your operations
manual.
PRACTICE EXERCISES
1. Build the least-privilege setup for a test app; prove the app role cannot read another database.
2. Break login on purpose: set a wrong HBA method, read the exact error from journalctl -u postgresql, fix it.
3. Automate the nightly dump with a systemd timer, then perform a full restore drill into goodo_restore.
4. Run the stuck-query view while a second psql session sits inside an open transaction — find and terminate it.





21. Advanced Networking & Firewalls
Static IPs with netplan (Ubuntu)
# /etc/netplan/01-static.yaml
network:
version: 2
ethernets:
eth0:
addresses: [192.168.1.50/24]
routes:
- to: default
via: 192.168.1.1
nameservers:
addresses: [1.1.1.1, 9.9.9.9]
sudo netplan try

1. Netplan: YAML that generates the actual network config.
2. Fixed address with CIDR mask (/24 = 255.255.255.0).
3. Default gateway.
4. DNS servers.
5. netplan try applies AND AUTO-REVERTS in 120 s unless you confirm — the seatbelt that prevents locking yourself
out of a remote machine with a bad network config. Never use plain 'apply' remotely.

Under ufw's hood — nftables/iptables literacy
ufw is a friendly front-end; the kernel's real firewall is nftables (successor to iptables). You don't need to write
raw rules often, but you must be able to READ them when debugging 'why is this blocked?' — especially
since Docker inserts its own rules that bypass ufw.
sudo nft list ruleset | less
sudo iptables -L -n -v | head -30
sudo iptables -t nat -L -n

1. The complete live ruleset — search for your port number when hunting a block.
2. Legacy view many tools still use: chains INPUT/FORWARD/OUTPUT with packet counters — counters incrementing
on a DROP rule = found your culprit.
3. The NAT table — where Docker's port mappings live. THE gotcha: docker run -p 5432:5432 publishes to the world
even with ufw denying it, because Docker's NAT rules run first. Bind consciously: -p 127.0.0.1:5432:5432.

WARNING: Memorize the Docker/ufw trap: published container ports bypass ufw. Always publish sensitive ports
bound to 127.0.0.1, or configure Docker's iptables integration explicitly. Countless 'hardened' servers have leaked
databases this way.

DNS — a working mental model plus tools





resolvectl status | head -15
dig goodo.app A +short
dig goodo.app MX
dig @1.1.1.1 goodo.app
dig +trace goodo.app | tail -8
dig -x 95.216.1.2

1. Who answers this machine's DNS queries (systemd-resolved's view).
2. Address record, terse.
3. Mail servers for the domain.
4. Ask a SPECIFIC resolver — distinguishes 'my DNS is stale' from 'the record is wrong'.
5. Follow the full delegation root → TLD → authoritative server — see the hierarchy that runs the internet.
6. Reverse: name for an IP.

Record TTLs explain 'the DNS change hasn't worked yet': resolvers cache answers for the TTL. Before
migrations, drop TTL to 300 a day early; raise it back after.

Traffic inspection — tcpdump essentials
sudo tcpdump -i any -nn port 8000 -c 20
sudo tcpdump -i any -nn 'tcp[tcpflags] & tcp-syn != 0' -c 10
sudo tcpdump -i any -nn -w capture.pcap port 5432

1. Watch 20 packets on the API port: SEE requests arrive (or prove they never do — instantly splitting 'network problem'
from 'app problem').
2. Only connection attempts (SYN packets) — who is trying to connect right now?
3. Write raw capture to a file — open it later in Wireshark on your laptop for full protocol dissection.

Bandwidth and quality
sudo apt install iperf3
iperf3 -s # on server
iperf3 -c server-ip # on client
mtr goodo.app

1. The standard throughput tester.
2. One side listens...
3. ...the other measures real achievable bandwidth between them — settles 'is the network slow?' with numbers.
4. traceroute+ping combined, live: per-hop loss and latency. The hop where loss begins is where the problem lives
(great evidence for provider tickets).

PRACTICE EXERCISES
1. In a VM: set a static IP with netplan try, deliberately typo the gateway, and watch the auto-revert rescue you.
2. Reproduce the Docker/ufw trap: publish a port with ufw denying it, prove outside reachability, then fix with a
127.0.0.1 bind.
3. Run dig +trace on your own domain and name each delegation step.
4. With tcpdump running on port 8000, curl your API and read the SYN/ACK handshake in the output.





22. Debugging Like an Expert — strace, lsof, /proc
The principle: stop guessing, start observing
Experts don't guess why a program misbehaves — they watch it talk to the kernel. Every meaningful action a
process takes (open a file, connect a socket, read config) is a system call, and Linux lets you watch them all.

strace — the truth serum
strace -f -e trace=openat,connect python3 app.py 2>&1 | grep -v ENOENT | head
strace -f -e openat python3 app.py 2>&1 | grep -E "\.conf|\.env|\.yaml"
strace -p 1123 -e trace=network -f
strace -c ls /usr/bin

1. Trace file-opens and connections: instantly answers 'WHICH config file is it actually reading?' and 'WHERE is it trying
to connect?' — the two eternal questions.
2. The classic: find every config-like file the app touches — ends all 'but I edited the config!' mysteries (it was reading a
different one).
3. Attach to a RUNNING process and watch only its network calls — is the hung backend waiting on the database?
4. Syscall statistics summary — a profile of what the program spends kernel time doing.
OUTPUT

openat(AT_FDCWD, "/opt/goodo/.env", O_RDONLY) = 3
connect(4, {sa_family=AF_INET, sin_port=htons(4000),
sin_addr=inet_addr("18.156.x.x")}, 16) = -1 ETIMEDOUT

Read the story: it opened .env successfully (returned file descriptor 3), then tried TiDB on port 4000 and
timed out. Diagnosis in two lines: the config loads fine; the network path to the database is the problem. No
print-statements needed.

lsof — who holds what
sudo lsof -p 1123 | head -20
sudo lsof -i :8000
sudo lsof /mnt/data
sudo lsof +L1 | head
sudo lsof -u deploy -i

1. Everything a process holds open: files, sockets, libraries — its complete grip on the system.
2. Which process owns a port — 'address already in use', solved.
3. Which processes hold files on a mount — 'umount: target is busy', solved.
4. Deleted files still held open (+L1): THE hidden-disk-space classic — df says full, du can't find it, because a process
still holds a deleted giant log. Restart the process to free it.
5. All network activity of one user.

/proc — interrogating a live process





ls -l /proc/1123/cwd /proc/1123/exe
cat /proc/1123/environ | tr '\0' '\n' | head
ls -l /proc/1123/fd | head
cat /proc/1123/status | grep -E "VmRSS|Threads"
cat /proc/1123/limits | grep "open files"

1. Its ACTUAL working directory and binary — not what you assume, what IS.
2. The environment it REALLY started with (null-separated) — 'did the service get my env var?' answered definitively.
3. Its open file descriptors as symlinks — lsof's raw source.
4. Real memory (VmRSS) and thread count.
5. The limits it actually runs under — service limits (Ch. 15) verified from the inside.

When it's slow, not broken
cat /proc/1123/stack
perf top
time curl -s https://api/endpoint -o /dev/null
curl -w "dns:%{time_namelookup} conn:%{time_connect} ttfb:%{time_starttransfer}\n" -o
/dev/null -s https://api/endpoint

1. Kernel-side stack of a hung process — what is it BLOCKED on (disk? lock? network?).
2. Live system-wide profiler: which functions across ALL processes burn CPU right now (apt install linux-tools-common).
3. Total request duration.
4. The professional version — split into DNS, TCP connect, and time-to-first-byte: the slow phase names the guilty layer
(DNS server / network path / the application itself).

PRACTICE EXERCISES
1. strace a program with a deliberately missing config; find the exact failing openat and the paths it searched.
2. Create the hidden-space scenario: write a big file from a background process, rm it, prove df/du disagree, find it
with lsof +L1, free it.
3. Compare /proc/PID/environ of a systemd service against your shell env — see why services 'don't get' your
variables.
4. Use the curl timing breakdown on three websites and interpret each phase.





23. Troubleshooting Scenarios — Ten Real Incidents
Each scenario below is a real-world pattern. Cover the resolution, work it from the symptom yourself, then
read on. This chapter is the book's dojo.

Scenario 1 — 'The website is down'
systemctl status nginx goodo # both active?
sudo ss -tulpn | grep -E ':80|:8000' # both listening?
curl -s localhost:8000/health # app OK locally?
curl -sI localhost # nginx OK locally?
journalctl -u goodo -n 30 # if not: why?

1. Layered elimination, inside-out: service states...
2. ...ports bound...
3. ...app answers on loopback...
4. ...proxy answers on loopback. If all four pass, the problem is OUTSIDE: firewall, DNS, or provider.
5. First failing layer → its logs hold the answer.

Scenario 2 — 'Disk full' (df says 100%)
df -h # which filesystem?
sudo du -xh --max-depth=2 / 2>/dev/null | sort -rh | head
sudo lsof +L1 # deleted-but-held files?
journalctl --disk-usage # journal bloat?
sudo apt clean

1. Locate the full mount.
2. -x stays on ONE filesystem (don't descend into /mnt): find the heavy directories.
3. The Ch. 22 classic if du can't account for the space.
4. Usual suspects: journals, apt cache, old logs, forgotten backups on the root disk.
5. Quick wins, then fix the CAUSE: logrotate config, journald caps, backups moved off-disk.

Scenario 3 — 'I'm locked out of SSH'
Console access (cPouta/Hetzner web console) is your back door — this is why providers offer it. From the
console: check sshd is running, check ufw status didn't lose the OpenSSH rule, read /var/log/auth.log for the
refusal reason, verify ~/.ssh permissions (700/600), and check fail2ban didn't ban YOUR home IP
(fail2ban-client status sshd → unban). Prevention: before restarting sshd with new config, always validate
with sshd -t and keep one session open.

Scenario 4 — 'It works in my shell but fails in cron/systemd'
journalctl -u myjob -n 20
sudo -u deploy env -i /bin/bash --noprofile --norc -c '/opt/scripts/job.sh'

1. Read the actual error first.
2. Reproduce the service's world: correct user, EMPTY environment, no rc files. 90% of these bugs are PATH
assumptions, missing env vars, or relative paths — fix by absolute paths + EnvironmentFile + WorkingDirectory.





Scenario 5 — 'The server is suddenly slow'
Run the Ch. 13 triage in order. Decision tree: load high + %us high → a process burns CPU (top names it).
Load high + %wa high → disk (iostat; find the writer with iotop). si/so nonzero in vmstat → swapping (memory
pressure; find the eater, add RAM/swap). Load LOW but app slow → not the machine: database queries (Ch.
20 stuck-query view), external API latency (curl timing breakdown), or connection pool exhaustion.

Scenario 6 — 'Permission denied' that makes no sense
namei -l /opt/goodo/backend/.env
sudo -u deploy cat /opt/goodo/backend/.env
getfacl /opt/goodo/backend/.env

1. The killer tool: shows permissions of EVERY path component — a 700 directory anywhere upstream blocks access
to a perfectly readable file (missing x on a parent dir is the classic invisible cause).
2. Test as the ACTUAL user in question, not as root (root bypasses everything and hides the bug).
3. ACLs can add rules invisible to ls -l — check when normal perms look correct.

Scenario 7 — 'apt is broken'
sudo dpkg --configure -a
sudo apt -f install
sudo rm /var/lib/apt/lists/lock /var/lib/dpkg/lock* # ONLY if no apt runs
sudo apt update

1. Finish interrupted package configuration (the state after a mid-upgrade disconnect — which tmux, Ch. 16, prevents).
2. Repair broken dependencies.
3. Stale locks after a crash — verify with ps aux | grep -E 'apt|dpkg' that nothing runs before removing.
4. Rebuild indexes. This four-line sequence resurrects most broken package systems.

Scenario 8 — 'The service restarts in a loop'
systemctl status goodo
journalctl -u goodo --since -10m | grep -B2 -A8 "Traceback\|error"
systemctl show goodo -p Restart,RestartSec,NRestarts
sudo systemd-run --uid=deploy --pty /opt/goodo/venv/bin/uvicorn main:app

1. Status shows 'activating (auto-restart)' and the exit code.
2. The crash reason with context — usually the FIRST error, not the last.
3. How many restarts systemd has attempted.
4. Run it interactively under systemd's own conditions — crashes now happen in front of your eyes.

Scenario 9 — 'DNS changed but the site shows the old server'
Check propagation from multiple resolvers: dig @1.1.1.1, dig @8.8.8.8, and your local resolver — differences
= caching still expiring (that TTL you should have lowered in advance, Ch. 21). Flush local: resolvectl
flush-caches. Remember browsers keep their own cache too. Meanwhile verify the NEW server answers by
forcing the connection: curl --resolve goodo.app:443:NEW_IP https://goodo.app — tests the future before
DNS agrees.

Scenario 10 — 'Certificate expired'




echo | openssl s_client -connect goodo.app:443 2>/dev/null | openssl x509 -noout -dates
sudo certbot renew --dry-run
systemctl list-timers | grep certbot
sudo certbot renew --force-renewal && sudo systemctl reload nginx

1. Read the live certificate's validity dates from outside.
2. Test the renewal machinery without touching anything — run this the day you SET UP certbot, not the day it fails.
3. The renewal timer should exist and be waiting.
4. The emergency fix, plus reload so nginx serves the new cert. Root causes are usually: port 80 blocked, changed
DNS, or a broken renewal hook.

PRO INSIGHT: Across all ten scenarios one method repeats: observe (logs, status, probes) → isolate the failing
layer → reproduce minimally → fix the cause, not the symptom → write the incident down. Your incident notes
become the runbook that makes the next occurrence a two-minute fix.
PRACTICE EXERCISES
1. Stage scenarios 1, 2, 6 and 8 in a VM (break it yourself), then resolve each from the symptom without peeking.
2. Run namei -l on a deep path and explain each line.
3. Time yourself on scenario 4: create a script that works in shell, install it as a failing service, fix it properly.
4. Start an incident journal today: date, symptom, diagnosis path, root cause, fix, prevention. Five entries in, you'll
feel the difference.





13. Logs, Monitoring & Performance Debugging
The USE method — how experts think
For every resource (CPU, memory, disk, network) check three things: Utilization (how busy), Saturation (how
much is queued waiting), Errors. A resource can show low utilization yet be saturated — the method catches
what intuition misses.

The 60-second triage, annotated
uptime
dmesg -T | tail -20
free -h
vmstat 1 5
top -o %CPU
iostat -xz 1 3
ss -s

1. Load average 1/5/15 min. Load 8 on a 4-core box = 2x oversubscribed. Rising left-to-right = getting worse.
2. Recent kernel events with timestamps: OOM kills, disk errors, network flaps — the machine's own testimony.
3. 'available' is the truth about memory. Swap 'used' growing steadily = memory pressure.
4. System pulse per second: r column = processes waiting for CPU (saturation!), si/so = swapping actively (bad), wa =
CPU idle waiting for disk.
5. Name the CPU culprit.
6. Disk: %util near 100 and await high = disk is the bottleneck.
7. Socket summary — thousands of connections where you expect dozens tells its own story.

Interpreting a real incident
OUTPUT

$ free -h
total used free shared buff/cache available
Mem: 1.9Gi 1.7Gi 80Mi 12Mi 190Mi 89Mi
Swap: 0B 0B 0B
$ dmesg -T | grep -i oom
[Thu Jul 2 03:12:44] Out of memory: Killed process 1123 (uvicorn)

Diagnosis in two commands: 89 Mi available, no swap, and the kernel confesses it killed uvicorn at 03:12.
Root cause: memory exhaustion. Fixes, in order: add swap (Ch. 9), cap the service's memory in its unit
(MemoryMax=1G makes systemd restart it gracefully instead), find the leak (Ch. 13 tools), or upsize the VPS.

journalctl — the complete query language





journalctl -u goodo --since today
journalctl -u goodo -p warning --since "2 days ago"
journalctl _PID=1123
journalctl -u goodo -o json-pretty -n 1
journalctl -f -u goodo -u nginx

1. One service, today only.
2. Only warnings and worse in a time window — cut the noise.
3. Everything one specific process ever logged.
4. Structured output — every log entry carries rich metadata worth seeing once.
5. Follow TWO services interleaved — watch a request flow from nginx into your app live.

Log rotation — why servers don't drown
# /etc/logrotate.d/goodo
/var/log/goodo/*.log {
daily
rotate 14
compress
delaycompress
missingok
notifempty
copytruncate
}

1. Drop a config per app into logrotate.d — it runs daily via systemd timer.
2. Rotate daily...
3. ...keep 14 generations...
4. ...gzip old ones (delaycompress leaves the newest uncompressed for easy reading).
5. Don't error if absent; skip empty files.
6. copytruncate lets the app keep writing to the same file handle — for apps that don't reopen logs on rotation.

Watching over time — lightweight and free
sudo apt install sysstat
sar -r | tail -5
sar -q -f /var/log/sysstat/sa01

1. sysstat records system metrics every 10 minutes automatically.
2. Memory history for today — 'was it already degrading this morning?'
3. Load history from the 1st of the month — performance archaeology. For dashboards later: Netdata (one-command
install) or Prometheus+Grafana.

PRACTICE EXERCISES
1. Run the full triage on your machine while idle; save the outputs as your baseline; repeat under load (stress --cpu
2) and compare.
2. Simulate memory pressure in a VM (stress --vm 2 --vm-bytes 1G), catch the OOM kill in dmesg.
3. Write a logrotate config for a fake app log, force it with logrotate -f, verify the rotation chain.
4. Set MemoryMax=200M on a test service, make it exceed the limit, observe systemd's handling in journalctl.





14. Security Hardening — The Professional Standard
Threat model of a public server
Within minutes of getting a public IP, automated scanners probe: SSH password guessing (thousands/day),
known CVE exploits against web software, and misconfiguration hunting (open databases, .env files served
by the webserver, .git directories exposed). Hardening defeats the automated 99%; the remaining 1% is
defeated by patching fast.

The first hour — complete, in order
# 1. as root on the fresh VPS:
adduser deploy && usermod -aG sudo deploy
rsync -a ~/.ssh /home/deploy/ && chown -R deploy: /home/deploy/.ssh
# 2. TEST in a NEW terminal:
ssh deploy@server sudo whoami # must print: root
# 3. lock the doors — /etc/ssh/sshd_config.d/hardening.conf:
PermitRootLogin no
PasswordAuthentication no
MaxAuthTries 3
sudo systemctl restart ssh
# 4. firewall:
sudo ufw default deny incoming
sudo ufw allow OpenSSH && sudo ufw allow 80,443/tcp
sudo ufw enable
# 5. automatic defense:
sudo apt install -y fail2ban unattended-upgrades
sudo dpkg-reconfigure -plow unattended-upgrades

1. Admin user.
2. Copy root's authorized key to the new user with correct ownership.
3. The golden rule: VERIFY the new access path works BEFORE closing the old one. Keep the root session open until
this prints 'root'.
4. Drop-in config directory — survives upgrades better than editing the main file.
5. No root logins.
6. Keys only.
7. Three strikes per connection.
8. Apply.
9. Default deny.
10. SSH first (or you're locked out), then web.
11. Enable.
12. Ban brute-forcers; auto-install security patches.
13. Enable the auto-updates in one prompt. Total time: ~15 minutes. This blocks the vast majority of real-world
compromises.

Verifying your defenses




sudo fail2ban-client status sshd
sudo grep "Failed password" /var/log/auth.log | wc -l
sudo lastb | head
last -20
sudo ss -tulpn | grep -v "127.0.0.1"

1. Currently banned IPs — a public server will show hits within hours.
2. Count of failed login attempts — feel the background radiation of the internet.
3. The failed-login log itself: usernames attackers guessed (admin, root, test, oracle...).
4. Successful logins — anything you don't recognize is an incident.
5. Services listening on PUBLIC interfaces. Everything here is attack surface; databases should show only 127.0.0.1.

Application-level hygiene
# .env handling
chmod 600 .env && chown deploy: .env
grep -r "SECRET\|PASSWORD" --include="*.py" /opt/goodo | grep -v ".env"
# nginx: never serve dotfiles
location ~ /\. { deny all; }
# database: bind local only (postgresql.conf)
listen_addresses = 'localhost'

1. Secrets file: one owner, no group/world access.
2. Audit for hardcoded secrets that should be in .env — run before every git push.
3. One nginx line prevents the classic .env / .git leak through the webserver.
4. PostgreSQL reachable only from the machine itself; remote access goes through SSH tunnels (Ch. 10).

When you suspect a compromise
ps auxf | less
sudo ss -tp | grep -v "your-ip"
crontab -l; sudo ls /etc/cron*; systemctl list-timers
find / -mtime -2 -type f 2>/dev/null | grep -vE "^/(proc|sys|var/log)" | head -50
last -50

1. Full process forest — unknown processes, especially with strange names or from /tmp.
2. Outbound connections you didn't create (crypto-miners phone home).
3. Persistence check: attackers install cron jobs and timers to survive reboots.
4. Files changed in the last 2 days outside the noisy areas.
5. Login history. Real answer if confirmed: assume total compromise — rebuild the server from scratch and restore data
from backups. Cleaning in place is a losing game.

PRACTICE EXERCISES
1. Perform the complete first-hour hardening on a throwaway VPS, from memory, timed. Target: under 30 minutes.
2. After 24 hours online, read your auth.log: count attempts, list top attacking IPs, list guessed usernames.
3. Configure fail2ban with a 24 h ban time (bantime in jail.local), get your OWN test IP banned, then unban it
(fail2ban-client unban).
4. Run the compromise checklist on a healthy machine so you know what 'normal' looks like — that's the whole
point of baselines.









24. Capstone — Deploy a Real Production Server
This project chains every chapter into one artifact: a hardened VPS serving a FastAPI application over
HTTPS with automated backups, monitoring, and one-command deploys. Complete it and you are,
operationally, a junior Linux administrator. Use the GoOdo backend or any small API.

The checklist
Phase

Tasks

Chapters

1. Provision

Create VPS (Hetzner CX22), point
DNS A-record at it

1, 10

2. Harden

deploy user, keys-only SSH, ufw,
fail2ban, auto-updates, swap

6, 9, 14

3. Runtime

apt basics, git clone to /opt/app,
venv, requirements

8

4. Service

systemd unit (non-root,
EnvironmentFile, Restart,
MemoryMax)

7

5. Expose

nginx reverse proxy → certbot
HTTPS → deny dotfiles

10, 14

6. Automate

backup script + systemd timer,
logrotate config, health-check alert

11, 13

7. Deploy

release-directory deploy script with
symlink switch + health gate

11

8. Verify

the acceptance tests below

all

Acceptance tests — prove it works
curl -s https://yourdomain/health # 1
ssh root@server # 2
sudo systemctl kill -s KILL app && sleep 6 && curl -fs https://yourdomain/health # 3
sudo reboot # then wait and: # 4
curl -fs https://yourdomain/health
systemctl list-timers | grep backup # 5
sudo ss -tulpn | grep -v 127.0.0.1 # 6

1. Returns 200 over valid HTTPS.
2. Must be REFUSED (root login disabled).
3. Kill -9 the app; within seconds systemd revives it and health returns 200 — self-healing verified.
4. Full reboot; everything returns with zero manual commands — persistence verified.
5. Backup timer scheduled and its last run succeeded.
6. Only ports 22, 80, 443 exposed publicly — minimal attack surface verified. Pass all six and the machine is
production-grade.





PRO INSIGHT: Then do the real expert exercise: destroy the VPS entirely and rebuild it from your notes in under
one hour. The second build is where scattered knowledge crystallizes into skill — and your notes become a
runbook you'll reuse for every future server, including eQuorum on-premise installs.





25. The 90-Day Plan & Beyond
Weekly schedule (≈1 hour/day)
Weeks

Chapters

Deliverable that proves it

1

1–2: foundations, terminal fluency

One week terminal-only for file management; vimtutor lesson 1–3

2

3: filesystem

Draw the / tree from memory; symlink and /proc exercises done

3

4: core commands

find one-liners solved; diff/watch in daily use

4–5

5: text processing

The 404-investigation pipeline built incrementally on a real log

6

6: permissions

Shared setgid directory working; sudoers fine-grained rule written

7

7: processes &amp; systemd

Own unit file surviving kill -9 and reboot; a systemd timer running

8

8–9: packages &amp; storage

Third-party repo added the signed way; disk added end-to-end in a
VM; swap live

9

10: networking

SSH config aliases; a working tunnel; the 5-step diagnosis narrated

10

11–12: scripting

getopts script + deploy script with traps and health gate; shellcheck
clean

11

13–14: monitoring &amp; security

Baseline triage saved; VPS hardened from memory under 30 min

12

15–17: boot, tmux, vim

Emergency-mode fstab repair done; tmux cockpit daily; vimtutor 1–4

13

18–19: WSL, Docker

WSL exported &amp; systemd on; compose stack with surviving
volume

14

20–22: Postgres, net, debugging

Restore drill passed; Docker/ufw trap reproduced; lsof +L1 drill done

15–16

23–24: scenarios, capstone

Six incidents solved unaided; all acceptance tests passing;
rebuild-from-notes done

After the book — the expert track
Containers: your Docker knowledge + this book = you now understand what Docker abstracts.
Configuration management: Ansible turns your runbook into executable YAML — the natural next step
after rebuilding a server by hand. Observability: Prometheus + Grafana. Certification: LPIC-1 or CompTIA
Linux+ (this book ≈ 85–90% coverage), then RHCSA for the hands-on credential employers respect most.
Above all: run real things. Your GoOdo backend, eQuorum demos, backups of your business data —
production responsibility is the greatest teacher.

You now have the map. The territory is a terminal away.
— End of the Complete Edition —

Appendix A — The One-Page Command Reference





Need

Command

Where am I / what's here

pwd · ls -lah · tree -L 2

Find files

find DIR -name 'PAT' · locate NAME

Find text

grep -rn 'PAT' DIR

Disk space

df -h · du -sh * · ncdu · lsof +L1

Memory / CPU

free -h · top · htop · vmstat 1

Service control

systemctl status|start|enable --now UNIT

Service logs

journalctl -u UNIT -f · --since '1h ago'

Ports listening

sudo ss -tulpn

Who owns a port

sudo lsof -i :PORT

Process control

ps aux · pgrep -af PAT · kill PID · pkill -f PAT

Permissions

chmod 755 F · chown user:grp F · namei -l PATH

Users

adduser U · usermod -aG GRP U · groups U

Packages

apt update · apt install P · dpkg -S FILE · dpkg -L P

Network basics

ip -br a · ping H · dig NAME · curl -v URL

Copy to server

rsync -avz SRC host:DST · scp F host:

Archive

tar -czf out.tar.gz DIR · tar -xzf F -C DIR

Follow a log

tail -f FILE · journalctl -f

Repeat with eyes

watch -n2 CMD

What is this cmd

type -a CMD · man CMD · tldr CMD

Trace a process

strace -p PID · lsof -p PID · cat /proc/PID/status

Firewall

sudo ufw status verbose · allow PORT/tcp

Certificates

certbot renew --dry-run

Docker

docker ps · logs -f C · exec -it C bash · compose up -d

PostgreSQL

sudo -u postgres psql · pg_dump -Fc DB > f.dump





Appendix B — Interview & Self-Test Questions
Answer each aloud in 2–3 sentences. If any feels shaky, its chapter number is your reading list. These mirror
real sysadmin/DevOps interview questions.

Fundamentals
1. What is the difference between the kernel, the shell, and a distribution? (Ch. 1) 2. Explain what happens,
layer by layer, from power-on to login prompt. (Ch. 15) 3. Why does 'everything is a file' make Linux
composable? (Ch. 3) 4. What is the difference between a hard link and a symlink, and when does each
break? (Ch. 3)

Permissions and processes
5. Decode 2775 on a directory and explain why teams use it. (Ch. 6) 6. Why can a file be deleted by
someone who cannot read it? (Ch. 6) 7. SIGTERM vs SIGKILL — and why prefer TERM? (Ch. 7) 8. Your
service died at 3 AM; list your first four commands. (Ch. 7, 13) 9. What does Restart=on-failure do that a cron
'@reboot' cannot? (Ch. 7)

Text, scripting, debugging
10. Build aloud: top 10 IPs by request count from an nginx log. (Ch. 5) 11. What do set -e, -u, and pipefail
each protect against? (Ch. 11) 12. Why is `for f in $(find ...)` broken and what replaces it? (Ch. 11) 13. df
shows the disk full but du cannot find the space — explain and fix. (Ch. 22) 14. How would strace answer
'which config file does this app really read'? (Ch. 22)

Networking, storage, security
15. Walk the four-layer network diagnosis order and the tool for each. (Ch. 10) 16. Why UUIDs in fstab, and
what does nofail prevent? (Ch. 9) 17. Explain the Docker-bypasses-ufw trap and its fix. (Ch. 21) 18. Describe
key-only SSH hardening AND the verification step that prevents lockout. (Ch. 14) 19. What is an SSH local
forward, with a database example? (Ch. 10) 20. Your pg_dump runs nightly — why is that alone not yet a
backup strategy? (Ch. 20)





Appendix C — Glossary
Term

Meaning

cgroup

Kernel mechanism limiting a process group's CPU/RAM/IO — powers containers and systemd
resource caps

CIDR (/24)

Subnet notation: /24 = first 24 bits are the network = 256 addresses

daemon

A background service process (sshd, nginx — the trailing d)

file descriptor

A process's numeric handle to an open file/socket; 0=stdin, 1=stdout, 2=stderr

HBA

PostgreSQL's host-based authentication rules (pg_hba.conf)

inode

The on-disk record of a file's metadata; filenames are just links to inodes

initramfs

Mini root filesystem the kernel uses at boot to load storage drivers

LVM

Logical Volume Manager — flexible layer between partitions and filesystems

namespace

Kernel isolation of a process's view (PIDs, network, mounts) — powers containers

OOM killer

Kernel's last resort under memory exhaustion: kills the 'worst' process

PID 1

The first process; systemd; ancestor of everything

reverse proxy

Front server (nginx) forwarding requests to backend apps

shebang

#!/usr/bin/env bash — the interpreter line of a script

socket

An endpoint for network (or local) communication, identified by IP:port

swap

Disk space used as overflow RAM

syscall

A request from a process to the kernel (open, read, connect) — what strace shows

target (systemd)

A named group of units; boot destinations like multi-user.target

TTL (DNS)

Seconds a resolver may cache a DNS answer

tuple/tup (pg)

A row version inside PostgreSQL; dead tuples = bloat

UUID

Stable unique ID for filesystems — the right identifier in fstab

unit (systemd)

Anything systemd manages: .service, .timer, .mount, .target

zombie

A finished process whose parent hasn't read its exit status — harmless in ones, a bug in hundreds

— End of the Ultimate Edition —