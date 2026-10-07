4. Enable ** to match files recursively (ls **/*.py finds all Python files at any depth).

A history setup that transforms your workflow





HISTSIZE=50000
HISTFILESIZE=100000
HISTCONTROL=ignoreboth
shopt -s histappend
HISTTIMEFORMAT="%F %T "
bind '"\e[A": history-search-backward'
bind '"\e[B": history-search-forward'