5. Targets reached

multi-user.target (server) or
graphical.target (desktop)

Login prompt appears

systemd-analyze
systemd-analyze critical-chain
systemctl get-default
sudo systemctl set-default multi-user.target
sudo systemctl reboot --boot-loader-entry=...