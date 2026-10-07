1. What Bash Is — Shell, Session & Startup
Shell, terminal, bash — three different things
People blur these, but they are distinct. A terminal is the window (or the console) that shows text. A shell is
the PROGRAM running inside it that reads your commands and runs them. Bash is the most common shell
(the 'Bourne Again SHell'). So: you type into a terminal, which runs a shell, which is usually bash.
echo $SHELL
bash --version
cat /etc/shells
ps -p $$