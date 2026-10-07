5. The WSL essential from Volume 1: commit LF, never CRLF.

Hooks — git runs your scripts
# .git/hooks/pre-commit (chmod +x)
#!/usr/bin/env bash
set -e
shellcheck scripts/*.sh
grep -rn "SECRET\|PASSWORD" --include="*.py" src/ && {
echo "Possible secret in code — commit blocked"; exit 1; }
exit 0