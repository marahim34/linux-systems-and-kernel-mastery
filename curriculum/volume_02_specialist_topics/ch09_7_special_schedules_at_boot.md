7. Special schedules: at boot...
8. ...and shorthand for common intervals (@hourly, @weekly, @monthly).

The environment problem — solved properly
# top of crontab:
SHELL=/bin/bash
PATH=/usr/local/bin:/usr/bin:/bin
MAILTO=marahim34@gmail.com
30 2 * * * /opt/scripts/backup.sh >> /var/log/backup.log 2>&1