11. Functions, Arguments & Exit Codes
Arguments — how scripts receive input
Variable

Means

$0

the script's name

$1, $2, ...

the first, second, ... argument

$#

the NUMBER of arguments

$@

ALL arguments, as separate quoted words

$*

all arguments as one string

$?

exit code of the last command

$$

the script's process ID

#!/usr/bin/env bash
set -euo pipefail
if [[ $# -lt 1 ]]; then
echo "Usage: $0 <name>" >&2
exit 1
fi
echo "Hello, $1"
echo "You gave $# argument(s)"