5. First failing layer → its logs hold the answer.

Scenario 2 — 'Disk full' (df says 100%)
df -h # which filesystem?
sudo du -xh --max-depth=2 / 2>/dev/null | sort -rh | head
sudo lsof +L1 # deleted-but-held files?
journalctl --disk-usage # journal bloat?
sudo apt clean