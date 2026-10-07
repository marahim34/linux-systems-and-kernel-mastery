4. Confirm it runs. Many Go and Rust tools ship exactly like this: one self-contained binary you drop into PATH.

The curl-pipe-bash pattern — convenient but read first
# vendors often suggest:
curl -fsSL https://get.docker.com | sudo bash
# SAFER: download first, READ it, then run:
curl -fsSL https://get.docker.com -o install.sh
less install.sh
sudo bash install.sh