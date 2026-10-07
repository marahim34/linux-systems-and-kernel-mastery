1. Same idea inverted: grep -v drops the lines ending in a slash, leaving non-directories. -v means 'invert the match'.

14.3 My processes
_ps shows processes owned by the current user.
_ps() {
ps -u "$USER" -f
}

1. ps -u "$USER" filters to processes owned by whoever is logged in; -f gives the full-format listing. $USER is a shell
variable holding your username, so the function works for anyone.

14.4 List by size
_lsize lists files sorted by size ascending.
_lsize() {
ls -la | sort -n -k 5
}

1. ls -la produces the detailed listing whose fifth column is the size. sort -n -k 5 sorts numerically on that column,
smallest first. Combining a listing with sort is a general pattern for ranking by any column.

PRO INSIGHT: Define all four in ~/.bashrc, then run source ~/.bashrc. From then on _lsd, _lsf, _ps and _lsize
behave like built-in commands in every terminal you open.
PRACTICE EXERCISES