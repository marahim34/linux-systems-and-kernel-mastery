13. Debugging Bash & Best Practices
The debugging tools
bash -x script.sh
bash -n script.sh
set -x # inside a script: start tracing here
set +x # stop tracing
shellcheck script.sh

1. -x TRACES execution: prints every command with variables expanded, as it runs. The single most useful bash
debugging tool.
2. -n checks SYNTAX without running — catch errors before execution.