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