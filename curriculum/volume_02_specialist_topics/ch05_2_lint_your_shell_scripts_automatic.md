2. Lint your shell scripts automatically...
3. ...and block any commit containing likely secrets. A non-zero exit cancels the commit — your first line of defense
against leaking .env contents to GitHub.

Your own git server — it's just SSH
# on the server:
sudo adduser --disabled-password git
sudo -u git mkdir -p /home/git/repos/goodo.git
sudo -u git git init --bare /home/git/repos/goodo.git
# your key into /home/git/.ssh/authorized_keys, then locally:
git remote add private git@server:repos/goodo.git
git push private main