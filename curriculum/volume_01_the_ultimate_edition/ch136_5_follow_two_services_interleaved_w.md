5. Follow TWO services interleaved — watch a request flow from nginx into your app live.

Log rotation — why servers don't drown
# /etc/logrotate.d/goodo
/var/log/goodo/*.log {
daily
rotate 14
compress
delaycompress
missingok
notifempty
copytruncate
}