1. Once defined in .bashrc and reloaded, they behave like built-in commands in every new shell.

14b. _lsize_desc (largest first)
_lsize_desc() {
ls -la | sort -k5,5nr
}