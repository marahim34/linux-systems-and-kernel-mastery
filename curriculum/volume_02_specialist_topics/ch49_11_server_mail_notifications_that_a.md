11. Server Mail — Notifications That Actually Arrive
The realistic goal
Running a full receiving mail server in 2026 is a specialist job (reputation, spam filtering, deliverability). What
every server DOES need is outbound notifications that arrive: cron output (Ch. 2 MAILTO), RAID alerts
(Ch. 7), fail2ban reports, backup results. The professional pattern: a tiny relay client sends through an
authenticated provider (Gmail app-password, Brevo, Mailgun).

msmtp — the five-minute relay
sudo apt install msmtp msmtp-mta mailutils
# /etc/msmtprc
defaults
auth on
tls on
account default
host smtp.gmail.com
port 587
from server@yourdomain.fi
user marahim34@gmail.com
passwordeval "cat /etc/msmtp.pass"
sudo chmod 600 /etc/msmtp.pass /etc/msmtprc
echo "Backup OK $(date)" | mail -s "[cpouta] backup" marahim34@gmail.com

1. msmtp-mta makes msmtp the system's sendmail — cron, mdadm, everything now routes through it.