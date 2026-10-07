6. Change it now (lost at reboot)...
7. ...and persist it. sysctl.d is where server tuning lives: swappiness, network buffers, file limits.
ulimit -n
# /etc/security/limits.d/goodo.conf
deploy soft nofile 65535
deploy hard nofile 65535