# Volume 6: Installing Software & Finding Things

LINUX MASTERY
VOLUME 6 — INSTALLING
SOFTWARE & FINDING THINGS
Package Managers, Every Way to Install a Program, Where Software Lives, and
How
to Locate Any File, Binary, Library or Config on the System — the Complete
Practical Guide

The book that answers 'how do I install this' and 'where did it go' · Prepared for MD
Abdur Rahim · 2026





Table of Contents — Volume 6
1. How Software Gets Onto Linux — the Big Picture
2. Where Programs Live — the Anatomy of an Installed Program
3. PATH — How the Shell Finds Commands
4. APT — the Debian/Ubuntu Package Manager, Complete
5. Finding & Choosing Packages
6. Where Did It Go? — Locating an Installed Program's Files
7. The Other Package Systems — Snap, Flatpak, AppImage
8. Language Package Managers — pip, npm & friends
9. Installing From Source — the Classic ./configure make
10. Installing Downloaded Files — .deb, .tar.gz, binaries
11. Finding Any File on the System — the Complete Toolkit
12. Keeping Software Healthy — updates, cleanup, troubleshooting





1. How Software Gets Onto Linux — the Big Picture
The Linux way is different from Windows
On Windows you download an .exe from a website and double-click it. On Linux, the normal way is the
opposite: you ask a package manager to fetch and install software from a trusted repository — a central,
curated collection of thousands of programs. You rarely download from random websites. This is safer,
faster, and keeps everything updatable from one place.

The five ways to install software — and when to use each
This is the map for the whole volume. Nearly every installation you ever do falls into one of these five
categories. Knowing which to reach for is half the skill.
Method

What it is

When to use it

Chapter

System package manager

apt fetches from official
repos

DEFAULT choice —
always try this first

4

Universal packages

Snap, Flatpak, AppImage

Newer apps not in the
repos, or GUI apps

7

Language managers

pip, npm, cargo, etc.

Developer libraries and
tools for a language

8

From source

compile the code yourself

Latest version, or software
not packaged anywhere

9

Downloaded files

.deb, tarball, single binary

Vendor gives you a file
directly (Docker, Chrome)

10

PRO INSIGHT: The golden rule of installing on Linux: ALWAYS try the system package manager (apt) first. It
handles dependencies, security updates, and clean removal automatically. Only move down the list — to snaps,
language managers, source, or downloaded files — when apt does not have what you need or has too old a
version. Reaching for a website download first is a Windows habit worth unlearning.

Why repositories are safer
A repository's packages are cryptographically signed by the distribution. When apt installs one, it verifies the
signature, guaranteeing the software really came from the trusted source and was not tampered with.
Downloading a random .deb or piping a website script into your shell (curl ... | bash) skips this protection —
sometimes necessary, but always a step down in safety. Understanding this trade-off is part of thinking like a
Linux administrator.





2. Where Programs Live — the Anatomy of an
Installed Program
A program is not one file
A common beginner surprise: installing 'a program' actually scatters several kinds of file across the system,
each in a standard place. Understanding this layout (which follows the Filesystem Hierarchy Standard from
Volume 4) means you always know where to look. A typical program installs into these locations:
Part

Typical location

What it is

The executable

/usr/bin/ or /usr/sbin/

The command you actually run (e.g.
/usr/bin/git)

Libraries

/usr/lib/

Shared code the program depends
on

Configuration

/etc/

System-wide settings (e.g. /etc/ssh/)

Your settings

~/.config/ or ~/.name

Per-user config in your home
directory

Documentation

/usr/share/doc/

Manuals and readmes

Manual pages

/usr/share/man/

What man command shows

Data files

/usr/share/name/

Icons, templates, other shared data

Variable data

/var/lib/name/

Databases and state the program
creates

The three tiers of where things install
WHERE a program lands tells you HOW it was installed. This is a useful diagnostic:
Location

Means it came from

Managed by

/usr/bin, /usr/lib

The system package manager (apt)

apt — do not edit by hand

/usr/local/bin, /usr/local/lib

You compiled or installed it manually

You — apt never touches /usr/local

/opt/name

A self-contained third-party app

The vendor's installer

PRO INSIGHT: The /usr vs /usr/local split is a deliberate, important convention. The package manager owns /usr.
Everything YOU install by hand goes in /usr/local, which apt promises never to touch. This keeps your manual
installations from clashing with system packages, and means you can wipe /usr/local to undo all your manual work
without breaking the system. When you compile from source (Chapter 9), it installs to /usr/local by default for
exactly this reason.

Seeing it yourself





which git
ls -l /usr/bin/git
ls /etc | head
ls ~/.config | head

1. Show WHERE the git command's executable lives — usually /usr/bin/git.
2. Confirm it is a real file (or a symlink to one) in the system binary directory.
3. Browse system configuration — each subdirectory usually belongs to one installed program.
4. Browse your PERSONAL config — where programs store your individual settings, separate from the system.





3. PATH — How the Shell Finds Commands
The question every beginner eventually asks
When you type git, how does the shell know to run /usr/bin/git and not some other file? The answer is the
PATH variable: an ordered, colon-separated list of directories the shell searches, left to right, stopping at the
first match. Understanding PATH explains 'command not found', why your own scripts do not run, and how
virtual environments 'take over' a command.
echo $PATH
echo $PATH | tr ':' '\n'

1. Print the raw PATH — a colon-separated list of directories.
2. The same, one directory per line, readable. The shell checks these top to bottom when you type any command.
OUTPUT

/home/abdur/bin
/usr/local/sbin
/usr/local/bin
/usr/sbin
/usr/bin
/bin

The three commands that answer 'which program runs?'
which python3
type python3
command -v python3
type -a python3

1. which shows the path of the command that WOULD run — the first match in PATH.
2. type is the shell built-in version; it also tells you if something is an alias, function, or built-in, not just a file.
3. command -v is the portable, script-safe way to ask the same question.
4. type -a shows ALL matches in PATH, not just the first — reveals when the same command exists in several places
(the cause of 'wrong version' confusion).

PRO INSIGHT: This is exactly how Python virtual environments and version managers work. When you 'activate' a
venv, it simply puts its own bin directory at the FRONT of PATH. Now typing python3 finds the venv's copy first,
before /usr/bin/python3. Deactivate, and PATH returns to normal. No magic — just PATH ordering. Once you see
this, a whole class of 'why is it using the wrong version' problems becomes obvious: run type -a and read the order.

Adding your own directory to PATH





mkdir -p ~/bin
echo 'export PATH="$HOME/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
which myscript.sh

1. Make a personal bin directory.
2. Prepend it to PATH in your shell config — $HOME/bin is now searched FIRST.
3. Reload the config so it takes effect now.
4. Any executable script you drop in ~/bin is now runnable by name from anywhere, just like a system command.

PRACTICE EXERCISES
1. Print your PATH one line per directory and explain the search order.
2. Run type -a python3 and type -a ls; note which is a file and which might be a builtin or alias.
3. Create a script in ~/bin, add ~/bin to PATH, and run it by name from a different directory.
4. Find a command that exists in two PATH locations (try type -a) and explain which one wins and why.





4. APT — the Debian/Ubuntu Package Manager,
Complete
The mental model
APT works with an INDEX (a local catalogue of what is available in the repositories) and the PACKAGES
themselves. You refresh the index, then install from it. This two-part design is why apt update (refresh the
catalogue) is separate from apt upgrade (install newer versions). Confusing these two is the most common
apt mistake.

The daily commands
sudo apt update
sudo apt upgrade
sudo apt install git
sudo apt install git curl htop
sudo apt remove git
sudo apt purge git
sudo apt autoremove

1. Refresh the catalogue of available packages. Downloads NO software — only the list. Run this before installing.
2. Install newer versions of everything already installed. This is how you keep the system patched.
3. Install a package, automatically pulling in everything it depends on.
4. Install several at once — just list them.
5. Uninstall, but KEEP its configuration files in /etc (in case you reinstall).
6. Uninstall AND delete its config files — a fully clean removal.
7. Remove dependencies that were installed for other packages but are no longer needed — keeps the system lean.

PRO INSIGHT: The command that fixes most 'package not found' errors: sudo apt update. If apt says it cannot find
a package you KNOW exists, your local catalogue is stale. Refresh it first. The rule of thumb: always run apt update
before apt install on a machine you have not touched in a while, or right after adding a new repository.

Understanding what apt is about to do
apt list --installed | wc -l
apt list --upgradable
apt-cache policy git
apt-mark hold postgresql-16
apt-mark unhold postgresql-16

1. How many packages are installed on this machine.
2. Preview exactly which packages have updates waiting BEFORE you upgrade.
3. Show the installed version, the available version, and which repository it comes from — the full status of one
package.
4. FREEZE a package at its current version so apt upgrade will not touch it — protect a database from a surprise major
upgrade.
5. Unfreeze it again when you are ready.





The dpkg layer underneath
apt is a friendly front-end over dpkg, the low-level tool that actually installs .deb files and tracks what is
installed. You use dpkg directly mainly to ASK questions about installed packages, which Chapter 6 covers in
full. For now, know that apt handles downloading and dependencies, while dpkg handles the actual
unpacking and record-keeping.
PRACTICE EXERCISES
1. Run apt update then apt list --upgradable and read what would change.
2. Install htop, then check apt-cache policy htop to see its version and source repository.
3. Install then purge a small package (like sl or cowsay), confirming with which that it is gone.
4. Hold a package, attempt an upgrade, watch it be kept back, then unhold it.





5. Finding & Choosing Packages
You know what you want to DO, not the package name
The real-world problem: you want 'a tool to edit photos' or 'the thing that provides the dig command', but you
do not know the package's name. These commands bridge the gap between intent and package name — a
skill used constantly.
apt search "image editor"
apt show gimp
apt-cache search pdf | head
apt-file update && apt-file search bin/dig

1. Search package names AND descriptions for keywords — how you discover what is available.
2. Show full details of one package: description, version, size, dependencies, homepage. Read this BEFORE installing
something unfamiliar.
3. Another search form; pipe to head because results can be long.
4. The powerful one: apt-file finds which PACKAGE PROVIDES a given file or command. Here it answers 'which
package gives me the dig command?' (answer: dnsutils). Install apt-file first with apt install apt-file.

PRO INSIGHT: The 'command not found, which package has it?' solution: apt-file search. When a tutorial tells you
to run a command you do not have, apt-file search bin/thatcommand names the package to install. Ubuntu even
does this automatically — try running an uninstalled command and it often suggests 'apt install X'. This closes the
most frustrating beginner gap: knowing the command name but not the package.

Judging a package before installing
apt show nginx
apt-cache depends nginx
apt-cache rdepends nginx | head

1. The full description and metadata — is this the right tool, is it maintained, how big is it?
2. What this package DEPENDS on — what will be pulled in with it.
3. What depends ON this package (reverse dependencies) — helps you understand how central a package is, and what
might break if you removed it.

PRACTICE EXERCISES
1. Find a package that provides a spellchecker using apt search.
2. Install apt-file, then discover which package provides the command 'ifconfig' and which provides 'traceroute'.
3. Run apt show on three packages and compare their sizes and dependency counts.
4. Use apt-cache depends to see everything nginx would pull in.





6. Where Did It Go? — Locating an Installed
Program's Files
The two questions you will always ask
After installing something, two questions recur: 'WHERE did all its files go?' and 'WHICH package does this
file belong to?'. dpkg answers both. These are among the most useful commands in daily Linux life, and
almost no beginner knows them.

Question 1: what files did this package install?
dpkg -L nginx
dpkg -L nginx | grep bin
dpkg -L nginx | grep etc

1. List EVERY file the nginx package installed, with full paths. The complete map of where it went.
2. Filter to just its executables — where are the commands?
3. Filter to just its config files — where are the settings I need to edit? This instantly answers 'where is nginx's config?'
(/etc/nginx/).

Question 2: which package owns this file?
dpkg -S /usr/bin/git
dpkg -S /etc/ssh/sshd_config
which nginx | xargs dpkg -S

1. The reverse lookup: given a file, which package installed it? Answers 'what do I remove to get rid of this?'
2. Works for any file — here, sshd_config belongs to openssh-server.
3. Chain them: find a command's path with which, then ask dpkg which package owns it. A two-step identification of any
command on the system.

PRO INSIGHT: These two commands, dpkg -L (package to files) and dpkg -S (file to package), are the answer to
'where is this program's config?' and 'what installed this mystery file?'. Master them and the filesystem stops being a
mystery. Example workflow: you install a service, it does not work, you need its config — dpkg -L servicename |
grep etc shows you exactly where to look. No guessing, no googling.

Verifying and inspecting an installed package
dpkg -l | grep nginx
dpkg -s nginx
dpkg -L nginx | xargs -I{} sh -c 'test -f "{}" && echo "{}"' | head

1. Is it installed, and which version? The 'ii' at the line start means installed-installed (good).
2. Full status and metadata of an installed package — description, version, dependencies, size.
3. List its files that actually exist as regular files — useful to see the real installed content.

PRACTICE EXERCISES
1. Install nginx (or any service), then use dpkg -L to find where its config and binary went.
2. Pick three random files in /usr/bin and use dpkg -S to identify which package each belongs to.





3. Find where the ssh CLIENT config lives using dpkg -L openssh-client | grep etc.
4. For a command you use daily, chain: which CMD | xargs dpkg -S to name its package.





7. The Other Package Systems — Snap, Flatpak,
AppImage
Why these exist
APT packages are built for one specific distribution version. Newer 'universal' formats bundle an app WITH
its dependencies so one file runs on any distro, and can update independently of the system. They are
heavier but more portable. You meet them when an app is not in the apt repos, or the apt version is too old.
Format

How it works

Install / run

Trade-off

Snap

Sandboxed, auto-updating,
from Canonical's store

snap install code

Convenient, but larger and
slower to start

Flatpak

Sandboxed, from Flathub,
popular for desktop apps

flatpak install flathub
org.gimp.GIMP

Great for GUI apps; needs
setup

AppImage

One self-contained file you
just run

chmod +x app.AppImage
&amp;&amp;
./app.AppImage

No install at all; you
manage updates yourself

snap find spotify
sudo snap install code --classic
snap list
snap info code
sudo snap remove code

1. Search the Snap store.
2. Install; --classic means it needs full system access (development tools often do).
3. List installed snaps and their versions.
4. Detailed info about a snap.
5. Remove a snap cleanly.

PRO INSIGHT: When to use which: try apt FIRST (lightest, best integrated). If the app is missing or too old, use a
snap or flatpak — especially for desktop GUI apps and fast-moving tools like editors and browsers. Use an
AppImage when a vendor offers only that, or you want a portable app with no installation. On a server, prefer apt
and avoid snaps where you can; on a desktop, the universal formats are genuinely useful.

# AppImage: no installation, just make it runnable
chmod +x SomeApp.AppImage
./SomeApp.AppImage

1. Make the downloaded file executable (Volume 1 permissions).
2. Run it directly — it contains everything it needs. Nothing was installed system-wide; delete the file to 'uninstall'.

PRACTICE EXERCISES
1. List any snaps already on your system with snap list.
2. Search the snap store for an app you use and read its snap info.
3. Download any AppImage, make it executable, and run it — note that nothing was installed system-wide.
4. Compare: find the same app in apt and as a snap; compare their sizes and versions.









8. Language Package Managers — pip, npm &
friends
A different layer of software
Developer libraries — a Python HTTP library, a Node.js framework — are not installed with apt. Each
programming language has its OWN package manager pulling from its OWN repository (PyPI for Python,
npm registry for Node). These install language-specific code, usually for a project or a user, not system-wide.
Language

Manager

Repository

Installs

Python

pip

PyPI

pip install requests

Node.js

npm

npm registry

npm install express

Rust

cargo

crates.io

cargo install ripgrep

Ruby

gem

RubyGems

gem install rails

The critical rule: never pollute the system Python
python3 -m venv ~/venvs/myproject
source ~/venvs/myproject/bin/activate
pip install requests fastapi
pip list
deactivate

1. Create an ISOLATED environment — a private copy of Python and its packages, just for this project.
2. Activate it; your prompt gains a (myproject) prefix and PATH now points here first (Chapter 3).
3. Install libraries INSIDE the sandbox — they cannot clash with the system or other projects.
4. See what is installed in this environment only.
5. Leave the environment; PATH returns to normal.

PRO INSIGHT: The hard rule every Python developer learns, often painfully: NEVER run sudo pip install to put
packages in the system Python. apt and pip will fight over the same files and eventually break each other,
sometimes badly enough to damage system tools written in Python. ALWAYS use a virtual environment (venv) per
project, or pipx for standalone tools. This isolation is exactly the PATH mechanism from Chapter 3 at work — the
venv's bin goes first.

pipx install httpie
pipx list

1. pipx installs a Python TOOL (not a library) in its own hidden environment but makes it available everywhere — the
best of both worlds for command-line tools.
2. List tools pipx manages.

PRACTICE EXERCISES
1. Create a venv, activate it, install a package, and confirm with which python that you are using the venv's Python.
2. Prove isolation: install a package in the venv, deactivate, and show it is not available system-wide.
3. Use pipx to install a command-line tool and run it from any directory.





4. Explain, using PATH, why activating a venv changes which python runs.





9. Installing From Source — the Classic Build
When and why
Sometimes software is not packaged anywhere, or you need the very latest version, or you want custom
build options. Then you compile it from its source code. This is more work and you lose automatic updates,
so it is a last resort — but knowing how demystifies a lot of Linux.

The classic three-step dance
sudo apt install build-essential
tar -xzf program-1.4.tar.gz
cd program-1.4
./configure
make
sudo make install

1. Install the compiler and build tools first (gcc, make) — needed to build anything.
2. Unpack the source archive (Volume 1 archiving).
3. Enter the source directory.
4. configure inspects your system and prepares the build, checking that dependencies exist. Read its output for
missing-library errors.
5. make actually COMPILES the source into an executable — this can take a while.
6. make install COPIES the built program into place, by default under /usr/local (Chapter 2's convention), so it never
clashes with apt's files.

PRO INSIGHT: The reason source installs default to /usr/local: it keeps YOUR compiled software cleanly separated
from the package manager's territory in /usr. But there is a cost — apt does not know this software exists, so it will
never update or track it. You are now the package manager for that program. This is why source-installing is a
deliberate choice, not a default, and why tools like checkinstall or building your own .deb exist for people who do it
often.

Uninstalling a source install
# from the same source directory, IF the project supports it:
sudo make uninstall
# otherwise you must remove files manually — which is why
# many people avoid source installs for casual software

1. Some projects provide make uninstall to reverse make install.
2. Many do not, leaving you to delete files by hand. This lack of clean removal is the biggest downside of source installs,
and the strongest argument for preferring packages.

PRACTICE EXERCISES
1. Install build-essential, then download and compile a small program from source (many tutorials use 'hello' or a
small tool).
2. Read the ./configure output and identify where it says it will install (the prefix).
3. After installing, use which to confirm it landed in /usr/local/bin.
4. Explain why apt will never update a program you installed from source.









10. Installing Downloaded Files — .deb, tarballs,
binaries
When a vendor gives you a file directly
Sometimes a vendor (Google Chrome, Docker, Slack) offers a direct download. These come in a few forms,
each installed differently. This is the closest to the Windows experience, and the least safe, so verify your
source.

A .deb file — the Debian package
wget https://example.com/app.deb
sudo apt install ./app.deb
dpkg -L app

1. Download the .deb file.
2. Install it WITH apt (note the ./) — this way apt resolves its dependencies automatically. Better than the old 'dpkg -i'
which does not handle dependencies.
3. Afterwards it is a normal package: dpkg -L works, apt can remove it. It integrates into the system.

A tarball with a ready binary
tar -xzf tool-linux-amd64.tar.gz
sudo mv tool /usr/local/bin/
sudo chmod +x /usr/local/bin/tool
tool --version

1. Unpack the archive.
2. Move the executable into /usr/local/bin — a directory already in PATH (Chapter 3), so it becomes runnable by name.
/usr/local because you are installing it manually.
3. Ensure it is executable.
4. Confirm it runs. Many Go and Rust tools ship exactly like this: one self-contained binary you drop into PATH.

The curl-pipe-bash pattern — convenient but read first
# vendors often suggest:
curl -fsSL https://get.docker.com | sudo bash
# SAFER: download first, READ it, then run:
curl -fsSL https://get.docker.com -o install.sh
less install.sh
sudo bash install.sh

1. The convenient one-liner runs a script straight from the internet as root — you are trusting it completely and blindly.
2. The responsible version: download the script...
3. ...READ what it will do...
4. ...then run it. For anything with root access, this five-second review is worth it. Never pipe an unread script from an
untrusted source into a root shell.





PRO INSIGHT: Ranking by safety: apt from official repos (safest) > apt install ./file.deb > universal packages >
vendor scripts you have read > curl | bash from an unknown source (riskiest). Each step down trades some safety
for convenience or availability. Knowing where you are on this ladder for each install is the mark of a security-aware
administrator — a mindset that matters for eQuorum's bank clients especially.
PRACTICE EXERCISES
1. Download a .deb (e.g. from a trusted vendor) and install it with apt install ./file.deb, then confirm with dpkg -L.
2. Download a single-binary tool, place it in /usr/local/bin, and run it by name from another directory.
3. Take any 'curl | bash' installer, download the script instead, and read what it actually does before deciding.
4. Explain the safety ranking of the five installation methods in your own words.





11. Finding Any File on the System — the Complete
Toolkit
Five tools, five jobs
'Where is that file?' has several answers depending on what you are looking for. Here is the complete toolkit,
each tool for its purpose. Together they mean nothing on your system is ever truly lost.
Tool

Finds

Speed

Best for

which / type

A command in your PATH

Instant

'Where is the git
executable?'

locate

Any file, by a prebuilt index

Very fast

'Where is that file called
nginx.conf?'

find

Any file, by live search +
any criterion

Slower

Complex searches: by
size, time, permission

dpkg -S / -L

Files belonging to
packages

Fast

'What installed this / where
did it go?'

grep -r

TEXT inside files

Slower

'Which file contains this
setting?'

The tools in action
which docker
locate nginx.conf
sudo updatedb
find /etc -name "*.conf" -mtime -7
grep -rn "server_name" /etc/nginx/
dpkg -S $(which docker)

1. Instantly locate a command's executable.
2. Find a file by name from a prebuilt database — extremely fast (install with apt install plocate).
3. Refresh locate's database if a recently-created file is not found yet.
4. Live search with criteria locate cannot express: .conf files in /etc changed in the last week.
5. Search the CONTENT of files: which nginx config file mentions server_name, with line numbers.
6. Identify which package a command came from, in one line.

PRO INSIGHT: The decision tree for 'find my file': Is it a COMMAND? Use which/type. Do you know its NAME? Use
locate (fast) or find (flexible). Do you know it belongs to a PACKAGE? Use dpkg -L. Are you searching for TEXT
inside files? Use grep -r. Matching the tool to the question is the whole skill — and it turns 'I can't find anything on
Linux' into 'I can find anything on Linux'.

The modern fast alternatives





fd conf /etc
rg "server_name" /etc/nginx/

1. fd is a faster, friendlier find (Volume 2) — fd conf /etc finds config files quickly.
2. rg (ripgrep) is a much faster grep -r — the modern tool for searching text in files. Both are optional upgrades over the
classics, which exist everywhere.

PRACTICE EXERCISES
1. Find the full path of five commands you use with which.
2. Use locate to find every file named *.conf; if it misses recent files, run sudo updatedb first.
3. Use find to locate all files in your home larger than 10 MB modified this month.
4. Use grep -r to find which file in /etc contains your hostname.
5. For a mystery file in /usr/bin, identify its package with dpkg -S.





12. Keeping Software Healthy
The regular maintenance routine
sudo apt update && sudo apt upgrade
sudo apt autoremove --purge
sudo apt clean
snap refresh
df -h /

1. The weekly essential: refresh the catalogue and install security and bug-fix updates. This one habit keeps a system
safe.
2. Remove orphaned dependencies AND their config — reclaim space and reduce clutter.
3. Clear the downloaded-package cache in /var/cache/apt (safe; they re-download if needed).
4. Update snaps (they also auto-update in the background).
5. Check disk space afterwards — package caches and old kernels are common space eaters.

Troubleshooting the common failures
Problem

Cause

Fix

'Unable to locate package'

Stale catalogue

sudo apt update first

'held broken packages'

Dependency conflict

sudo apt install -f (fix broken)

Interrupted install

apt/dpkg stopped mid-way

sudo dpkg --configure -a

'Could not get lock'

Another apt is running

Wait, or find it: ps aux | grep apt

Command exists but not found

Not in PATH

Find it (Ch. 11), add its dir to PATH
(Ch. 3)

Wrong version runs

Another copy earlier in PATH

type -a CMD to see all; fix PATH
order

sudo dpkg --configure -a
sudo apt install -f
sudo apt update --fix-missing

1. Finish any package configuration left half-done by an interrupted install — the first repair to try.
2. Fix broken dependencies — the second repair.
3. Rebuild the catalogue when downloads failed. These three commands resurrect most broken package systems.

PRO INSIGHT: Prevention beats repair: run apt update && apt upgrade weekly, and do big upgrades inside tmux
(Volume 1) so a dropped SSH connection cannot leave dpkg half-finished and the system unbootable. A
well-maintained package system almost never breaks; a neglected one breaks at the worst moment. This is doubly
true for the servers running your businesses.

How this volume fits the whole set
You now have the complete practical picture of software on Linux: the five ways to install it, where every part
of a program lives, how the shell finds commands through PATH, and how to locate any file, binary, config or