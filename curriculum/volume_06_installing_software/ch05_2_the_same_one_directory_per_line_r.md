2. The same, one directory per line, readable. The shell checks these top to bottom when you type any command.
OUTPUT

/home/abdur/bin
/usr/local/sbin
/usr/local/bin
/usr/sbin
/usr/bin
/bin

The three commands that answer 'which program runs?'
which python3
type python3
command -v python3
type -a python3

1. which shows the path of the command that WOULD run — the first match in PATH.
2. type is the shell built-in version; it also tells you if something is an alias, function, or built-in, not just a file.
3. command -v is the portable, script-safe way to ask the same question.
4. type -a shows ALL matches in PATH, not just the first — reveals when the same command exists in several places
(the cause of 'wrong version' confusion).

PRO INSIGHT: This is exactly how Python virtual environments and version managers work. When you 'activate' a
venv, it simply puts its own bin directory at the FRONT of PATH. Now typing python3 finds the venv's copy first,
before /usr/bin/python3. Deactivate, and PATH returns to normal. No magic — just PATH ordering. Once you see
this, a whole class of 'why is it using the wrong version' problems becomes obvious: run type -a and read the order.

Adding your own directory to PATH





mkdir -p ~/bin
echo 'export PATH="$HOME/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
which myscript.sh