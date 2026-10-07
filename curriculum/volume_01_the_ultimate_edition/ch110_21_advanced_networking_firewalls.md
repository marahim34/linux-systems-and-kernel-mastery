21. Advanced Networking & Firewalls
Static IPs with netplan (Ubuntu)
# /etc/netplan/01-static.yaml
network:
version: 2
ethernets:
eth0:
addresses: [192.168.1.50/24]
routes:
- to: default
via: 192.168.1.1
nameservers:
addresses: [1.1.1.1, 9.9.9.9]
sudo netplan try