4. PostgreSQL reachable only from the machine itself; remote access goes through SSH tunnels (Ch. 10).

When you suspect a compromise
ps auxf | less
sudo ss -tp | grep -v "your-ip"
crontab -l; sudo ls /etc/cron*; systemctl list-timers
find / -mtime -2 -type f 2>/dev/null | grep -vE "^/(proc|sys|var/log)" | head -50
last -50