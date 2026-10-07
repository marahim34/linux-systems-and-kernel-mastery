4. APT — the Debian/Ubuntu Package Manager,
Complete
The mental model
APT works with an INDEX (a local catalogue of what is available in the repositories) and the PACKAGES
themselves. You refresh the index, then install from it. This two-part design is why apt update (refresh the
catalogue) is separate from apt upgrade (install newer versions). Confusing these two is the most common
apt mistake.

The daily commands
sudo apt update
sudo apt upgrade
sudo apt install git
sudo apt install git curl htop
sudo apt remove git
sudo apt purge git
sudo apt autoremove