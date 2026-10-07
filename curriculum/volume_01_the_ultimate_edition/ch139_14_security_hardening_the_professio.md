14. Security Hardening — The Professional Standard
Threat model of a public server
Within minutes of getting a public IP, automated scanners probe: SSH password guessing (thousands/day),
known CVE exploits against web software, and misconfiguration hunting (open databases, .env files served
by the webserver, .git directories exposed). Hardening defeats the automated 99%; the remaining 1% is
defeated by patching fast.

The first hour — complete, in order
# 1. as root on the fresh VPS:
adduser deploy && usermod -aG sudo deploy
rsync -a ~/.ssh /home/deploy/ && chown -R deploy: /home/deploy/.ssh
# 2. TEST in a NEW terminal:
ssh deploy@server sudo whoami # must print: root
# 3. lock the doors — /etc/ssh/sshd_config.d/hardening.conf:
PermitRootLogin no
PasswordAuthentication no
MaxAuthTries 3
sudo systemctl restart ssh
# 4. firewall:
sudo ufw default deny incoming
sudo ufw allow OpenSSH && sudo ufw allow 80,443/tcp
sudo ufw enable
# 5. automatic defense:
sudo apt install -y fail2ban unattended-upgrades
sudo dpkg-reconfigure -plow unattended-upgrades