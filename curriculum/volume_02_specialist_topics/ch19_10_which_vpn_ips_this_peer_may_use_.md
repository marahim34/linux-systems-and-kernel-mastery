10. Which VPN IPs this peer may use — /32 = exactly one address.
sudo systemctl enable --now wg-quick@wg0
sudo wg show

1. wg-quick@ is a template unit: the tunnel is now a normal systemd service, up at every boot.