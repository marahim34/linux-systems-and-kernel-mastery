4. Dynamic: a SOCKS proxy — route a browser through your server (an instant poor-man's VPN).

Transferring files
scp -r ./dist hetzner:/opt/goodo/
rsync -avz --progress ./backend/ hetzner:/opt/goodo/backend/
rsync -avzn --delete ./site/ hetzner:/var/www/