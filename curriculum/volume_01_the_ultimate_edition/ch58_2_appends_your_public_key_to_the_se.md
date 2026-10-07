2. Appends your public key to the server's ~/.ssh/authorized_keys with correct permissions.
3. -v debug mode — when login fails, the answer is ALWAYS in this output (key offered? accepted? permissions
complaint?).





# ~/.ssh/config
Host hetzner
HostName 95.216.x.x
User deploy
IdentityFile ~/.ssh/id_ed25519
ServerAliveInterval 60
Host *.tuni.fi
User marahim34