1. Aliases do simple text replacement and do not handle $1 — it is taken literally, not as your argument. Only a function
can use an argument in the middle. This is the concrete reason functions exist alongside aliases.

Ch.4 — 'up N' function to climb directories
up() {
local n="${1:-1}"
local path=""
for ((i=0; i<n; i++)); do path="../$path"; done
cd "$path" || return 1
}