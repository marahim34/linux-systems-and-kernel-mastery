5. Print one specific environment variable.

The important ones
Variable

Controls

PATH

Where the shell looks for commands (Volume 6 Ch. 3)

HOME

Your home directory; where ~ points

EDITOR / VISUAL

Default editor for git, crontab, etc.

LANG / LC_*

Language and locale (dates, sorting, characters)

PS1

Your prompt (Chapter 5)

USER

Your username

PWD / OLDPWD

Current and previous directory

TERM

Your terminal type (affects colours)

Setting them permanently and safely





# in ~/.bashrc for interactive use:
export EDITOR="vim"
export PATH="$HOME/bin:$PATH"
# for a secret, load from a file, never hardcode:
export API_KEY="$(cat ~/.secrets/api_key)"
chmod 600 ~/.secrets/api_key