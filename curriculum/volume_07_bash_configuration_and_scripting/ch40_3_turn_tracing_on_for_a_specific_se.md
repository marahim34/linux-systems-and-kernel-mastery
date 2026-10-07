3. Turn tracing on for a specific SECTION of a script...
4. ...and off again, to debug just the tricky part.
5. shellcheck is a LINTER that catches bugs, bad quoting, and dangerous patterns automatically. Install with apt install
shellcheck.

PRO INSIGHT: shellcheck is the closest thing bash has to a compiler checking your work. It flags unquoted
variables, useless constructs, common mistakes, and genuine bugs before they bite. Run it on every script you
write. Combined with bash -x for tracing runtime behaviour, these two tools turn bash debugging from guesswork
into a systematic process. No professional writes bash without shellcheck.

The best-practices checklist
Practice

Why

#!/usr/bin/env bash + set -euo pipefail

Portable interpreter, fail fast and loud

Quote every variable: "$var"

Prevents word-splitting bugs and disasters

Use local in functions

Stops variables leaking and clashing

Validate input with ${1:?...} or guards

Fail clearly instead of doing damage

Use $( ) not backticks

Readable and nestable

Use [[ ]] for tests, (( )) for math

The safe, modern constructs

trap for cleanup

Temp files and state cleaned up on any exit

Run shellcheck

Catches bugs automatically before they run

Prefer functions over long linear scripts

Readable, testable, reusable

PRACTICE EXERCISES