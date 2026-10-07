#!/usr/bin/env bash
# ==============================================================================
# Production Log Analyzer & Anomaly Detector
# Demonstrates: regex matching, awk aggregations, status distribution, brute force detection
# ==============================================================================
set -euo pipefail

LOG_FILE="${1:-practice_data/access.log}"
if [ ! -f "$LOG_FILE" ]; then
    echo "Usage: $0 <path_to_access_log>"
    exit 1
fi

echo "=================================================================="
echo "          HTTP LOG INTELLIGENCE REPORT: $LOG_FILE"
echo "=================================================================="

TOTAL_REQS=$(wc -l < "$LOG_FILE")
UNIQUE_IPS=$(awk '{print $1}' "$LOG_FILE" | sort -u | wc -l)
echo "  Total Requests Analyzed: $TOTAL_REQS"
echo "  Unique IP Addresses    : $UNIQUE_IPS"

echo -e "\n[1] HTTP STATUS CODE BREAKDOWN"
awk '{status[$9]++} END {
    for (s in status) {
        printf "  Status %-4s : %4d requests (%5.1f%%)\n", s, status[s], (status[s]/NR)*100
    }
}' "$LOG_FILE" | sort -k2,2rn

echo -e "\n[2] TOP TALKERS (HIGHEST VOLUME CLIENTS)"
awk '{ips[$1]++} END {
    for (ip in ips) {
        printf "  %-18s : %3d requests\n", ip, ips[ip]
    }
}' "$LOG_FILE" | sort -k3,3rn | head -n 5

echo -e "\n[3] SUSPICIOUS TRAFFIC / 4xx/5xx ERRORS"
awk '$9 ~ /^(4|5)/ {
    printf "  %-16s %-6s %-30s (Status: %s)\n", $1, $6, $7, $9
}' "$LOG_FILE"

echo -e "\n[4] DATA VOLUME BY RESPONSE STATUS"
awk '{bytes[$9] += $10} END {
    for (s in bytes) {
        printf "  Status %-4s : %8d bytes (%.2f KB)\n", s, bytes[s], bytes[s]/1024
    }
}' "$LOG_FILE" | sort -k2,2rn

echo -e "\nLog analysis complete."
