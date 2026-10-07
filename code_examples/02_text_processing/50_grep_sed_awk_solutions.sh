#!/usr/bin/env bash
# ==============================================================================
# GREP, SED & AWK 50 GRADED PRACTICE EXERCISES + BONUS CHALLENGES
# Prepared for MD Abdur Rahim · Linux Mastery Platform
# Companion script to Grep_Sed_Awk_Practice_Exercises.pdf
# ==============================================================================
set -euo pipefail

DATA_DIR="../../practice_data"
if [ ! -d "$DATA_DIR" ]; then
    DATA_DIR="./practice_data"
fi
cd "$DATA_DIR"

echo "=== SECTION 1: GREP EXERCISES (1-15) ==="
echo "[Task 1] Show all lines in app.log containing ERROR:"
grep ERROR app.log

echo -e "\n[Task 2] Count how many ERROR lines are in app.log:"
grep -c ERROR app.log

echo -e "\n[Task 3] Show ERROR and WARN lines together:"
grep -E 'ERROR|WARN' app.log

echo -e "\n[Task 4] Show all lines that are NOT INFO level in app.log:"
grep -v INFO app.log

echo -e "\n[Task 5] Show lines in app.log with line numbers:"
grep -n ERROR app.log

echo -e "\n[Task 6] Count HTTP 500 errors in access.log:"
grep -c ' 500 ' access.log

echo -e "\n[Task 7] Find all failed logins (401) in access.log:"
grep ' 401 ' access.log

echo -e "\n[Task 8] Show only active config lines in server.conf (no comments, no blanks):"
grep -Ev '^#|^$' server.conf

echo -e "\n[Task 9] Extract just IP addresses from access.log:"
grep -oE '^[0-9.]+' access.log

echo -e "\n[Task 10] Find suspicious requests (admin, wp-admin, wp-login) in access.log:"
grep -E 'admin|wp-' access.log

echo -e "\n[Task 11] Case-insensitively find 'database' in app.log:"
grep -i database app.log

echo -e "\n[Task 12] Show each ERROR in app.log with 1 line of context before and after:"
grep -C1 ERROR app.log

echo -e "\n[Task 13] List which users in users.txt use bash:"
grep '/bin/bash' users.txt

echo -e "\n[Task 14] Find users with nologin shell in users.txt:"
grep nologin users.txt

echo -e "\n[Task 15] Count total requests from IP 203.0.113.7 in access.log:"
grep -c '203.0.113.7' access.log

echo -e "\n=== SECTION 2: SED EXERCISES (16-30) ==="
echo "[Task 16] Change port from 8080 to 9090 in server.conf (preview):"
sed 's/port 8080/port 9090/' server.conf

echo -e "\n[Task 18] Delete all comment lines from server.conf (preview):"
sed '/^#/d' server.conf

echo -e "\n[Task 19] Delete both comments AND blank lines from server.conf:"
sed '/^#/d; /^$/d' server.conf

echo -e "\n[Task 20] Replace every 'info' with 'debug' in server.conf (preview):"
sed 's/info/debug/g' server.conf

echo -e "\n[Task 21] Print only lines 5 to 10 of app.log:"
sed -n '5,10p' app.log

echo -e "\n[Task 22] Print only ERROR lines from app.log using sed:"
sed -n '/ERROR/p' app.log

echo -e "\n[Task 23] Change 'localhost' to '127.0.0.1' in server.conf (preview):"
sed 's/localhost/127.0.0.1/' server.conf

echo -e "\n[Task 24] Wrap WARN with '*** WARN ***' in app.log:"
sed 's/WARN/*** WARN ***/' app.log

echo -e "\n[Task 25] Extract just usernames (text before first colon) from users.txt:"
sed 's/:.*//' users.txt

echo -e "\n[Task 26] In users.txt, replace /bin/bash with /bin/sh (preview):"
sed 's|/bin/bash|/bin/sh|g' users.txt

echo -e "\n[Task 27] Show first 5 lines of access.log using sed quit:"
sed '5q' access.log

echo -e "\n[Task 28] Add a '# ' marker before every 'port' line in server.conf:"
sed 's/^port/# port/' server.conf

echo -e "\n[Task 29] Squeeze multiple spaces into one in server.conf:"
sed 's/  */ /g' server.conf

echo -e "\n[Task 30] Swap format: 'port 8080' -> '8080 is the port' using backreferences:"
sed -E 's/port ([0-9]+)/\1 is the port/' server.conf

echo -e "\n=== SECTION 3: AWK EXERCISES (31-50) ==="
echo "[Task 31] Print just IP (field 1) from access.log:"
awk '{print $1}' access.log

echo -e "\n[Task 32] Print status code (field 9) and bytes (field 10) from access.log:"
awk '{print $9, $10}' access.log

echo -e "\n[Task 33] Show only requests that returned status 500:"
awk '$9 == 500' access.log

echo -e "\n[Task 34] Print usernames from colon-separated users.txt:"
awk -F: '{print $1}' users.txt

echo -e "\n[Task 35] Print full name (field 5) of each user in users.txt:"
awk -F: '{print $5}' users.txt

echo -e "\n[Task 36] From employees.csv, print employee name and salary (skip header):"
awk -F, 'NR>1 {print $2, $4}' employees.csv

echo -e "\n[Task 37] Total bytes served (field 10) in access.log:"
awk '{sum += $10} END {print sum}' access.log

echo -e "\n[Task 38] Average salary of all employees:"
awk -F, 'NR>1 {sum += $4; n++} END {print sum/n}' employees.csv

echo -e "\n[Task 39] Average salary of Engineering department only:"
awk -F, '$3=="Engineering" {sum += $4; n++} END {print sum/n}' employees.csv

echo -e "\n[Task 40] Count requests per IP (top talkers):"
awk '{c[$1]++} END {for (ip in c) print c[ip], ip}' access.log | sort -rn

echo -e "\n[Task 41] Count occurrences per HTTP status code:"
awk '{c[$9]++} END {for (s in c) print c[s], s}' access.log | sort -rn

echo -e "\n[Task 42] Count employees per department:"
awk -F, 'NR>1 {c[$3]++} END {for (d in c) print d, c[d]}' employees.csv

echo -e "\n[Task 43] Sum total salary per city:"
awk -F, 'NR>1 {s[$5]+=$4} END {for (city in s) print city, s[city]}' employees.csv

echo -e "\n[Task 44] Print employees earning more than 5000:"
awk -F, 'NR>1 && $4>5000 {print $2, $4}' employees.csv

echo -e "\n[Task 45] Count ERROR, WARN, INFO lines in app.log in one command:"
awk '{c[$3]++} END {for (l in c) print l, c[l]}' app.log

echo -e "\n[Task 46] Print last field (NF) of each access.log line:"
awk '{print $NF}' access.log

echo -e "\n[Task 47] Show requests larger than 4000 bytes with IP and size:"
awk '$10 > 4000 {print $1, $10}' access.log

echo -e "\n[Task 48] Formatted report: IP and status for 500 errors:"
awk '$9==500 {printf "%-16s status %s\n", $1, $9}' access.log

echo -e "\n[Task 49] Largest response (max bytes) in access.log:"
awk '$10 > max {max = $10} END {print max}' access.log

echo -e "\n[Task 50] Mini log summary: total lines, error count, and error rate percentage:"
awk '/ERROR/{e++} {t++} END {printf "Total:%d Errors:%d Rate:%.1f%%\n", t, e, e/t*100}' app.log

echo -e "\n=== BONUS COMBO CHALLENGES (C1-C5) ==="
echo "[Task C1] Top 3 IPs by request count:"
grep -oE '^[0-9.]+' access.log | sort | uniq -c | sort -rn | head -3

echo -e "\n[Task C2] All IPs that caused 500 error (unique):"
awk '$9==500 {print $1}' access.log | sort -u

echo -e "\n[Task C3] Attacker IP and probe counts:"
awk '$9==403 || $9==404 {print $1}' access.log | sort | uniq -c | sort -rn

echo -e "\n[Task C4] Active config values with log level modified to debug:"
grep -Ev '^#|^$' server.conf | sed 's/log_level info/log_level debug/'

echo -e "\n[Task C5] Total bytes served per status code:"
awk '{bytes[$9] += $10} END {for (s in bytes) print s, bytes[s]}' access.log | sort -rn

echo -e "\nAll 50 exercises + bonus challenges executed successfully!"
