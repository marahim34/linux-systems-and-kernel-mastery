3. The ERR trap fires on any error, reporting WHICH line failed ($LINENO) — invaluable for debugging.

A complete, realistic script
#!/usr/bin/env bash
set -euo pipefail
readonly SRC="${1:?Usage: backup.sh <dir>}"
readonly DEST="$HOME/backups"
readonly STAMP=$(date +%Y%m%d-%H%M%S)
log() { echo "[$(date +%T)] $*"; }
mkdir -p "$DEST"
log "Backing up $SRC"
tar -czf "$DEST/backup-$STAMP.tar.gz" "$SRC"
log "Removing backups older than 7 days"
find "$DEST" -name "backup-*.tar.gz" -mtime +7 -delete
log "Done. Current backups:"
ls -lh "$DEST"