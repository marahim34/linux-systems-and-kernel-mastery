3. PATH — How the Shell Finds Commands
The question every beginner eventually asks
When you type git, how does the shell know to run /usr/bin/git and not some other file? The answer is the
PATH variable: an ordered, colon-separated list of directories the shell searches, left to right, stopping at the
first match. Understanding PATH explains 'command not found', why your own scripts do not run, and how
virtual environments 'take over' a command.
echo $PATH
echo $PATH | tr ':' '\n'