5. Last 50 log lines if anything looks wrong.

systemd timers — cron's successor
# backup.timer
[Timer]
OnCalendar=*-*-* 03:00:00
Persistent=true
[Install]
WantedBy=timers.target