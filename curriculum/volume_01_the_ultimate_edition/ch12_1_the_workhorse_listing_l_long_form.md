1. The workhorse listing: -l long format, -a all files, -h human sizes.
OUTPUT

-rw-r--r-- 1 root root 3.2K Jun 30 09:14 ssh_config
drwxr-xr-x 2 root root 4.0K Jun 30 09:14 sshd_config.d
-rw------- 1 root root 505 Jun 30 09:14 ssh_host_ed25519_key

Column by column: type+permissions (d=directory, -=file, l=link), link count, owner, group, size, modified
time, name. Notice the host key: -rw------- (600) — only root can read the server's private key. Permissions
tell stories.

Copy and move — the flags that matter
cp report.pdf report_v2.pdf
cp -r project/ project_backup/
cp -a /etc/nginx /root/nginx-backup
cp -i data.csv /backup/
mv *.log old_logs/
mv -n new.conf /etc/app.conf