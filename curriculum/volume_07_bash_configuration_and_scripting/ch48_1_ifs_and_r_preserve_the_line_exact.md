1. IFS= and -r preserve the line exactly; feeding the file with < avoids a subshell so n survives. This is the correct,
whitespace-safe way to process a file line by line.

Ch.11 — Script requiring two arguments





#!/usr/bin/env bash
set -euo pipefail
if [[ $# -lt 2 ]]; then
echo "Usage: $0 <src> <dest>" >&2
exit 1
fi
echo "Copying $1 to $2"

1. $# is the argument count; if fewer than 2, print usage to stderr and exit 1. Validating input up front is the mark of a
robust script.

Ch.11 — Function returning success if file exists
exists() { [[ -e "$1" ]]; }
if exists /etc/hostname; then echo "present"; fi