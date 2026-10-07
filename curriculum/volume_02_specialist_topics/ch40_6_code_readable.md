6. Code readable...
7. ...only uploads writable...
8. ...network allowed. An exploited app can now write NOWHERE except uploads — a breach becomes an
inconvenience.

SELinux literacy — for RedHat-family machines and RHCSA
getenforce
sudo setenforce 0
ls -Z /var/www/html | head -3
sudo restorecon -Rv /var/www/html
sudo ausearch -m avc -ts recent | tail
sudo setsebool -P httpd_can_network_connect 1