8. Package Management — Complete
What a package manager actually does
A package is a compressed archive of files + metadata (version, dependencies, install scripts). The manager
keeps a database of every file it installed, resolves dependency graphs, and verifies signatures. This is why
apt install is safe and curl | sudo bash is a leap of faith.

The apt workflow, properly understood
sudo apt update
apt list --upgradable
sudo apt upgrade
sudo apt full-upgrade
sudo apt install nginx=1.24.*
apt-mark hold postgresql-16
apt depends nginx
dpkg -L nginx
dpkg -S /usr/sbin/nginx