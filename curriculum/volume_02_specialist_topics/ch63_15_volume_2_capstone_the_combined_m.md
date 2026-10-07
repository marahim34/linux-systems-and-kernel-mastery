15. Volume 2 Capstone & the Combined Master Plan
Capstone 2 — the professional infrastructure
Extend your Volume 1 production server into a small professional infrastructure. Every piece below is a
chapter of this volume; together they form a setup many real companies would envy.
Component

Built from

Acceptance test

Private git remote with
deploy-on-push

Ch. 1

git push private main updates the live service

All alerts by mail

Ch. 2, 11

cron failure, RAID test alert, and cert-expiry warning all reach your
phone

Internal TLS everywhere

Ch. 3

curl with no -k against internal services

WireGuard mesh

Ch. 4

laptop + phone + server tunneled; DB reachable ONLY via wg0

Encrypted backup disk

Ch. 5

auto-unlocked at boot; header backup stored off-site

NFS share over the VPN

Ch. 6

mounted with _netdev, survives reboot

Monitored RAID 1 (VM)

Ch. 7

failure drill passed, alert mail received

AppArmor profile on the app

Ch. 8

app cannot read /etc/passwd; uploads still work

Audit trail on secrets

Ch. 9

ausearch names who read .env, through sudo

Dual-stack serving

Ch. 10

curl -4 and curl -6 both return 200

Everything as Ansible

Ch. 13

fresh VPS to full stack in ONE playbook run; second run all-green

The app on k3s (VM)

Ch. 14

kill-a-pod self-healing + rolling upgrade demonstrated

The combined master plan — Volumes 1 + 2
Phase

Weeks

Content

Core

1–11

Volume 1 chapters 1–14 (the original plan)

Power

12–16

Vol. 1: boot/kernel, tmux, vim, WSL, Docker, Postgres, debugging, scenarios

Capstone 1

17–18

Production server + rebuild-from-notes

Specialist

19–24

Vol. 2: git server, TLS, WireGuard, LUKS, NFS/RAID, MAC, auditd, IPv6, mail

Automation

25–27

Modern CLI week, then Ansible: capstone 1 fully as code

Orchestration

28–29

k3s primer + capstone 2 acceptance tests

Mastery

30+

Operate it. Incident journal. RHCSA/LPIC-2 if certifying. Teach someone — the final test
of understanding.

Two volumes, one path. Nothing essential remains outside these pages —
only practice remains outside them.