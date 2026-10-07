5. The Prompt — Customising PS1
What PS1 is
PS1 is the variable holding your prompt's format. Change it in .bashrc to show exactly the information you
want — directory, user, host, git branch, time. A good prompt gives context at a glance.
Code

Shows

Code

Shows

\u

username

\w

full current directory

\h

hostname (short)

\W

current directory
basename only

\H

hostname (full)

\$

$ for user, # for root

\t

time (24h HH:MM:SS)

\n

newline

\A

time (HH:MM)

\!

history number

\d

date

\j

number of background jobs

PS1='[\u@\h \w]\$ '
PS1='\[\e[32m\]\u@\h\[\e[0m\]:\[\e[34m\]\w\[\e[0m\]\$ '