6. Which services slow down your boot — performance forensics.

A production-grade unit file, annotated
[Unit]
Description=GoOdo API
After=network-online.target postgresql.service
Wants=network-online.target
[Service]
Type=simple
User=deploy
Group=deploy
WorkingDirectory=/opt/goodo/backend
EnvironmentFile=/opt/goodo/.env
ExecStart=/opt/goodo/venv/bin/uvicorn main:app --port 8000
Restart=on-failure
RestartSec=5
NoNewPrivileges=true
ProtectSystem=full
[Install]
WantedBy=multi-user.target