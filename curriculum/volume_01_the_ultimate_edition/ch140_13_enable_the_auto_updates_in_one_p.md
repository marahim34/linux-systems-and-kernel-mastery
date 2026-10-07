13. Enable the auto-updates in one prompt. Total time: ~15 minutes. This blocks the vast majority of real-world
compromises.

Verifying your defenses




sudo fail2ban-client status sshd
sudo grep "Failed password" /var/log/auth.log | wc -l
sudo lastb | head
last -20
sudo ss -tulpn | grep -v "127.0.0.1"