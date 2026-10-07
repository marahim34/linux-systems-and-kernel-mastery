4. What does the name resolve to? Wrong IP → your DNS record is the bug.
5. -v shows the whole conversation: TCP connect, TLS handshake, request, response. The line where it stalls names
the guilty layer.

Ports and listening services
sudo ss -tulpn
sudo ss -tn state established
nc -zv 86.50.20.210 22
curl ifconfig.me