8. Windows-side adb is visible in PATH — how your OnePlus connects to Flutter inside WSL.

systemd, services and networking in WSL
# /etc/wsl.conf
[boot]
systemd=true
[automount]
options = "metadata"
# Windows side: %UserProfile%\.wslconfig
[wsl2]
memory=6GB
processors=4
localhostForwarding=true