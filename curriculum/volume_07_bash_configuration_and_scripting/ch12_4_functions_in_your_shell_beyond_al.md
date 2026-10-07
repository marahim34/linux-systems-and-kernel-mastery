4. Functions in Your Shell — Beyond Aliases
When an alias is not enough
A function is a named block of shell code that can take arguments and run multiple commands. Put
functions in .bashrc just like aliases. Use one whenever you need an argument in the middle, logic, or several
steps.
mkcd() {
mkdir -p "$1" && cd "$1"
}
extract() {
case "$1" in
*.tar.gz|*.tgz) tar -xzf "$1" ;;
*.tar.bz2) tar -xjf "$1" ;;
*.zip) unzip "$1" ;;
*.gz) gunzip "$1" ;;
*) echo "Cannot extract '$1'" ;;
esac
}
backup() {
cp "$1" "$1.$(date +%F).bak"
}

1. mkcd: make a directory AND enter it. $1 is the first argument. The && means 'cd only if mkdir succeeded'.
2. extract: one command for every archive type...
3. ...case matches the filename pattern...
4. ...and runs the right tar/unzip flags. Never memorise archive flags again.
5. backup: copy a file to a dated .bak — $(date +%F) inserts today's date. backup config.yaml makes
config.yaml.2026-07-03.bak.

PRO INSIGHT: Alias versus function decision: an alias is a nickname; a function is a small program. If you can write
it as 'replace this word with that phrase', use an alias. If you need to reference an argument like $1 in the middle,
run logic, or use multiple commands, use a function. Functions are strictly more powerful — when in doubt, write a
function.
PRACTICE EXERCISES