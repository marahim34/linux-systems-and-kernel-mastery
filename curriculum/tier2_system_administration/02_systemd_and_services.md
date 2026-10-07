# Tier 2 · Chapter 2: Systemd Architecture & Unit Management

## 1. Systemd Architecture
Systemd is the PID 1 init system and service manager for modern Linux.
It provides socket activation, parallel service startup, cgroup resource isolation, and declarative dependency graphs.

## 2. Production Unit File Example (`/etc/systemd/system/app.service`)
```ini
[Unit]
Description=Production API Service
After=network.target postgresql.service
Wants=postgresql.service

[Service]
Type=simple
User=appuser
Group=appuser
WorkingDirectory=/opt/app
ExecStart=/usr/bin/python3 -m app.main
Restart=always
RestartSec=5s
Environment=PORT=8000
LimitNOFILE=65535

# Security hardening directives
ProtectSystem=strict
ProtectHome=true
NoNewPrivileges=true
PrivateTmp=true

[Install]
WantedBy=multi-user.target
```

## 3. Service Commands
```bash
sudo systemctl daemon-reload
sudo systemctl enable --now app.service
sudo systemctl status app.service
journalctl -u app.service -f
```
