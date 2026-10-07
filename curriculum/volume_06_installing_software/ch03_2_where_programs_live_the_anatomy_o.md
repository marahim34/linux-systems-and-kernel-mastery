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