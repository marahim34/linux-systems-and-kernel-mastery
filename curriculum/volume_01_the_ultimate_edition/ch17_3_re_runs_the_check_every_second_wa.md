3. Re-runs the check every second — watch your port appear as the backend starts.

find — the interrogator
find walks a directory tree and tests every entry against your conditions — then optionally acts on matches.
Grammar: find WHERE CONDITIONS ACTION.
find /var/log -name "*.log"
find . -iname "readme*"
find /home -type d -name ".ssh"
find . -type f -size +100M
find /opt -mtime -2
find . -name "*.pyc" -delete
find . -name "*.sh" -exec chmod +x {} \;
find /tmp -type f -mtime +7 -exec rm {} +