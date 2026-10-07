6. File Sharing — NFS & Samba
Choosing
NFS

Samba (SMB)

Best for

Linux-to-Linux

Windows/macOS clients, mixed
offices

Auth model

trusts client IPs/UIDs (v4+Kerberos
for real auth)

usernames and passwords

Typical use

shared storage between servers

the office file share

NFS server in five commands
sudo apt install nfs-kernel-server
sudo mkdir -p /srv/nfs/shared
sudo chown nobody:nogroup /srv/nfs/shared
echo "/srv/nfs/shared 10.8.0.0/24(rw,sync,no_subtree_check)" | sudo tee -a /etc/exports
sudo exportfs -ra && sudo exportfs -v