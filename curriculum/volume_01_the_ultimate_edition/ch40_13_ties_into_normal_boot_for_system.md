13. Ties into normal boot for systemctl enable.
sudo cp goodo.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now goodo
systemctl status goodo
journalctl -u goodo -n 50