4. Ad-hoc mode: one command on EVERY server at once — already useful before writing any playbook.

A real playbook — the capstone, automated





# site.yml
- hosts: web
become: true
vars:
app_dir: /opt/goodo
tasks:
- name: Baseline packages
apt:
name: [nginx, fail2ban, git, python3-venv]
state: present
update_cache: yes
- name: Harden SSH
copy:
src: files/hardening.conf
dest: /etc/ssh/sshd_config.d/hardening.conf
notify: restart ssh
- name: Allow web ports
community.general.ufw:
rule: allow
port: "{{ item }}"
loop: ["OpenSSH", "80", "443"]
- name: App service unit
template:
src: templates/goodo.service.j2
dest: /etc/systemd/system/goodo.service
notify: restart goodo
handlers:
- name: restart ssh
service: { name: ssh, state: restarted }
- name: restart goodo
systemd: { name: goodo, state: restarted, daemon_reload: true }