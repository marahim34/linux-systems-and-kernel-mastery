11. Bash Scripting — From Zero to Automation
Engineer
Your first real script, line by line
#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'
readonly LOG_FILE="/var/log/myscript.log"
main() {
log "Starting"
check_requirements
do_work "$@"
log "Done"
}
log() { printf '%s %s\n' "$(date '+%F %T')" "$*" | tee -a "$LOG_FILE"; }
main "$@"