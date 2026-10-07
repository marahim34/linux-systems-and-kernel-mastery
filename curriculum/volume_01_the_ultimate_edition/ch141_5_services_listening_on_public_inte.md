5. Services listening on PUBLIC interfaces. Everything here is attack surface; databases should show only 127.0.0.1.

Application-level hygiene
# .env handling
chmod 600 .env && chown deploy: .env
grep -r "SECRET\|PASSWORD" --include="*.py" /opt/goodo | grep -v ".env"
# nginx: never serve dotfiles
location ~ /\. { deny all; }
# database: bind local only (postgresql.conf)
listen_addresses = 'localhost'