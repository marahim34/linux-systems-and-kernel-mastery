13. Ansible — Your Runbook Becomes Code
The idea
Everything you did by hand in the Volume 1 capstone — users, hardening, packages, unit files, nginx —
Ansible expresses as YAML that runs over plain SSH (no agent on servers). Two properties make it
professional-grade: idempotence (running twice changes nothing the second time — tasks describe desired
STATE, not actions) and repeatability (server #2 is one command, not one afternoon).
pipx install ansible
# inventory.ini
[web]
hetzner ansible_host=95.216.x.x ansible_user=deploy
cpouta ansible_host=86.50.20.210 ansible_user=fbmdra
ansible -i inventory.ini all -m ping
ansible -i inventory.ini all -a "df -h /"