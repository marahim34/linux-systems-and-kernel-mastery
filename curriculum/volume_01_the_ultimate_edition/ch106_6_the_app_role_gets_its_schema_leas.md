6. The app role gets its schema. Least privilege from day one.

The two files that control access





# postgresql.conf
listen_addresses = 'localhost'
max_connections = 100
# pg_hba.conf (read top-down, first match wins)
local all postgres peer
host goodo goodo_app 127.0.0.1/32 scram-sha-256
sudo systemctl reload postgresql