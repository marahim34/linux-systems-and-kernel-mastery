14. User Commands — Shell Functions
A function is a named block of shell code. Define these in ~/.bashrc so they are available in every session.

14.1 List only directories
_lsd shows just the directories here.
_lsd() {
ls -p | grep '/$'
}

1. ls -p appends a slash to directory names. grep '/$' keeps only lines ENDING in a slash, which are exactly the
directories. Wrapping it in _lsd() { ... } makes it a reusable command.

14.2 List only files
_lsf shows just the regular files here.
_lsf() {
ls -p | grep -v '/$'
}