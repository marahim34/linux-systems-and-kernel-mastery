#!/usr/bin/env bash
# ==============================================================================
# Automated Backup Rotator with Retention Policy
# Demonstrates: tar archiving, SHA256 checksums, retention pruning, exit codes
# ==============================================================================
set -euo pipefail

SOURCE_DIR="${1:-practice_data}"
BACKUP_DIR="${2:-/tmp/dojo_backups}"
KEEP_COUNT="${3:-5}"

mkdir -p "$BACKUP_DIR"
TIMESTAMP=$(date '+%Y%m%d_%H%M%S')
ARCHIVE_NAME="backup_${TIMESTAMP}.tar.gz"
TARGET_PATH="${BACKUP_DIR}/${ARCHIVE_NAME}"

echo "Creating compressed backup of '$SOURCE_DIR' -> '$TARGET_PATH'..."
tar -czf "$TARGET_PATH" -C "$(dirname "$SOURCE_DIR")" "$(basename "$SOURCE_DIR")"

# Generate checksum
sha256sum "$TARGET_PATH" > "${TARGET_PATH}.sha256"
SIZE=$(du -h "$TARGET_PATH" | cut -f1)
echo "Backup created successfully! Size: $SIZE"
echo "Checksum: $(cat "${TARGET_PATH}.sha256")"

# Retention policy: Prune old backups
echo -e "\nEnforcing retention policy (keeping newest $KEEP_COUNT backups)..."
CURRENT_COUNT=$(find "$BACKUP_DIR" -maxdepth 1 -name "backup_*.tar.gz" | wc -l)
if [ "$CURRENT_COUNT" -gt "$KEEP_COUNT" ]; then
    find "$BACKUP_DIR" -maxdepth 1 -name "backup_*.tar.gz" -printf '%T+ %p\n' | \
        sort | head -n "$((CURRENT_COUNT - KEEP_COUNT))" | awk '{print $2}' | while read -r old_file; do
            echo "Removing pruned backup: $old_file"
            rm -f "$old_file" "${old_file}.sha256"
        done
else
    echo "Current backups ($CURRENT_COUNT) within limit ($KEEP_COUNT). No pruning needed."
fi
