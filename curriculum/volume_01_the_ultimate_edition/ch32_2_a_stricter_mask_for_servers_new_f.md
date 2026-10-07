2. A stricter mask for servers: new files 640, dirs 750 — others get nothing by default.

sudo — how it actually works





sudo systemctl restart nginx
sudo -u postgres psql
sudo visudo
# inside sudoers:
deploy ALL=(ALL) NOPASSWD: /usr/bin/systemctl restart goodo