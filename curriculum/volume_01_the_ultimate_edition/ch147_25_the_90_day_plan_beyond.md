25. The 90-Day Plan & Beyond
Weekly schedule (≈1 hour/day)
Weeks

Chapters

Deliverable that proves it

1

1–2: foundations, terminal fluency

One week terminal-only for file management; vimtutor lesson 1–3

2

3: filesystem

Draw the / tree from memory; symlink and /proc exercises done

3

4: core commands

find one-liners solved; diff/watch in daily use

4–5

5: text processing

The 404-investigation pipeline built incrementally on a real log

6

6: permissions

Shared setgid directory working; sudoers fine-grained rule written

7

7: processes &amp; systemd

Own unit file surviving kill -9 and reboot; a systemd timer running

8

8–9: packages &amp; storage

Third-party repo added the signed way; disk added end-to-end in a
VM; swap live

9

10: networking

SSH config aliases; a working tunnel; the 5-step diagnosis narrated

10

11–12: scripting

getopts script + deploy script with traps and health gate; shellcheck
clean

11

13–14: monitoring &amp; security

Baseline triage saved; VPS hardened from memory under 30 min

12

15–17: boot, tmux, vim

Emergency-mode fstab repair done; tmux cockpit daily; vimtutor 1–4

13

18–19: WSL, Docker

WSL exported &amp; systemd on; compose stack with surviving
volume

14

20–22: Postgres, net, debugging

Restore drill passed; Docker/ufw trap reproduced; lsof +L1 drill done

15–16

23–24: scenarios, capstone

Six incidents solved unaided; all acceptance tests passing;
rebuild-from-notes done

After the book — the expert track
Containers: your Docker knowledge + this book = you now understand what Docker abstracts.
Configuration management: Ansible turns your runbook into executable YAML — the natural next step
after rebuilding a server by hand. Observability: Prometheus + Grafana. Certification: LPIC-1 or CompTIA
Linux+ (this book ≈ 85–90% coverage), then RHCSA for the hands-on credential employers respect most.
Above all: run real things. Your GoOdo backend, eQuorum demos, backups of your business data —
production responsibility is the greatest teacher.

You now have the map. The territory is a terminal away.
— End of the Complete Edition —

Appendix A — The One-Page Command Reference





Need

Command

Where am I / what's here

pwd · ls -lah · tree -L 2

Find files

find DIR -name 'PAT' · locate NAME

Find text

grep -rn 'PAT' DIR

Disk space

df -h · du -sh * · ncdu · lsof +L1

Memory / CPU

free -h · top · htop · vmstat 1

Service control

systemctl status|start|enable --now UNIT

Service logs

journalctl -u UNIT -f · --since '1h ago'

Ports listening

sudo ss -tulpn

Who owns a port

sudo lsof -i :PORT

Process control

ps aux · pgrep -af PAT · kill PID · pkill -f PAT

Permissions

chmod 755 F · chown user:grp F · namei -l PATH

Users

adduser U · usermod -aG GRP U · groups U

Packages

apt update · apt install P · dpkg -S FILE · dpkg -L P

Network basics

ip -br a · ping H · dig NAME · curl -v URL

Copy to server

rsync -avz SRC host:DST · scp F host:

Archive

tar -czf out.tar.gz DIR · tar -xzf F -C DIR

Follow a log

tail -f FILE · journalctl -f

Repeat with eyes

watch -n2 CMD

What is this cmd

type -a CMD · man CMD · tldr CMD

Trace a process

strace -p PID · lsof -p PID · cat /proc/PID/status

Firewall

sudo ufw status verbose · allow PORT/tcp

Certificates

certbot renew --dry-run

Docker

docker ps · logs -f C · exec -it C bash · compose up -d

PostgreSQL

sudo -u postgres psql · pg_dump -Fc DB > f.dump





Appendix B — Interview & Self-Test Questions
Answer each aloud in 2–3 sentences. If any feels shaky, its chapter number is your reading list. These mirror
real sysadmin/DevOps interview questions.

Fundamentals