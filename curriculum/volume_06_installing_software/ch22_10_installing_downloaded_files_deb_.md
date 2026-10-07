10. Installing Downloaded Files — .deb, tarballs,
binaries
When a vendor gives you a file directly
Sometimes a vendor (Google Chrome, Docker, Slack) offers a direct download. These come in a few forms,
each installed differently. This is the closest to the Windows experience, and the least safe, so verify your
source.

A .deb file — the Debian package
wget https://example.com/app.deb
sudo apt install ./app.deb
dpkg -L app