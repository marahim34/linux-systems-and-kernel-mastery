3. Afterwards it is a normal package: dpkg -L works, apt can remove it. It integrates into the system.

A tarball with a ready binary
tar -xzf tool-linux-amd64.tar.gz
sudo mv tool /usr/local/bin/
sudo chmod +x /usr/local/bin/tool
tool --version