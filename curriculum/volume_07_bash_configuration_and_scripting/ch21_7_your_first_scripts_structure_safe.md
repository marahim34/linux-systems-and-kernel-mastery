7. Your First Scripts — Structure & Safety
The anatomy of a script
#!/usr/bin/env bash
set -euo pipefail
echo "Hello, this is my first script"
echo "Today is $(date +%F)"
echo "You are $USER in $PWD"