3. Remove parsed options so $1 becomes the first positional argument. Now your script runs as: deploy.sh -e prod -v
target1 target2

Traps — cleaning up no matter what
tmpdir=$(mktemp -d)
trap 'rm -rf "$tmpdir"' EXIT
trap 'echo "Interrupted"; exit 130' INT