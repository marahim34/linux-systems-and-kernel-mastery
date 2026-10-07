2. Mount it like a local disk — that's the whole client story.
3. _netdev = wait for network before mounting; nofail = boot proceeds if the server is away (Vol. 1 Ch. 9 lessons
applied).

Samba — the Windows-friendly share





sudo apt install samba
# /etc/samba/smb.conf (append)
[projects]
path = /srv/samba/projects
valid users = abdur
read only = no
create mask = 0660
sudo smbpasswd -a abdur
testparm
sudo systemctl restart smbd