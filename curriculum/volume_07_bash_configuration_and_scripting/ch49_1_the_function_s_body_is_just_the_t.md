1. The function's body is just the test; its exit code becomes the function's return value. So exists works directly in an if,
reading naturally. No explicit return needed — the last command's status is returned automatically.

Ch.12 — Confirmation before proceeding
read -p "Delete all logs? [y/N] " ans
[[ "${ans,,}" == "y" ]] || { echo "Cancelled"; exit 0; }
echo "Deleting..."

1. ${ans,,} lowercases the reply so Y and y both work. If it is not y, print Cancelled and exit cleanly. A safe confirmation
pattern for destructive actions.

Ch.13 — Trace a section only
echo "normal part"
set -x
result=$(( 6 * 7 ))
echo "$result"
set +x
echo "normal again"

1. set -x begins printing each command with expansions; set +x stops it. This isolates tracing to the tricky calculation
without flooding the whole run with debug output.

You can now configure the shell to fit your hands and program it to do your work.
That is the whole of bash.
— End of Volume 7, Bash: Configuration & Scripting —