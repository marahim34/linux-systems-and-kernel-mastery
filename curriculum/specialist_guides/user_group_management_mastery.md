# User Group Management Mastery

LINUX
USER & GROUP
MANAGEMENT
A Mastery Guide — From First Account to Enterprise Identity

Covers: passwd/shadow internals · useradd/usermod/userdel · groupadd/gpasswd
chage & password policy · permissions & SUID/SGID · sudo & sudoers
PAM basics · LDAP/SSSD overview · bulk scripting · troubleshooting

Table of Contents
01

Foundations — Users, Groups, and the Kernel's View of Identity

02

The Core Files — passwd, shadow, group, gshadow

03

Creating and Managing Users

04

Creating and Managing Groups

05

Password Policy and Account Aging

06

Ownership, Permissions, and Special Bits

07

sudo and Privilege Escalation

08

PAM, Login Control, and Account Locking

09

Centralized Identity — LDAP, SSSD, and NIS in Brief

10

Bulk Operations and Scripting

11

Troubleshooting and Real-World Scenarios

12

Quick Reference Cheat Sheet

13

Practice Exercises

Linux User & Group Management — Mastery Guide

1

CHAPTER 01

Foundations — Users, Groups, and
the Kernel's View of Identity
Before touching a single command, understand what the kernel actually checks when it decides
whether you're allowed to do something. Everything else in this book builds on this chapter.

1.1 What a 'user' really is to Linux
Linux does not know your name. It knows numbers. Every process on the system runs with a User ID
(UID) and one or more Group IDs (GID). The kernel compares these numbers against the permissions on
a file or resource to decide access. The username abdur is just a human-friendly label mapped to a UID
in a text file. The kernel never reads that label.

1.2 UID ranges — how Linux organizes identity
UID Range

Meaning

Example

0

root — full system access, bypasses permission checks

root

1–99

Static system accounts, allocated by distro packages

daemon, bin, sys

100–999

Dynamic system/service accounts, created by installed
software

sshd, systemd-network

1000+

Regular human (login) users

abdur, deploy

These ranges are convention, defined by /etc/login.defs (UID_MIN / UID_MAX), not hard kernel law.
Debian/Ubuntu and RHEL/Fedora both default regular users to starting at 1000.

1.3 Why root is UID 0 — and why that matters
The kernel has one special case in its permission logic: if the process's effective UID is 0, most permission
checks are skipped entirely. This is not a policy or a config file, it's built into the kernel's access control
path. Anything with UID 0 is root, no matter what its username is. This is why a common attack technique
is to create a second UID-0 account with an innocuous name; a security audit that only looks for a user
literally called 'root' will miss it.
CAUTION — UID 0 is UID 0

Linux User & Group Management — Mastery Guide

2

If you ever see two lines in /etc/passwd with UID 0, treat it as a serious incident. There should be
exactly one: root.

1.4 Primary group vs. supplementary groups
Every user has exactly one primary group (recorded in /etc/passwd) and can belong to zero or more
supplementary groups (recorded in /etc/group). When you create a file, its group ownership defaults to
your primary group. Supplementary groups exist to grant you extra access without changing what new
files you create — e.g. adding yourself to the docker or sudo group doesn't change your primary group.
TIP — Private Group Scheme
Debian/Ubuntu, by default, create a new group with the same name as each new user (user private
group scheme) rather than putting everyone in a shared users group. This makes umask-based
collaboration safer — each user's own files are private by default, and shared directories use SGID to
control group collaboration (see Chapter 6).

1.5 Checking your own identity
$ id
uid=1000(abdur) gid=1000(abdur) groups=1000(abdur),27(sudo),999(docker)
$ whoami
abdur
$ groups
abdur sudo docker
$ id -u # print only the UID
1000
$ id -g # print only the primary GID
1000
$ id -Gn # print all group names
abdur sudo docker

id is the authoritative command. whoami and groups are shortcuts built on the same underlying lookup.

Linux User & Group Management — Mastery Guide

3

CHAPTER 02

The Core Files — passwd, shadow,
group, gshadow
Every user and group management command is, underneath, just a careful, lock-protected edit to
four plain-text files. Understanding them means you can diagnose and fix almost anything without
memorizing extra commands.

2.1 /etc/passwd — the user database
Despite the name, this file has not stored actual passwords for decades. It's world-readable and holds
account metadata. Each line has seven colon-separated fields:
abdur:x:1000:1000:MD Abdur:/home/abdur:/bin/bash

#

Field

Meaning

1

abdur

Login name

2

x

Password placeholder — real hash lives in /etc/shadow

3

1000

UID

4

1000

Primary GID

5

MD Abdur

GECOS — full name / comment field

6

/home/abdur

Home directory

7

/bin/bash

Login shell

An x in field 2 tells the login process to look up the real hash in /etc/shadow instead. If field 2 were a
literal hash, every user on the system could read it, since /etc/passwd is world-readable by design
(commands like ls -l need to resolve UIDs to names for everyone).

2.2 /etc/shadow — the real password store
Readable only by root (mode 000 or 640 depending on distro). Nine colon-separated fields:
abdur:$6$randomsalt$hashvalue...:19850:0:90:7:14::

#

Field

Meaning

1

abdur

Login name

Linux User & Group Management — Mastery Guide

4

#

Field

Meaning

2

$6$...

Password hash. $6$ = SHA-512, $y$ = yescrypt (modern default)

3

19850

Days since Jan 1 1970 password was last changed

4

0

Minimum days before password can be changed again

5

90

Maximum days password is valid before it must change

6

7

Warning period (days) before expiry

7

14

Grace period after expiry before account is disabled

8

(empty)

Account expiration date (absolute, days since epoch)

9

(reserved)

Unused

CAUTION — Never hand-edit /etc/shadow directly
Always use vipw -s or chage/passwd. A stray character or missing colon can corrupt the field count
and lock every account out at once.

2.3 /etc/group — the group database
sudo:x:27:abdur,deploy

#

Field

Meaning

1

sudo

Group name

2

x

Password placeholder (rarely used — see gshadow)

3

27

GID

4

abdur,deploy

Comma-separated list of supplementary members

Note what's not here: a user whose primary group is sudo won't appear in this member list — primary
group membership lives only in /etc/passwd, field 4.

2.4 /etc/gshadow — group passwords and administrators
sudo:!::abdur,deploy

Rarely used in practice (group passwords are a legacy feature few systems rely on), but it does define
group administrators — users who can add/remove members with gpasswd without root, field 3 in this
file.

2.5 Reading these files safely

Linux User & Group Management — Mastery Guide

5

$ getent passwd abdur # correct way — works with LDAP/SSSD too
abdur:x:1000:1000:MD Abdur:/home/abdur:/bin/bash
$ getent group sudo
sudo:x:27:abdur,deploy
$ sudo cat /etc/shadow | grep abdur # requires root

TIP — Use getent, not cat, in scripts
getent queries through Name Service Switch (NSS), so it returns correct results whether accounts
come from local files, LDAP, or SSSD. Reading /etc/passwd directly only shows local accounts and
will silently miss centrally-managed ones.

Linux User & Group Management — Mastery Guide

6

CHAPTER 03

Creating and Managing Users
The command-line tools that write to the files from Chapter 2 so you never have to edit them by
hand. This is where most day-to-day admin work happens.

3.1 useradd — the low-level tool
useradd is the standard, distro-agnostic tool. On its own it's minimal — no home directory skeleton, no
password. Always pair it with explicit flags.
$ sudo useradd -m -d /home/rina -s /bin/bash -c "Rina Akter" rina
$ sudo passwd rina # set the password interactively
New password:
Retype new password:
passwd: password updated successfully

Flag

Meaning

-m

Create the home directory, copying /etc/skel into it

-d PATH

Specify home directory path explicitly

-s SHELL

Login shell, e.g. /bin/bash, /usr/sbin/nologin

-c "text"

GECOS comment field (usually full name)

-g GROUP

Primary group (name or GID)

-G g1,g2

Supplementary groups, comma-separated

-u UID

Force a specific UID

-e YYYY-MM-DD

Account expiration date

-r

Create a system account (UID below UID_MIN, no expiry)

3.2 adduser — the friendly Debian/Ubuntu wrapper
adduser is a Perl script wrapping useradd with sane interactive defaults — it creates the home directory,
sets up a private group, prompts for the password, and asks for GECOS fields. Not available by default on
RHEL/Fedora/CentOS.
$ sudo adduser rina
Adding user `rina' ...
Adding new group `rina' (1001) ...

Linux User & Group Management — Mastery Guide

7

Adding new user `rina' (1001) with group `rina' ...
Creating home directory `/home/rina' ...
Copying files from `/etc/skel' ...
New password:
Retype new password:
Full Name []: Rina Akter
Room Number []:
Work Phone []:
Home Phone []:
Other []:
Is the information correct? [Y/n] y

TIP — Which one should you script with?
Use useradd in scripts and automation — it's non-interactive and identical across distros. Use
adduser for a human sitting at the terminal on Debian/Ubuntu.

3.3 /etc/skel — the template for new home directories
Whatever exists in /etc/skel is copied into every new user's home directory when created with -m.
Common contents: .bashrc, .profile, .bash_logout, and often empty Desktop/Documents folders. Add a
company-wide .bashrc snippet or README here and every future user gets it automatically.
$ sudo cp /path/to/company-motd.txt /etc/skel/README.txt
$ sudo useradd -m newhire # newhire's home now includes README.txt

3.4 usermod — modifying existing accounts
$ sudo usermod -aG docker rina # ADD rina to docker group (supplementary)
$ sudo usermod -s /usr/sbin/nologin svc_backup # disable interactive login
$ sudo usermod -l newname oldname # rename login (does NOT rename home dir)
$ sudo usermod -d /srv/rina -m rina # move home directory, updating passwd
$ sudo usermod -L rina # lock the account (prepend ! to hash)
$ sudo usermod -U rina # unlock the account
$ sudo usermod -e 2026-12-31 rina # set account expiration date

CAUTION — -G replaces, -aG appends
usermod -G docker rina without -a REPLACES all of rina's supplementary groups with just
docker — removing sudo, adm, everything else. This is the single most common Linux admin mistake.
Always use -aG when adding, never bare -G.

3.5 userdel — removing accounts
$ sudo userdel rina # removes account, LEAVES home directory behind
$ sudo userdel -r rina # also removes home directory and mail spool

Linux User & Group Management — Mastery Guide

8

$ sudo find / -xdev -nouser -o -nogroup # audit: files still owned by a deleted UID

Deleting a user does not touch files that user owned elsewhere on the filesystem — those files become
orphaned, owned by a UID that no longer resolves to a name. On a production server, always audit for
orphaned files before or after removing an account, especially if the UID might be reused later.

3.6 passwd — setting and managing passwords
$ passwd # change your OWN password
$ sudo passwd rina # root sets/resets rina's password
$ sudo passwd -l rina # lock (same effect as usermod -L)
$ sudo passwd -u rina # unlock
$ sudo passwd -e rina # force password change at next login
$ sudo passwd -S rina # show account status
rina L 07/13/2026 0 90 7 14

The -S output fields are: username, status (P=usable password, L=locked, NP=no password), date last
changed, min age, max age, warn period, inactive period — the same values stored in /etc/shadow.

3.7 su and switching identity
$ su rina # switch to rina, keep current shell environment
$ su - rina # switch to rina with a full login shell (clean environment)
$ su -c "systemctl status nginx" rina # run one command as rina

TIP — Prefer 'su -' over 'su'
Plain su rina keeps your old PATH, environment variables, and working directory, which can cause
confusing bugs (wrong binaries picked up, wrong $HOME). su - rina gives rina a genuinely fresh
login shell, exactly as if they had logged in directly.

Linux User & Group Management — Mastery Guide

9

CHAPTER 04

Creating and Managing Groups
Groups are how Linux does role-based access without giving every application its own password.
Get comfortable with these four commands and shared-directory permissions stop being
mysterious.

4.1 groupadd — creating groups
$ sudo groupadd developers
$ sudo groupadd -g 5000 developers # force a specific GID
$ sudo groupadd -r svc_monitoring # system group (low GID range)

4.2 Adding and removing members
There are two tools for this: usermod (from the user's side) and gpasswd (from the group's side). Both edit
the same /etc/group file.
$ sudo usermod -aG developers rina # add rina to developers (from user side)
$ sudo gpasswd -a rina developers # identical result (from group side)
$ sudo gpasswd -d rina developers # remove rina from developers
$ sudo gpasswd -M rina,masud,shafin developers # set the FULL member list at once

TIP — gpasswd -M is the safe bulk tool
When you need a group's membership to exactly match a list (e.g. syncing from an HR export),
gpasswd -M replaces the whole list atomically — safer than looping usermod calls where a mid-script
failure leaves the group half-updated.

4.3 groupmod — modifying groups
$ sudo groupmod -n devs developers # rename developers -> devs
$ sudo groupmod -g 5050 devs # change the GID

CAUTION — Changing a GID does not update existing files
If files on disk were group-owned by GID 5000 and you renumber the group to 5050, those files still
carry the raw number 5000 in their inode. They will appear owned by 'no group' (or worse, by any
other group that happens to claim 5000 later) until you run find / -group 5000 -exec chgrp
devs {} \; to fix them.

Linux User & Group Management — Mastery Guide

10

4.4 groupdel — removing groups
$ sudo groupdel developers

Fails if the group is still any user's primary group — you must change that user's primary group first
(usermod -g). Files owned by the deleted GID become orphaned, same caveat as user deletion.

4.5 Primary group vs. shared collaboration group
A common real design: each user gets a private primary group matching their username (so their own files
default to being private), and separate shared groups like developers or finance handle team access
to specific directories via SGID (Chapter 6).
$ sudo mkdir /srv/projects/apollo
$ sudo chgrp developers /srv/projects/apollo
$ sudo chmod 2775 /srv/projects/apollo # SGID bit: new files inherit the group
$ ls -ld /srv/projects/apollo
drwxrwsr-x 2 root developers 4096 Jul 13 10:02 /srv/projects/apollo

The 's' in place of the group execute bit is the SGID bit — every file created inside this directory
automatically belongs to the developers group, regardless of the creating user's primary group. Full detail
in Chapter 6.

4.6 Listing and auditing groups
$ getent group developers
developers:x:5000:rina,masud,shafin
$ groups rina # what groups is rina in?
rina : rina developers docker
$ lid -g developers # (libuser) alternative listing, if installed

Linux User & Group Management — Mastery Guide

11

CHAPTER 05

Password Policy and Account Aging
Setting a password is easy. Enforcing when it must be changed, how long an account can sit
dormant, and what happens on expiry is where real account hygiene lives.

5.1 chage — the aging policy tool
$ sudo chage -l rina # list current aging settings
Last password change : Jul 13, 2026
Password expires : Oct 11, 2026
Password inactive : Oct 25, 2026
Account expires : never
Minimum number of days between changes : 0
Maximum number of days between changes : 90
Number of days of warning before expire : 7
$ sudo chage -M 90 -m 7 -W 14 -I 30 rina
$ sudo chage -E 2026-12-31 rina # account itself expires on this date
$ sudo chage -d 0 rina # force password change at NEXT login

Flag

Meaning

-M

Maximum days a password stays valid

-m

Minimum days before it can be changed again (stops rapid cycling)

-W

Warning days shown before expiry

-I

Inactive days after expiry before the account is fully disabled

-E

Absolute account expiration date

-d 0

Expire the password immediately, forcing a change on next login

5.2 System-wide defaults — /etc/login.defs
New accounts inherit their default aging values from this file, read by useradd at creation time. Editing it
only affects users created afterward — it never retroactively changes existing accounts.
PASS_MAX_DAYS 90
PASS_MIN_DAYS 7
PASS_WARN_AGE 14
UID_MIN 1000
UID_MAX 60000

Linux User & Group Management — Mastery Guide

12

5.3 Password quality — PAM's pwquality module
chage controls timing; it says nothing about password strength. That's enforced separately by PAM,
typically via pam_pwquality, configured in /etc/security/pwquality.conf.
# /etc/security/pwquality.conf
minlen = 12
dcredit = -1 # require at least 1 digit
ucredit = -1 # require at least 1 uppercase letter
ocredit = -1 # require at least 1 special character
retry = 3

This is expanded fully in Chapter 8 (PAM).

5.4 Locking vs. expiring vs. deleting — know the difference
Action

Command

Effect

Lock

passwd -l / usermod -L

Prepends ! to hash. Login blocked, account and files intact.
Reversible.

Expire
password

chage -d 0

User can still log in but must set a new password
immediately.

Expire
account

chage -E DATE / usermod
-e

Login blocked entirely after that date, independent of
password.

Delete

userdel [-r]

Account removed from passwd/shadow. Not reversible
without a backup.

TIP — Offboarding pattern
For an employee leaving the company: lock immediately (usermod -L), set an account expiry a short
grace period out, audit their file ownership, then delete once access is fully migrated. Never delete on
day one — you may need that UID for forensic file ownership lookups.

Linux User & Group Management — Mastery Guide

13

CHAPTER 06

Ownership, Permissions, and Special
Bits
Users and groups only matter because the kernel checks them against every file. This chapter
connects identity to actual access control.

6.1 The permission triplet
$ ls -l notes.txt
-rw-r--r-- 1 abdur developers 2048 Jul 13 09:11 notes.txt

Ten characters: file type, then three groups of rwx — owner, group, others. rw-r--r-- reads as: owner
can read/write, group can read, others can read. Numerically this is 644 (r=4, w=2, x=1, summed per
triplet).

6.2 chown and chgrp — changing ownership
$ sudo chown rina notes.txt # change owner only
$ sudo chown rina:developers notes.txt # change owner AND group in one call
$ sudo chown :developers notes.txt # change group only (chown syntax)
$ sudo chgrp developers notes.txt # equivalent, group-only
$ sudo chown -R rina:developers /srv/projects/apollo # recursive

CAUTION — chown -R on a shared tree
Recursive chown can silently break other people's files inside a shared directory tree. Scope it tightly,
and prefer find ... -user OLDUSER -exec chown NEWUSER {} \; when you only want to
reassign one person's files within a shared area.

6.3 chmod — the three special bits
Bit

On a file

On a directory

Octal

SUID

Runs with the file owner's
privileges, not the caller's

No effect

4000

SGID

Runs with the file's group
privileges

New files inherit the directory's group

2000

Sticky

No effect

Only the file's owner (or root) can
delete/rename inside

1000

Linux User & Group Management — Mastery Guide

14

$ sudo chmod u+s /usr/bin/passwd # SUID example — this is WHY passwd works at all;
# it must write to /etc/shadow, which regular users can't
$ ls -l /usr/bin/passwd
-rwsr-xr-x 1 root root 68208 ... /usr/bin/passwd
$ sudo chmod g+s /srv/projects/apollo # SGID on a directory (see Chapter 4.5)
$ sudo chmod +t /tmp # sticky bit — this is why /tmp is safe to share
$ ls -ld /tmp
drwxrwxrwt 12 root root 4096 ... /tmp

CAUTION — SUID on scripts is ignored by the kernel
The kernel refuses to honor SUID/SGID on shell scripts as a security measure (race conditions in the
shebang execution path made it exploitable). It only works on compiled binaries. If you need elevated
execution for a script, use sudo with a tightly scoped rule instead (Chapter 7).

6.4 umask — the default permission mask
umask subtracts permissions from a baseline (666 for files, 777 for directories) at creation time. It's set
per-shell/session, usually in /etc/profile, /etc/bash.bashrc, or a user's own shell rc file.
$ umask
0022
$ touch newfile.txt && ls -l newfile.txt
-rw-r--r-- 1 abdur abdur 0 Jul 13 09:20 newfile.txt # 666 - 022 = 644
$ umask 0002 # common for group-collaborative setups
$ touch teamfile.txt && ls -l teamfile.txt
-rw-rw-r-- 1 abdur developers 0 Jul 13 09:21 teamfile.txt # group gets write too

TIP — umask 002 pairs with SGID directories
A umask of 0022 strips group-write, which defeats the point of an SGID shared directory (Chapter 4.5)
— teammates could read but not edit each other's new files. Set umask 0002 for accounts that
primarily work in shared group directories.

6.5 Access Control Lists (ACLs) — beyond
owner/group/other
Standard permissions only give you one owner and one group per file. When you need "rina: read-write,
masud: read-only, everyone else: nothing" on the same file simultaneously, use POSIX ACLs.
$ sudo setfacl -m u:masud:r-- notes.txt # grant masud read-only, beyond owner/group
$ sudo setfacl -m g:auditors:r-- notes.txt # grant the auditors group read-only
$ getfacl notes.txt
# file: notes.txt
# owner: rina
# group: developers

Linux User & Group Management — Mastery Guide

15

user::rwuser:masud:r-group::r-group:auditors:r-mask::rwother::--$ sudo setfacl -x u:masud notes.txt # remove that specific ACL entry

A file with ACLs shows a trailing + after the permission string in ls -l as a visual reminder to check
getfacl.

Linux User & Group Management — Mastery Guide

16

CHAPTER 07

sudo and Privilege Escalation
Root access without sharing the root password, with a full audit trail. This is how production
systems actually grant admin rights.

7.1 Why sudo instead of logging in as root
—
—

Every command is logged to /var/log/auth.log (or journalctl), tagged with the real user who ran it.

—
—

The root password itself never needs to be shared or even known by anyone.

Access can be scoped — a user can be allowed to run exactly one command as root, not
everything.

Revoking access is instant: remove the user from the sudoers config or the sudo group.

7.2 The quick path — group membership
$ sudo usermod -aG sudo rina # Debian/Ubuntu — the group is called 'sudo'
$ sudo usermod -aG wheel rina # RHEL/Fedora/CentOS — the group is called 'wheel'

This grants full, unrestricted root access (subject to a password prompt) — appropriate for admins, not for
narrowly-scoped service accounts.

7.3 The precise path — /etc/sudoers and visudo
CAUTION — Never edit /etc/sudoers directly
Always use visudo. It locks the file against concurrent edits and, critically, syntax-checks it before
saving. A broken sudoers file can lock out sudo access system-wide, including your own.
$ sudo visudo
# Grant rina full root, password required (default):
rina ALL=(ALL:ALL) ALL
# Grant rina passwordless restart rights on nginx ONLY:
rina ALL=(root) NOPASSWD: /usr/bin/systemctl restart nginx
# Grant an entire group deployment rights, no shell access:
%deploy ALL=(deploy_user) NOPASSWD: /usr/local/bin/deploy.sh

Syntax: who where=(as_whom) what. The %-prefix targets a group instead of a user.

Linux User & Group Management — Mastery Guide

17

7.4 Drop-in files under /etc/sudoers.d/
Rather than growing one shared file, add one file per user or team under /etc/sudoers.d/. Cleaner for
version control and rollback.
$ sudo visudo -f /etc/sudoers.d/rina
rina ALL=(ALL) ALL
$ sudo chmod 440 /etc/sudoers.d/rina # required permissions or sudo will ignore the
file

7.5 Auditing sudo usage
$ sudo grep sudo /var/log/auth.log | tail -20 # Debian/Ubuntu
$ sudo journalctl _COMM=sudo --since today # systemd-based, any distro
$ sudo -l # what am I allowed to run as sudo?
$ sudo -l -U rina # what is rina allowed to run?

Linux User & Group Management — Mastery Guide

18

CHAPTER 08

PAM, Login Control, and Account
Locking
PAM is the layer that decides what 'authentication' even means on Linux — passwords, fingerprint
readers, hardware keys, or lockout after failed attempts all plug in here.

8.1 What PAM actually is
Pluggable Authentication Modules. Instead of every program (login, sshd, sudo, su) implementing its own
password-checking logic, they all call into PAM, which runs a configured stack of modules and returns
pass/fail. Config lives under /etc/pam.d/, one file per service.
$ cat /etc/pam.d/sshd | head -5
auth required pam_unix.so
auth requisite pam_faillock.so preauth
account required pam_nologin.so
password requisite pam_pwquality.so retry=3
session required pam_limits.so

Each line is a module and a control flag (required, requisite, sufficient, optional) that determines how its
pass/fail result affects the overall stack.

8.2 pam_faillock — locking accounts after failed logins
# /etc/security/faillock.conf
deny = 5
unlock_time = 900 # seconds; 0 = admin must unlock manually
$ sudo faillock --user rina # view rina's failed attempt count
$ sudo faillock --user rina --reset # clear the lockout

8.3 pam_nologin and /etc/nologin
If /etc/nologin exists, only root can log in — everyone else sees the file's contents as a message and
is refused. Useful for maintenance windows.
$ sudo sh -c 'echo "System under maintenance until 14:00 UTC" > /etc/nologin'
$ sudo rm /etc/nologin # restore normal logins

8.4 Restricting login without deleting the account
Linux User & Group Management — Mastery Guide

19

Goal

Method

No interactive shell, but service can still
run as this user

Set shell to /usr/sbin/nologin

Deny SSH specifically, but allow console
login

AllowUsers/DenyUsers in /etc/ssh/sshd_config

Deny all logins temporarily, system-wide

Create /etc/nologin

Deny one specific account only

usermod -L or passwd -l

8.5 Login process resource limits —
/etc/security/limits.conf
Tied to identity too — limits can target a user or a group.
# /etc/security/limits.conf
rina soft nofile 4096
rina hard nofile 8192
@developers soft nproc 2048

Linux User & Group Management — Mastery Guide

20

CHAPTER 09

Centralized Identity — LDAP, SSSD,
and NIS in Brief
Everything so far has been local files on one machine. Real organizations manage hundreds of
machines, and nobody edits /etc/passwd by hand on each one.

9.1 The problem local files don't solve
With local-only accounts, onboarding an engineer means creating their user on every server they touch,
and offboarding means remembering to remove it from all of them. Centralized identity systems keep one
authoritative user/group database that every machine consults.

9.2 LDAP — the directory itself
LDAP (Lightweight Directory Access Protocol) is a hierarchical database purpose-built for exactly this:
users, groups, and their attributes, queried over the network. OpenLDAP and Microsoft Active Directory
(which speaks LDAP alongside Kerberos) are the two dominant implementations.
# A simplified LDAP entry for a user, in LDIF format
dn: uid=rina,ou=people,dc=aisora,dc=example
uid: rina
uidNumber: 5001
gidNumber: 5000
homeDirectory: /home/rina
loginShell: /bin/bash
objectClass: posixAccount

9.3 SSSD — the client-side glue
SSSD (System Security Services Daemon) is what actually runs on each Linux machine, caching lookups
against LDAP/AD/Kerberos so identity resolution keeps working even during brief network outages. It
plugs into NSS and PAM, which is why getent passwd someuser (Chapter 2.5) can return an LDAP
account exactly like a local one.
$ sudo systemctl status sssd
$ getent passwd rina@aisora.example # SSSD-backed lookup, works even though
# rina has no line in local /etc/passwd
$ id rina@aisora.example

Linux User & Group Management — Mastery Guide

21

9.4 NIS — the legacy predecessor
Network Information Service (formerly "Yellow Pages") solved the same problem decades earlier by
broadcasting flat passwd/group maps across a network, unencrypted. It predates LDAP and modern
security expectations. You'll still encounter it on older institutional or research infrastructure, but new
deployments should use LDAP/AD with SSSD or Kerberos instead.
CAUTION — NIS transmits credentials in the clear
If you inherit a system still running NIS/YP, treat migrating off it as a security priority, not a
nice-to-have.

9.5 How this changes the commands you already know
Reassuringly: mostly, it doesn't. useradd/usermod/groupadd still work for local accounts. What changes is
that getent, id, and login itself now also check the centralized source through SSSD. The commands
you learned in Chapters 3-4 remain exactly how you manage any purely local or service accounts that
shouldn't live in the central directory.

Linux User & Group Management — Mastery Guide

22

CHAPTER 10

Bulk Operations and Scripting
One user at a time doesn't scale past a handful of accounts. These are the tools for onboarding
twenty engineers at once, or syncing accounts from a CSV export.

10.1 Looping useradd from a list
#!/bin/bash
# create_users.sh — reads one username per line from users.txt
while IFS= read -r username; do
sudo useradd -m -s /bin/bash "$username"
echo "${username}:ChangeMe123!" | sudo chpasswd
sudo chage -d 0 "$username" # force password change on first login
echo "Created: $username"
done < users.txt

10.2 chpasswd — bulk password setting
$ cat passwords.txt
rina:Str0ngP@ss1
masud:Str0ngP@ss2
$ sudo chpasswd < passwords.txt
# Using pre-hashed values (safer — no plaintext ever touches disk):
$ echo 'rina:$6$salt$hashvalue...' | sudo chpasswd -e

CAUTION — Never leave plaintext password files lying around
If you must use a plaintext passwords.txt for chpasswd, shred it immediately after: shred -u
passwords.txt. Better still, generate random passwords and deliver them through a secrets
manager, not a flat file.

10.3 newusers — full batch account creation
newusers takes passwd-format lines (including a plaintext password in the hash field) and creates every
account, home directory, and password in one pass.
$ cat newusers.txt
rina:Str0ngP@ss1:1001:1001:Rina Akter:/home/rina:/bin/bash
masud:Str0ngP@ss2:1002:1002:Masud Rana:/home/masud:/bin/bash
$ sudo newusers newusers.txt

Linux User & Group Management — Mastery Guide

23

10.4 Scripted group sync from a CSV
#!/bin/bash
# sync_group.sh <groupname> <csv_of_usernames>
group="$1"
members="$2"
sudo gpasswd -M "$members" "$group"
echo "Group $group now contains: $members"

10.5 Auditing everything at once
# List every human user (UID >= 1000) with their shell and groups
$ awk -F: '$3 >= 1000 && $3 < 60000 {print $1, $7}' /etc/passwd
# Find accounts with no password set at all (NP status — dangerous)
$ sudo awk -F: '($2 == "") {print $1}' /etc/shadow
# Find accounts whose password field is locked (starts with !)
$ sudo awk -F: '($2 ~ /^!/) {print $1}' /etc/shadow
# Find every user who is a member of sudo/wheel
$ getent group sudo wheel

Linux User & Group Management — Mastery Guide

24

CHAPTER 11

Troubleshooting and Real-World
Scenarios
The scenarios that actually show up in tickets, and the exact diagnostic path for each.

"Permission denied" but the user is clearly in the right group
Group membership changes don't apply to already-open sessions. The user must log out and back in (or
run `newgrp groupname`) for a new supplementary group to take effect in their shell.
$ newgrp developers # activates the new group in the CURRENT shell without full
re-login

New files in a shared folder keep landing with the wrong group
Check for the SGID bit: `ls -ld /path` should show 's' in the group execute position. If it's missing, `sudo
chmod g+s /path` — see Chapter 6.3.
Also check the creating user's umask; 0022 strips group-write even with SGID set.

User can't log in, no error beyond 'Access denied'
$ sudo passwd -S username # check L (locked) vs P (usable)
$ sudo chage -l username # check whether account or password has expired
$ getent passwd username # confirm the account resolves at all (local vs LDAP
mismatch)
$ sudo grep username /var/log/auth.log # see the actual PAM rejection reason

Deleted a user, now 'ls -l' shows a raw number instead of a name
That's an orphaned file — its UID no longer maps to any account. Find them all with `sudo find / -xdev
-nouser` and either chown them to a real account or archive/remove as appropriate before that UID gets
reused by a new account.

sudo says "username is not in the sudoers file. This incident will be
reported."
Expected behavior, not a bug. Check `sudo -l -U username` as an existing admin to see current rights,
then add access properly via visudo or the sudo/wheel group (Chapter 7).

Linux User & Group Management — Mastery Guide

25

If NO account has sudo (fully locked out), boot into single-user/rescue mode or use a live USB to mount
the disk and fix /etc/sudoers offline.

useradd works but the account can't be found by other tools
Usually an NSS/SSSD caching issue in centralized environments. Try `sudo sss_cache -E` to expire the
SSSD cache, or `getent passwd username` to confirm which source (files vs sss) is actually being
consulted, per /etc/nsswitch.conf.

Linux User & Group Management — Mastery Guide

26

CHAPTER 12

Quick Reference Cheat Sheet
Every command from this book, one place, for when you already know the concept and just need
the syntax.

Users
Task

Command

Create user + home dir

sudo useradd -m -s /bin/bash username

Set password

sudo passwd username

Add to a group (correct)

sudo usermod -aG groupname username

Lock / unlock account

sudo usermod -L username / -U username

Rename login

sudo usermod -l newname oldname

Delete user + home dir

sudo userdel -r username

Show account status

sudo passwd -S username

Show aging policy

sudo chage -l username

Force password change at next
login

sudo chage -d 0 username

Groups
Task

Command

Create group

sudo groupadd groupname

Add member

sudo gpasswd -a username groupname

Remove member

sudo gpasswd -d username groupname

Replace full member list

sudo gpasswd -M user1,user2 groupname

Rename group

sudo groupmod -n newname oldname

Delete group

sudo groupdel groupname

List a user's groups

groups username

List a group's members

getent group groupname

Linux User & Group Management — Mastery Guide

27

Permissions
Task

Command

Change owner + group

sudo chown user:group path

Recursive ownership change

sudo chown -R user:group path

Set SGID on a shared dir

sudo chmod g+s path

Set sticky bit

sudo chmod +t path

Grant one extra user access via
ACL

sudo setfacl -m u:username:rw- path

View ACLs

getfacl path

sudo / identity
Task

Command

Edit sudoers safely

sudo visudo

Add a drop-in sudo rule

sudo visudo -f /etc/sudoers.d/username

Check what I can run as sudo

sudo -l

Check own identity

id

Query any identity source
(local/LDAP)

getent passwd username

Linux User & Group Management — Mastery Guide

28

CHAPTER 13

Practice Exercises
Work through these on a disposable VM or container, not production. Answers are intentionally not
included — check your own work with getent, id, and ls -l.

01

Create a user `nabil` with home directory /home/nabil, bash shell, and full name "Nabil
Hasan" in the GECOS field. Confirm every field with `getent passwd nabil`.

02

Set nabil's password to expire every 60 days, with a 10-day warning, and force a change on
first login.

03

Create a group `finance` with GID 6000. Add nabil and one other user to it as a
supplementary group without disturbing their existing groups.

04

Create a shared directory /srv/finance owned by root:finance, mode 2770, and verify that a
file created inside it by any finance member is automatically group-owned by finance.

05

Grant nabil passwordless sudo rights to restart the nginx service only, using a dedicated file
under /etc/sudoers.d/. Verify with `sudo -l -U nabil`.

06

Lock nabil's account, confirm the lock with `passwd -S`, then unlock it and confirm again.

07

Write a one-line find command that lists every file on the system owned by a UID that has no
matching entry in /etc/passwd.

08

Set up an ACL on a single file so that a user who is NOT in its owning group still gets
read-only access, without changing the file's owner or group.

09

Write a small bash script that reads a list of usernames from a text file, creates each as a
locked account (no login yet), and prints a summary table of who was created.

10

Explain, in your own words, the exact chain of files and commands the kernel and login
process consult between you typing your password and getting a shell — from Chapter 2
through Chapter 8.

Linux User & Group Management — Mastery Guide

29

