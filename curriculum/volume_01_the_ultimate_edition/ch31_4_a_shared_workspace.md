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