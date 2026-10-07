1. PATH is the colon-separated list of directories searched for commands; putting $HOME/bin first lets your own scripts
take priority. HOME is your home directory, used by ~ expansion and by cd with no argument. export makes a variable
visible to child processes. Add these lines to ~/.bashrc (interactive shells) or ~/.profile (login shells) to make them
permanent.

13.2 A custom prompt
Set PS1 to show host, history number, time and directory.
PS1="[\h \! \A] \w\$ "