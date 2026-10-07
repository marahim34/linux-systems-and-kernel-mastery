5. Don't error if absent; skip empty files.
6. copytruncate lets the app keep writing to the same file handle — for apps that don't reopen logs on rotation.

Watching over time — lightweight and free
sudo apt install sysstat
sar -r | tail -5
sar -q -f /var/log/sysstat/sa01

1. sysstat records system metrics every 10 minutes automatically.