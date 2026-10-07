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