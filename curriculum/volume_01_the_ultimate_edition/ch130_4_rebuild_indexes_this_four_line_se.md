4. Rebuild indexes. This four-line sequence resurrects most broken package systems.

Scenario 8 — 'The service restarts in a loop'
systemctl status goodo
journalctl -u goodo --since -10m | grep -B2 -A8 "Traceback\|error"
systemctl show goodo -p Restart,RestartSec,NRestarts
sudo systemd-run --uid=deploy --pty /opt/goodo/venv/bin/uvicorn main:app