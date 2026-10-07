9. Auditing & Accountability — auditd
What auditd answers
Logs say what applications reported. The audit subsystem records what the KERNEL saw: who read that file,
who ran that command, who changed that config — with user, process, and timestamp. It answers 'who
touched this?' with evidence, which is precisely what bank-grade compliance (hello, eQuorum customers)
requires.
sudo apt install auditd audispd-plugins
sudo auditctl -w /etc/passwd -p wa -k identity
sudo auditctl -w /opt/goodo/.env -p rwa -k secrets
sudo auditctl -a always,exit -F arch=b64 -S execve -F auid>=1000 -k commands
sudo auditctl -l