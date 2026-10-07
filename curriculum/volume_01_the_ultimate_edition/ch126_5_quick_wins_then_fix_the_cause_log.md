5. Quick wins, then fix the CAUSE: logrotate config, journald caps, backups moved off-disk.

Scenario 3 — 'I'm locked out of SSH'
Console access (cPouta/Hetzner web console) is your back door — this is why providers offer it. From the
console: check sshd is running, check ufw status didn't lose the OpenSSH rule, read /var/log/auth.log for the
refusal reason, verify ~/.ssh permissions (700/600), and check fail2ban didn't ban YOUR home IP
(fail2ban-client status sshd → unban). Prevention: before restarting sshd with new config, always validate
with sshd -t and keep one session open.

Scenario 4 — 'It works in my shell but fails in cron/systemd'
journalctl -u myjob -n 20
sudo -u deploy env -i /bin/bash --noprofile --norc -c '/opt/scripts/job.sh'