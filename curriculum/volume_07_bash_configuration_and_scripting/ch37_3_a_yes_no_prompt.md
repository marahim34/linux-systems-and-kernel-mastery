3. A yes/no prompt...
4. ...proceed only if the answer is y, otherwise exit cleanly.

Error handling with traps
#!/usr/bin/env bash
set -euo pipefail
tmpdir=$(mktemp -d)
trap 'rm -rf "$tmpdir"' EXIT
trap 'echo "Failed at line $LINENO" >&2' ERR
# work using $tmpdir...
echo "Working in $tmpdir"