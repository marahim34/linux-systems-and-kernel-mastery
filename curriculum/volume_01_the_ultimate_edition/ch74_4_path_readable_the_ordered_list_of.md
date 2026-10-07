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