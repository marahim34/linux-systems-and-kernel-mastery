#!/usr/bin/env bash
# ==============================================================================
# Linux User & Privilege Security Auditor
# Demonstrates: UID 0 checks, SUID audit, /etc/passwd parsing, sudoers audit
# ==============================================================================
set -euo pipefail

echo "=================================================================="
echo "          LINUX USER & PRIVILEGE SECURITY AUDIT"
echo "=================================================================="

# 1. Check for accounts with UID 0 (root privileges)
echo -e "\n[1] ACCOUNTS WITH UID 0 (SUPERUSER EQUIVALENTS)"
awk -F: '$3 == 0 { printf "  - User: %-15s UID: %s Shell: %s\n", $1, $3, $7 }' /etc/passwd

# 2. Check for users with valid login shells
echo -e "\n[2] INTERACTIVE USER ACCOUNTS (REGULAR USERS >= 1000)"
awk -F: '$3 >= 1000 && $7 !~ /(nologin|false)/ { printf "  - User: %-15s UID: %-6s Home: %-20s Shell: %s\n", $1, $3, $6, $7 }' /etc/passwd

# 3. Check for accounts with empty passwords (if readable)
echo -e "\n[3] PASSWORD INTEGRITY CHECK"
if [ -r /etc/shadow ]; then
    EMPTY_PW=$(awk -F: '($2 == "" || $2 == "!") {print $1}' /etc/shadow)
    if [ -z "$EMPTY_PW" ]; then
        echo "  No active empty password accounts detected."
    else
        echo "  Accounts with locked or blank passwords: $EMPTY_PW"
    fi
else
    echo "  /etc/shadow requires elevated privilege to read (as expected for security)."
fi

# 4. SUID/SGID Binaries in common directories
echo -e "\n[4] SUID/SGID BINARY SCAN (/usr/bin, /bin, /usr/sbin)"
find /usr/bin /bin /usr/sbin -maxdepth 2 -type f \( -perm -4000 -o -perm -2000 \) 2>/dev/null | head -n 10 | while read -r binary; do
    PERMS=$(ls -l "$binary" | awk '{print $1, $3, $4}')
    printf "  - %-30s [%s]\n" "$binary" "$PERMS"
done
echo "  (Displaying top 10 SUID/SGID binaries)"

# 5. Sudoers groups
echo -e "\n[5] PRIVILEGED GROUPS (sudo / wheel)"
for grp in sudo wheel adm; do
    if grep -q "^${grp}:" /etc/group 2>/dev/null; then
        MEMBERS=$(grep "^${grp}:" /etc/group | cut -d: -f4)
        echo "  Group '$grp' members: ${MEMBERS:-none}"
    fi
done

echo -e "\nAudit finished."
