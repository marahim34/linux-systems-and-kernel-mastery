5. List active rules. (These are runtime; persist in /etc/audit/rules.d/*.rules.)

Interrogating the audit trail
sudo ausearch -k secrets -ts today
sudo ausearch -k commands -ts recent -i | grep -E "proctitle" | tail
sudo aureport --summary
sudo aureport -au --failed | head
sudo ausearch -f /etc/passwd -i | tail -20