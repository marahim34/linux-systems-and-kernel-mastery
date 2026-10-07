#!/usr/bin/env bash
# ==============================================================================
# System Health & Performance Monitor
# Demonstrates: procfs interrogation, awk formatting, threshold alerts, strict mode
# ==============================================================================
set -euo pipefail

ALERT_CPU_THRESHOLD=85
ALERT_MEM_THRESHOLD=90
ALERT_DISK_THRESHOLD=85

echo "=================================================================="
echo "          LINUX SYSTEM HEALTH MONITOR - $(date '+%Y-%m-%d %H:%M:%S')"
echo "=================================================================="

# 1. OS & Kernel Information
OS_NAME=$(grep -oP '(?<=PRETTY_NAME=")[^"]*' /etc/os-release 2>/dev/null || uname -s)
KERNEL=$(uname -r)
UPTIME=$(uptime -p 2>/dev/null || uptime | awk '{print $3,$4}')
echo -e "\n[1] HOST & KERNEL"
echo "  Operating System : $OS_NAME"
echo "  Kernel Version   : $KERNEL"
echo "  Uptime           : $UPTIME"

# 2. CPU Load & Utilization
echo -e "\n[2] CPU METRICS"
LOAD=$(uptime | awk -F'load average:' '{ print $2 }' | xargs)
CPU_CORES=$(grep -c ^processor /proc/cpuinfo)
echo "  CPU Cores        : $CPU_CORES"
echo "  Load Average     : $LOAD (1m, 5m, 15m)"

# 3. Memory & Swap (via /proc/meminfo)
echo -e "\n[3] MEMORY ALLOCATION"
MEM_TOTAL=$(awk '/MemTotal/ {print int($2/1024)}' /proc/meminfo)
MEM_AVAIL=$(awk '/MemAvailable/ {print int($2/1024)}' /proc/meminfo)
MEM_USED=$((MEM_TOTAL - MEM_AVAIL))
MEM_PERCENT=$((MEM_USED * 100 / MEM_TOTAL))

SWAP_TOTAL=$(awk '/SwapTotal/ {print int($2/1024)}' /proc/meminfo)
SWAP_FREE=$(awk '/SwapFree/ {print int($2/1024)}' /proc/meminfo)
SWAP_USED=$((SWAP_TOTAL - SWAP_FREE))

printf "  RAM Total        : %d MB\n" "$MEM_TOTAL"
printf "  RAM Used         : %d MB (%d%%)\n" "$MEM_USED" "$MEM_PERCENT"
printf "  Swap Total/Used  : %d MB / %d MB\n" "$SWAP_TOTAL" "$SWAP_USED"

if [ "$MEM_PERCENT" -ge "$ALERT_MEM_THRESHOLD" ]; then
    echo "  [ALERT] Memory usage is critically high: ${MEM_PERCENT}%!"
fi

# 4. Disk Usage
echo -e "\n[4] STORAGE FILESYSTEMS"
df -h --output=source,fstype,size,used,avail,pcent,target -x tmpfs -x devtmpfs | while read -r line; do
    echo "  $line"
done

# 5. Top 5 CPU Processes
echo -e "\n[5] TOP 5 PROCESSES BY CPU"
ps -eo pid,user,%cpu,%mem,comm --sort=-%cpu | head -n 6 | awk 'NR==1 {printf "  %-8s %-10s %-6s %-6s %-15s\n", $1,$2,$3,$4,$5; next} {printf "  %-8s %-10s %-6s %-6s %-15s\n", $1,$2,$3,$4,$5}'

# 6. Failed Systemd Services
echo -e "\n[6] SYSTEMD SERVICES STATUS"
if command -v systemctl >/dev/null 2>&1; then
    FAILED=$(systemctl --failed --no-legend 2>/dev/null || true)
    if [ -z "$FAILED" ]; then
        echo "  All systemd units healthy (0 failed)."
    else
        echo "  [WARNING] Failed units detected:"
        echo "$FAILED" | awk '{print "    - " $1 " (" $2 ")"}'
    fi
else
    echo "  systemctl not available on this environment."
fi

echo -e "\n=================================================================="
echo "Report generated successfully."
