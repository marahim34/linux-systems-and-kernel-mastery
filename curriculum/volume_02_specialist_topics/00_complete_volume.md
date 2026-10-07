# Volume 2: Specialist Topics

Solution 7 — VMs vs containers
Aspect

Virtual Machine

Container

Virtualization layer

Hardware (own kernel)

Operating system (shared kernel)

Isolation

Strong

Lighter

Startup / size

Minutes / gigabytes

Milliseconds / megabytes

Best for

Different OSes, strong isolation

Dense, many small services

Solution 8 — A process stuck in state D
State D is uninterruptible sleep — the process is blocked in a system call waiting on hardware, usually disk
or network I/O, and cannot even be killed until it returns. Theoretical causes: slow or failing disk, a stuck
NFS mount, a device not responding. Practical investigation: check what it waits on with cat
/proc/PID/stack and cat /proc/PID/wchan; check disk health with iostat -xz 1 (high await, %util near 100
confirms disk); check dmesg for I/O errors; for NFS, check the server and network. The fix addresses the
hardware or mount, not the process — you usually cannot kill a D-state process; you must clear what it is
waiting on.
cat /proc/<pid>/wchan; echo
cat /proc/<pid>/stack 2>/dev/null
iostat -xz 1 3
dmesg -T | grep -iE "i/o error|nfs|timeout" | tail

1. wchan names the kernel function the process is sleeping in — often reveals the subsystem (disk, nfs).
2. The kernel stack shows exactly where it is blocked.
3. Disk statistics: high await and %util confirm an I/O bottleneck as the cause.
4. Kernel messages for the hardware or mount errors behind the stuck state.

Every algorithm here is one you can now trace by hand. That is what
understanding, versus memorising, feels like.
— End of Volume 5 Solutions —

LINUX MASTERY
VOLUME 2 — THE SPECIALIST
TOPICS




Everything Beyond the Core: Git Servers, TLS, VPNs, Encryption, File Sharing,
RAID, SELinux/AppArmor, Auditing, IPv6, Mail, Modern CLI, Ansible & Kubernetes

Prepared for MD Abdur Rahim · Tampere, Finland · 2026





Table of Contents — Volume 2
1. Git on Linux — Workflows, Hooks & Your Own Git Server
2. Scheduling Deep Dive — cron, anacron, at & systemd timers compared
3. TLS & Certificates — openssl Fluency
4. WireGuard — Your Own VPN in Twenty Minutes
5. LUKS — Full Disk & Volume Encryption
6. File Sharing — NFS & Samba
7. Software RAID — mdadm
8. Mandatory Access Control — AppArmor & SELinux
9. Auditing & Accountability — auditd
10. IPv6 — The Essentials That Matter Now
11. Server Mail — Notifications That Actually Arrive
12. The Modern CLI — zsh, fzf, ripgrep & Friends
13. Ansible — Your Runbook Becomes Code
14. Kubernetes Primer — k3s on One Node
15. Volume 2 Capstone & the Combined Master Plan





1. Git on Linux — Workflows, Hooks & Your Own Git
Server
Linux-side git fluency
git config --global user.name "MD Abdur Rahim"
git config --global core.editor nano
git config --global init.defaultBranch main
git config --global alias.lg "log --oneline --graph --all -15"
git config --global core.autocrlf input

1. Identity for commits.
2. Editor for commit messages and rebases.
3. Modern default branch name.
4. Aliases live in git itself: git lg gives a compact graph view everywhere.
5. The WSL essential from Volume 1: commit LF, never CRLF.

Hooks — git runs your scripts
# .git/hooks/pre-commit (chmod +x)
#!/usr/bin/env bash
set -e
shellcheck scripts/*.sh
grep -rn "SECRET\|PASSWORD" --include="*.py" src/ && {
echo "Possible secret in code — commit blocked"; exit 1; }
exit 0

1. Hooks are plain scripts in .git/hooks; pre-commit runs before every commit.
2. Lint your shell scripts automatically...
3. ...and block any commit containing likely secrets. A non-zero exit cancels the commit — your first line of defense
against leaking .env contents to GitHub.

Your own git server — it's just SSH
# on the server:
sudo adduser --disabled-password git
sudo -u git mkdir -p /home/git/repos/goodo.git
sudo -u git git init --bare /home/git/repos/goodo.git
# your key into /home/git/.ssh/authorized_keys, then locally:
git remote add private git@server:repos/goodo.git
git push private main

1. A dedicated 'git' user with no password login (keys only).
2. A BARE repository: no working files, just the .git database — what servers host.
3. Normal SSH key setup from Volume 1 Ch. 14.
4. Git speaks SSH natively — no software beyond git itself was installed.
5. A fully private remote for client code (eQuorum!) that never touches GitHub. This is all GitHub fundamentally is, plus a
web UI.





Deploy-on-push — the classic hook
# server: /home/git/repos/goodo.git/hooks/post-receive (chmod +x)
#!/usr/bin/env bash
GIT_WORK_TREE=/opt/goodo git checkout -f main
sudo /usr/bin/systemctl restart goodo

1. post-receive runs after every push arrives.
2. Checks the pushed code out into the live directory...
3. ...and restarts the service (allowed via the fine-grained sudoers rule from Vol. 1 Ch. 6). Result: git push private main
IS your deployment.

PRACTICE EXERCISES
1. Set up the private bare repo on any server and push a project to it.
2. Write a pre-commit hook that blocks commits containing the word FIXME; test both paths.
3. Wire post-receive deploy for a toy app; deploy with a single push.
4. Run git lg on a busy repo and read the branch graph aloud.





2. Scheduling Deep Dive — cron, anacron, at &
timers
cron — complete syntax mastery
# m h dom mon dow command
30 2 * * * /opt/scripts/backup.sh
*/10 * * * * /opt/scripts/healthcheck.sh
0 9-17 * * 1-5 /opt/scripts/business_hours.sh
0 3 1 * * /opt/scripts/monthly_report.sh
15 4 * * sun /opt/scripts/weekly.sh
@reboot /opt/scripts/on_boot.sh
@daily /opt/scripts/daily.sh

1. Five time fields then the command.
2. Daily at 02:30.
3. */10 = every 10 minutes.
4. Ranges combine: hourly, 9–17, Monday–Friday only.
5. 1st of every month at 03:00.
6. Day names work too.
7. Special schedules: at boot...
8. ...and shorthand for common intervals (@hourly, @weekly, @monthly).

The environment problem — solved properly
# top of crontab:
SHELL=/bin/bash
PATH=/usr/local/bin:/usr/bin:/bin
MAILTO=marahim34@gmail.com
30 2 * * * /opt/scripts/backup.sh >> /var/log/backup.log 2>&1

1. Crontabs accept variable assignments at the top:
2. Explicit shell...
3. ...explicit PATH (cron's default is nearly empty — Vol. 1 Scenario 4)...
4. ...and MAILTO: any output a job produces is emailed here (see Ch. 11 for making mail actually work).
5. Belt and braces: also capture output to a log.

System crontabs, anacron, at





ls /etc/cron.daily/
cat /etc/anacrontab
at 23:30
at> /opt/scripts/one_off.sh
at> Ctrl+D
atq

1. Drop a script here for daily execution — the zero-syntax option (also cron.hourly/weekly/monthly).
2. anacron runs those directories and CATCHES UP missed runs after downtime — the reason laptop backups still
happen. (systemd timers' Persistent=true is the modern equivalent.)
3. at = run ONCE at a time: tonight's one-off maintenance...
4. ...type the commands...
5. ...end input. Also accepts: at now + 2 hours.
6. List pending at jobs (atrm N cancels).

Choosing between cron and systemd timers
Criterion

cron

systemd timer

Setup effort

one line

two files (.service + .timer)

Logging

manual redirection

automatic via journalctl

Missed runs (machine off)

lost (unless anacron)

Persistent=true catches up

Random delay (avoid stampedes)

hand-rolled sleep

RandomizedDelaySec=

Resource limits

no

full unit options (MemoryMax etc.)

Verdict

quick personal jobs

production services — prefer this

PRACTICE EXERCISES
1. Write cron expressions for: every 15 min during business hours; 1st and 15th monthly at 06:00; Saturdays 22:00.
Verify at crontab.guru.
2. Set MAILTO and prove job output arrives (after Ch. 11).
3. Schedule a one-off with at now + 5 minutes and watch it fire.
4. Convert one cron job to a timer with RandomizedDelaySec=300 and Persistent=true.





3. TLS & Certificates — openssl Fluency
The trust model in one paragraph
A certificate binds a public key to a name (api.goodo.app), signed by a Certificate Authority the client
already trusts. TLS then uses the key pair to negotiate an encrypted session. Everything else — chains,
expiry, SANs — is bookkeeping around that one idea.

Inspecting certificates — the four commands
echo | openssl s_client -connect goodo.app:443 -servername goodo.app 2>/dev/null | openssl
x509 -noout -dates -subject -issuer
openssl x509 -in cert.pem -noout -text | less
openssl s_client -connect goodo.app:443 -showcerts </dev/null 2>/dev/null | grep -c "BEGIN
CERT"
curl -vI https://goodo.app 2>&1 | grep -E "expire|issuer|SSL"

1. The live certificate: validity window, who it's for, who signed it. -servername matters on shared-IP hosts (SNI).
2. Full anatomy of a certificate file: SANs (all names it covers), key size, extensions.
3. How many certs the server sends — should be 2+ (leaf + intermediate); exactly 1 = the classic 'incomplete chain' that
browsers accept but strict clients (and Flutter apps!) reject.
4. curl's verdict on the whole setup.

Self-signed certificates — internal services done right
openssl req -x509 -newkey rsa:4096 -sha256 -days 825 \
-nodes -keyout internal.key -out internal.crt \
-subj "/CN=eq.internal" \
-addext "subjectAltName=DNS:eq.internal,IP:10.0.0.5"
chmod 400 internal.key
sudo cp internal.crt /usr/local/share/ca-certificates/
sudo update-ca-certificates

1. One command, key + certificate: 4096-bit RSA, SHA-256, ~27 months.
2. -nodes = key not password-protected (services can't type passwords at boot).
3. The certificate's primary name.
4. CRITICAL: modern clients validate the SAN field, not CN — omit this and everything rejects your cert.
5. Private key locked down (Vol. 1 Ch. 6).
6. Distribute the cert to client machines...
7. ...and register it as trusted system-wide — curl and apps now accept your internal service. This is the pattern for
eQuorum installs inside bank networks with no internet.

Keys, CSRs, and checking they match





openssl genpkey -algorithm ed25519 -out server.key
openssl req -new -key server.key -out server.csr -subj "/CN=api.bank.internal"
openssl pkey -in server.key -pubout | sha256sum
openssl x509 -in server.crt -pubkey -noout | sha256sum

1. Generate a modern key.
2. A CSR = 'please sign this public key for this name' — what you send to a corporate CA.
3. Fingerprint of the key's public half...
4. ...and of the cert's public key. IDENTICAL hashes = this key and cert belong together — the 30-second check that
prevents the 'key values mismatch' nginx startup failure.

Testing TLS without a browser
openssl s_client -connect host:443 -tls1_2 </dev/null
curl --cacert internal.crt https://eq.internal/health
openssl s_client -connect host:5432 -starttls postgres </dev/null

1. Force a protocol version — verify old TLS is disabled.
2. Test against YOUR ca file explicitly — separates 'cert broken' from 'trust store missing it'.
3. STARTTLS: check TLS on protocols that upgrade mid-connection (postgres, smtp).

PRACTICE EXERCISES
1. Inspect three public sites: read expiry, issuer, SAN list, and chain length for each.
2. Create a SAN-correct self-signed cert for a local service; trust it system-wide; get a clean curl with no -k flag.
3. Deliberately serve a mismatched key+cert in nginx, read the exact error, then prove the mismatch with the
sha256 method.
4. Set a calendar reminder pattern: openssl -dates in a monthly cron emailing you certs within 20 days of expiry.





4. WireGuard — Your Own VPN in Twenty Minutes
Why WireGuard won
WireGuard is ~4,000 lines of code (OpenVPN: ~100,000), lives in the kernel, uses modern cryptography
only, and configures like SSH: each side has a keypair; you exchange public keys; done. Use cases: reach
your home/office network from Berlin or Tivat, give your laptop a Finnish IP abroad, or link servers into a
private network where databases can safely listen.

Server setup (the VPS)
sudo apt install wireguard
wg genkey | sudo tee /etc/wireguard/server.key | wg pubkey | sudo tee
/etc/wireguard/server.pub
sudo chmod 600 /etc/wireguard/server.key
# /etc/wireguard/wg0.conf
[Interface]
Address = 10.8.0.1/24
ListenPort = 51820
PrivateKey = <contents of server.key>
PostUp = sysctl -w net.ipv4.ip_forward=1
[Peer]
# laptop
PublicKey = <laptop public key>
AllowedIPs = 10.8.0.2/32

1. One package.
2. Generate the keypair in one pipeline: private saved, public derived and saved.
3. Private key = crown jewels.
4. The config IS the interface definition:
5. The server's address inside the VPN's private subnet.
6. UDP port to open in ufw: sudo ufw allow 51820/udp.
7. Enable routing when the tunnel comes up (Vol. 1 Ch. 15 sysctl).
8. One [Peer] block per client:
9. The client's PUBLIC key — identity and encryption in one.
10. Which VPN IPs this peer may use — /32 = exactly one address.
sudo systemctl enable --now wg-quick@wg0
sudo wg show

1. wg-quick@ is a template unit: the tunnel is now a normal systemd service, up at every boot.
2. Live status: peers, last handshake, transferred bytes — 'latest handshake' seconds ago = tunnel healthy.

Client setup (laptop/phone)





# laptop /etc/wireguard/wg0.conf
[Interface]
Address = 10.8.0.2/24
PrivateKey = <laptop private key>
DNS = 1.1.1.1
[Peer]
PublicKey = <server public key>
Endpoint = 95.216.x.x:51820
AllowedIPs = 0.0.0.0/0
PersistentKeepalive = 25

1. The client's VPN address.
2. DNS while tunneled.
3. Where the server lives on the real internet.
4. THE routing decision: 0.0.0.0/0 = send ALL traffic through the VPN (full tunnel, café-WiFi mode). Alternative
10.8.0.0/24 = only VPN-network traffic (split tunnel).
5. Keepalive packets let the tunnel survive NAT routers on hotel WiFi.

On the phone: the WireGuard app imports a QR code — generate one with: qrencode -t ansiutf8 < client.conf
(apt install qrencode). Perfect for your Berlin and Montenegro trips: hotel WiFi becomes irrelevant; you
browse via your own Finnish server.
PRACTICE EXERCISES
1. Build the full server+laptop tunnel; verify with wg show and curl ifconfig.me (should show the VPS IP in full-tunnel
mode).
2. Switch AllowedIPs between full and split tunnel and demonstrate the difference with ifconfig.me.
3. Add your phone as a second peer via QR code.
4. Bind PostgreSQL to the wg0 address (10.8.0.1) and connect from the laptop over the tunnel — a database
reachable ONLY via VPN.





5. LUKS — Full Disk & Volume Encryption
What LUKS protects against — and what it doesn't
LUKS encrypts data at rest: a stolen laptop, a decommissioned VPS disk, a USB stick lost in an airport. It
does NOT protect a running, unlocked system — while mounted, files are plaintext to any process with
permissions. Remember Volume 1 Ch. 15: init=/bin/bash gives anyone with physical access a root shell —
LUKS is the answer to exactly that.

Encrypting a data disk / USB stick
sudo cryptsetup luksFormat /dev/sdb1
sudo cryptsetup open /dev/sdb1 securedata
sudo mkfs.ext4 /dev/mapper/securedata
sudo mount /dev/mapper/securedata /mnt/secure
# ... work ...
sudo umount /mnt/secure
sudo cryptsetup close securedata

1. Formats the partition as a LUKS container — DESTROYS existing data; asks for the passphrase (make it long).
2. Unlock: the decrypted view appears as /dev/mapper/securedata.
3. A normal filesystem goes INSIDE the container...
4. ...and mounts normally. Everything written is encrypted transparently.
5. Locking up: unmount...
6. ...and close. The disk is now ciphertext again — losing this USB stick in Berlin costs you hardware, not data.

Key management — the part people regret skipping
sudo cryptsetup luksAddKey /dev/sdb1
sudo cryptsetup luksRemoveKey /dev/sdb1
sudo cryptsetup luksDump /dev/sdb1 | grep -A2 "Keyslots"
sudo cryptsetup luksHeaderBackup /dev/sdb1 --header-backup-file sdb1.header

1. LUKS has 8 keyslots: add a SECOND passphrase (a long recovery phrase stored in a safe place) — one forgotten
password should not equal data loss.
2. Revoke a passphrase (e.g., after it was typed on an untrusted machine).
3. See which slots are occupied.
4. THE critical backup: the header holds the master key material — a damaged header makes the data unrecoverable
even WITH the passphrase. Store this file off-disk.

Auto-unlock for servers — crypttab





sudo dd if=/dev/urandom of=/root/.diskkey bs=64 count=1
sudo chmod 400 /root/.diskkey
sudo cryptsetup luksAddKey /dev/sdb1 /root/.diskkey
# /etc/crypttab
securedata UUID=<luks-uuid> /root/.diskkey luks
# /etc/fstab
/dev/mapper/securedata /mnt/secure ext4 defaults,nofail 0 2

1. A 64-byte random keyfile...
2. ...root-only...
3. ...added as a keyslot.
4. crypttab unlocks at boot using the keyfile (encrypted data disk + unattended reboots — the keyfile lives on the OS
disk, protecting against DATA-disk theft/disposal).
5. Then fstab mounts the mapper device as usual — the two files chain together at boot.

PRO INSIGHT: For laptops, choose 'encrypt disk' in the Ubuntu installer (LUKS on LVM on the whole disk) —
retrofitting full-disk encryption later is painful. For servers, encrypt the DATA volumes as above.
PRACTICE EXERCISES
1. Encrypt a USB stick end-to-end; unlock it, write files, close it, and inspect the raw device with strings /dev/sdb1 |
head to confirm ciphertext.
2. Add a recovery passphrase and a keyfile; luksDump to confirm three occupied slots.
3. Back up the header, luksErase a TEST container, restore the header, and recover access — the drill that teaches
why headers matter.
4. Set up crypttab+fstab auto-unlock in a VM and confirm a clean reboot mounts everything.





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

1. The server package.
2. The directory to publish.
3. Neutral ownership for a general share.
4. The export: WHO (a subnet — here, wisely, the WireGuard network from Ch. 4) and HOW (read-write, sync writes,
standard option). NEVER export to the open internet.
5. Apply and verify exports.
# client:
sudo apt install nfs-common
sudo mount -t nfs 10.8.0.1:/srv/nfs/shared /mnt/shared
# fstab:
10.8.0.1:/srv/nfs/shared /mnt/shared nfs defaults,nofail,_netdev 0 0

1. Client tools.
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

1. Share name as Windows sees it: \\server\projects.
2. Who may connect...
3. ...with write access...
4. ...and sane permissions for created files.
5. Samba keeps its OWN password database — set one per user.
6. Config syntax check (Samba's nginx -t).
7. Apply. From Windows Explorer: \\server-ip\projects. From Linux: sudo mount -t cifs //server/projects /mnt/p -o
username=abdur.

PRO INSIGHT: Permission truth for both: the share config AND normal Linux permissions (Vol. 1 Ch. 6) must
BOTH allow access. When a share mysteriously refuses writes, check the directory's chmod/chown first — it's the
cause more often than the share config.
PRACTICE EXERCISES
1. Export an NFS share restricted to your WireGuard subnet; mount from a client through the tunnel.
2. Set up the Samba share and open it from Windows Explorer (WSL host counts!).
3. Break it deliberately: chmod 500 the shared directory and observe both protocols refuse writes; fix and explain.
4. Add the NFS mount to client fstab with _netdev and verify a clean reboot.





7. Software RAID — mdadm
What RAID is and is NOT
RAID keeps a server RUNNING through a disk failure (availability). It is not a backup: deletion, ransomware,
and filesystem corruption replicate to all disks instantly. RAID + backups, never RAID instead of backups.
Level

Disks

Capacity

Survives

Use

RAID 0

2+

100%

NOTHING — any
disk dies, all data
dies

scratch speed only

RAID 1

2

50%

1 disk failure

the sane default for
small servers

RAID 5

3+

n-1 disks

1 failure

capacity-efficient;
slow rebuilds on big
disks

RAID 10

4+

50%

1 per mirror pair

databases: fast +
redundant

Building a RAID 1 mirror
sudo apt install mdadm
sudo mdadm --create /dev/md0 --level=1 --raid-devices=2 /dev/sdb /dev/sdc
cat /proc/mdstat
sudo mkfs.ext4 /dev/md0 && sudo mount /dev/md0 /mnt/raid
sudo mdadm --detail --scan | sudo tee -a /etc/mdadm/mdadm.conf
sudo update-initramfs -u

1. The software RAID toolkit.
2. Create the mirror from two whole disks.
3. The array's heartbeat file: [UU] = both members Up. Bookmark this file mentally.
4. The array is a block device like any other — filesystem, mount, fstab (by UUID!) as in Vol. 1 Ch. 9.
5. Persist the array definition...
6. ...into the boot image so the array assembles before mounting. Forgetting this = 'my RAID vanished after reboot'.

The failure drill — practice BEFORE it's real





sudo mdadm --fail /dev/md0 /dev/sdb
cat /proc/mdstat
sudo mdadm --remove /dev/md0 /dev/sdb
sudo mdadm --add /dev/md0 /dev/sdd
watch cat /proc/mdstat

1. Simulate a disk death.
2. [U_] — degraded but SERVING. This is RAID's entire value, visible.
3. Remove the 'dead' member...
4. ...add the replacement...
5. ...and watch the rebuild percentage climb. Data remained available throughout.
# /etc/mdadm/mdadm.conf
MAILADDR marahim34@gmail.com
sudo mdadm --monitor --scan --test --oneshot

1. THE line that makes RAID useful: mail on failure events (via Ch. 11's mail setup).
2. Send a test alert now. An unmonitored mirror silently degrades to one disk, then the second dies — with monitoring,
you replace the first disk calmly instead.

PRACTICE EXERCISES
1. In a VM with three virtual disks: build the mirror, run the complete failure drill, time the rebuild.
2. Reboot without the mdadm.conf/initramfs step once (in the VM) to see the failure mode, then fix it.
3. Configure MAILADDR and receive the test alert.
4. Explain to yourself (aloud) a concrete scenario where RAID 1 does NOT save you but a pg_dump does.





8. Mandatory Access Control — AppArmor &
SELinux
Why rwx isn't the whole story
Classic permissions are discretionary: whatever a process's user may touch, the process may touch. If
nginx (as www-data) is exploited, the attacker gets everything www-data can reach. Mandatory access
control adds a second, non-negotiable layer: a policy says 'the nginx PROGRAM may only read /var/www
and its configs — regardless of user'. Exploited nginx now hits a wall. Ubuntu ships AppArmor; RedHat ships
SELinux.

AppArmor — Ubuntu's guardian
sudo aa-status
sudo apparmor_status | grep -A3 "enforce"
sudo dmesg | grep -i apparmor | tail -5
sudo aa-complain /etc/apparmor.d/usr.sbin.mysqld
sudo aa-enforce /etc/apparmor.d/usr.sbin.mysqld

1. The overview: loaded profiles, enforce vs complain mode counts.
2. Which programs run confined right now.
3. DENIED lines: AppArmor blocking something — the FIRST place to look when a service fails mysteriously on Ubuntu
with correct rwx permissions.
4. Complain mode: log violations but allow them — the debugging switch.
5. Back to enforcing once the profile is fixed.

Writing a profile for your own service





sudo apt install apparmor-utils
sudo aa-genprof /opt/goodo/venv/bin/uvicorn
# exercise the app fully in another terminal, then (S)can, answer prompts, (F)inish
# result: /etc/apparmor.d/opt.goodo.venv.bin.uvicorn
/opt/goodo/venv/bin/uvicorn {
#include <abstractions/base>
#include <abstractions/python>
/opt/goodo/backend/** r,
/opt/goodo/backend/uploads/** rw,
network inet stream,
}

1. The profile-generation tools.
2. The learning wizard: it watches what the app ACTUALLY does...
3. ...and interviews you about each access. Exercise every feature (uploads, exports!) or the profile will block them in
production.
4. A readable result:
5. Shared base rules via includes.
6. Code readable...
7. ...only uploads writable...
8. ...network allowed. An exploited app can now write NOWHERE except uploads — a breach becomes an
inconvenience.

SELinux literacy — for RedHat-family machines and RHCSA
getenforce
sudo setenforce 0
ls -Z /var/www/html | head -3
sudo restorecon -Rv /var/www/html
sudo ausearch -m avc -ts recent | tail
sudo setsebool -P httpd_can_network_connect 1

1. Enforcing / Permissive / Disabled.
2. Permissive TEMPORARILY (the diagnostic move: problem disappears → it was SELinux; now fix properly, don't
leave it off).
3. -Z reveals security CONTEXTS on files — SELinux decides by context, not path.
4. THE fix for 90% of SELinux issues: files moved (mv keeps old context!) into /var/www get the wrong label; restorecon
relabels correctly.
5. The denial log — what was blocked and why.
6. Booleans: prepackaged policy switches — this one lets a web app make outbound connections (reverse proxy
setups). -P persists.

PRO INSIGHT: The professional pattern on both systems: when something fails with correct permissions, CHECK
THE MAC LAYER before disabling it. dmesg/AppArmor or ausearch/SELinux names the exact denial; the fix is one
profile line or one boolean — not turning off the guard.
PRACTICE EXERCISES
1. Run aa-status on Ubuntu/WSL and list which daemons are confined.
2. Generate a profile for a small script that reads one directory; verify it CANNOT read /etc/passwd in enforce mode.
3. In a Rocky/Fedora VM: mv an html file into /var/www, watch the 403, diagnose with ls -Z, fix with restorecon.





4. Practice the diagnostic toggle: setenforce 0 → works → setenforce 1 → fix via boolean, not via disabling.





9. Auditing & Accountability — auditd
What auditd answers
Logs say what applications reported. The audit subsystem records what the KERNEL saw: who read that file,
who ran that command, who changed that config — with user, process, and timestamp. It answers 'who
touched this?' with evidence, which is precisely what bank-grade compliance (hello, eQuorum customers)
requires.
sudo apt install auditd audispd-plugins
sudo auditctl -w /etc/passwd -p wa -k identity
sudo auditctl -w /opt/goodo/.env -p rwa -k secrets
sudo auditctl -a always,exit -F arch=b64 -S execve -F auid>=1000 -k commands
sudo auditctl -l

1. The daemon and helpers.
2. Watch /etc/passwd for writes and attribute changes, tagged 'identity'.
3. Who even READS the secrets file — every access recorded.
4. The big one: record every command executed by real (non-system) users.
5. List active rules. (These are runtime; persist in /etc/audit/rules.d/*.rules.)

Interrogating the audit trail
sudo ausearch -k secrets -ts today
sudo ausearch -k commands -ts recent -i | grep -E "proctitle" | tail
sudo aureport --summary
sudo aureport -au --failed | head
sudo ausearch -f /etc/passwd -i | tail -20

1. Everything that touched the secrets file today.
2. Recent commands, -i translating IDs to names; proctitle shows the actual command line.
3. The executive overview: events, users, files.
4. Failed authentications, tabulated — brute-force at a glance.
5. Full history of one file. Every event carries auid — the ORIGINAL login identity, surviving sudo: 'root did it' becomes
'abdur, via sudo, did it'.

PRO INSIGHT: A useful audit setup is small: watch identity files (/etc/passwd, shadow, sudoers), your secrets, your
app configs, and exec by real users. Watching everything drowns the signal and the disk.
PRACTICE EXERCISES
1. Install the four rules above, cat the .env as a normal user, and find your own access in ausearch.
2. Edit a watched file via sudo and confirm the trail shows YOUR auid, not just root.
3. Persist rules in rules.d and verify they survive a reboot (auditctl -l).
4. Generate three failed sudo attempts and locate them in aureport --failed.





10. IPv6 — The Essentials That Matter Now
Reading IPv6 without fear
An IPv6 address is eight 16-bit groups: 2a01:4f9:c010:1a2b:0000:0000:0000:0001 — compressible by
dropping leading zeros and collapsing ONE zero-run with :: → 2a01:4f9:c010:1a2b::1. Your VPS typically
gets a whole /64 (18 quintillion addresses). Addresses starting fe80:: are link-local (every interface has one,
never routed); ::1 is localhost.
ip -6 a
ping -6 -c3 google.com
dig AAAA goodo.app +short
curl -6 -sI https://ifconfig.co
sudo ss -6 -tulpn

1. Your v6 addresses — a global 2xxx/3xxx one means you're live on IPv6.
2. Force v6 reachability test.
3. AAAA is the v6 address record (A is v4) — dual-stack sites publish both.
4. Force a request over v6.
5. What listens on v6. Note: many services bind BOTH protocols via one v6 socket (shown as *:80).

The three practical implications
# 1. firewall BOTH stacks — ufw does automatically; raw nftables must:
sudo ip6tables -L -n | head -5
# 2. nginx must listen on both:
listen 80;
listen [::]:80;
# 3. v6 addresses in URLs and configs need brackets:
curl http://[2a01:4f9::1]:8000/health

1. A server 'fully firewalled' on v4 but open on v6 is a classic modern hole — verify both.
2. The bracketed form is the v6 listen — without it, v6 visitors get connection refused while 'the site works fine' on v4.
3. Brackets separate address from port — everywhere: curl, pg connection strings, ssh (ssh -6 user@[addr]).

PRO INSIGHT: Debugging asymmetry: 'the site is down' for ONE user while fine for you is increasingly a
broken-AAAA story — their network prefers v6, yours prefers v4. Test both explicitly: curl -4 and curl -6.
PRACTICE EXERCISES
1. Inventory your machines: which have global v6? Test each with ping -6.
2. Check your domains for AAAA records; if your VPS has v6, add the record and verify with curl -6.
3. Add the [::]:80 listener to an nginx site and confirm v6 serving.
4. Reproduce the asymmetry drill: curl -4 vs curl -6 against a dual-stack site of yours.





11. Server Mail — Notifications That Actually Arrive
The realistic goal
Running a full receiving mail server in 2026 is a specialist job (reputation, spam filtering, deliverability). What
every server DOES need is outbound notifications that arrive: cron output (Ch. 2 MAILTO), RAID alerts
(Ch. 7), fail2ban reports, backup results. The professional pattern: a tiny relay client sends through an
authenticated provider (Gmail app-password, Brevo, Mailgun).

msmtp — the five-minute relay
sudo apt install msmtp msmtp-mta mailutils
# /etc/msmtprc
defaults
auth on
tls on
account default
host smtp.gmail.com
port 587
from server@yourdomain.fi
user marahim34@gmail.com
passwordeval "cat /etc/msmtp.pass"
sudo chmod 600 /etc/msmtp.pass /etc/msmtprc
echo "Backup OK $(date)" | mail -s "[cpouta] backup" marahim34@gmail.com

1. msmtp-mta makes msmtp the system's sendmail — cron, mdadm, everything now routes through it.
2. Authenticated...
3. ...encrypted...
4. ...via your provider (Gmail: create an App Password; or a transactional provider's SMTP credentials).
5. Submission port.
6. The From your provider allows.
7. Password read from a file — never inline in a config that might get committed.
8. Both files locked down (Vol. 1 Ch. 6).
9. The test — and exactly how every alert in both volumes reaches your phone.

If you ever must run Postfix (send-only)
sudo apt install postfix # choose "Internet Site"
sudo postconf -e "inet_interfaces = loopback-only"
sudo postconf -e "relayhost = [smtp.eu.mailgun.org]:587"
echo test | mail -s "postfix test" you@mail.com
sudo tail -f /var/log/mail.log

1. The full MTA, when an app insists on localhost:25.
2. CRITICAL: listen on loopback ONLY — an internet-open port 25 becomes a spam relay within hours.
3. Still relay outbound through a provider.
4. Test...
5. ...and mail.log tells you exactly what happened to every message (the deliverability debugger).





Deliverability minimum for a custom From-domain
Sending as anything@yourdomain.fi requires DNS records or Gmail/Outlook will junk it: SPF (TXT: which
servers may send for the domain), DKIM (your provider gives a signing record), DMARC (policy record). All
three are copy-paste values from your relay provider's dashboard — ten minutes that decide whether alerts
arrive or vanish.
PRACTICE EXERCISES
1. Set up msmtp with a provider and receive the test mail on your phone.
2. Point cron's MAILTO at yourself and force a job to produce output.
3. Trigger the mdadm test alert from Ch. 7 through the new relay.
4. Check any domain's mail posture: dig TXT yourdomain.fi and dig TXT _dmarc.yourdomain.fi — read the
SPF/DMARC policies aloud.





12. The Modern CLI — zsh, fzf, ripgrep & Friends
zsh + a framework
sudo apt install zsh
chsh -s $(which zsh)
sh -c "$(curl -fsSL
https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
# ~/.zshrc
plugins=(git z sudo docker)

1. zsh: bash-compatible with superior completion (menu-select, typo correction, mid-word matching).
2. Make it your login shell (relog after).
3. Oh My Zsh: themes and plugins with sane defaults.
4. Plugin picks: git aliases; z = jump to any directory by fragment (z goodo); sudo = double-press Esc prefixes sudo;
docker completion. Everything from both volumes still works — zsh runs your bash knowledge.

The new-generation tools
Tool

Replaces

Why it wins

ripgrep (rg)

grep -rn

5–50x faster, respects .gitignore,
sane defaults: rg TODO

fd

find

fd -e py pattern — intuitive syntax,
fast, gitignore-aware

fzf

—

fuzzy-finds ANYTHING: Ctrl+R
history, Ctrl+T files, ** completion

bat

cat

syntax highlighting + line numbers +
git markers

eza

ls

eza -la --git — colors, tree mode, git
status column

zoxide

cd

learns your habits: z back(end) jumps
to your most-used match

jq / yq

—

query JSON/YAML in pipes: curl api |
jq '.items[].name'

btop

top/htop

the monitor you'll actually enjoy
reading

tldr

man (for recall)

examples-first help: tldr tar





sudo apt install ripgrep fd-find bat fzf jq
rg "OdometerManager" --type dart
fd -e log -x gzip {}
history | fzf
curl -s https://api.github.com/repos/flutter/flutter | jq '.stargazers_count'

1. One line installs the core set (Ubuntu names: fd is fdfind, bat is batcat — alias them).
2. Search only Dart files across the GoOdo repo — instant.
3. find+exec, modern grammar: gzip every log file.
4. Pipe ANY list into fzf for interactive fuzzy filtering.
5. The API-work staple: extract one field from JSON cleanly.

PRO INSIGHT: These tools change daily comfort, not fundamentals — which is why they're in Volume 2. Learn the
classics first (they exist on EVERY server you'll ever SSH into); enjoy the modern set on YOUR machines.
PRACTICE EXERCISES
1. Install the set, alias fdfind/batcat, and use rg + fzf for one full day of work.
2. Wire fzf keybindings (Ctrl+R/Ctrl+T) and feel history search transform.
3. Rewrite three of your old find/grep one-liners in fd/rg.
4. Use jq to extract fields from your own FastAPI endpoints' JSON.





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

1. Install on your CONTROL machine only (laptop/WSL) — servers need nothing but SSH.
2. The inventory: your machines, grouped.
3. The handshake test over SSH.
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

1. Target the [web] group.
2. become = sudo.
3. Variables once, used everywhere.
4. Every task has a NAME (the log line) and a MODULE (apt, copy, ufw...):
5. State 'present' = install if missing, do nothing if there — idempotence in action.
6. Push your Vol. 1 Ch. 14 hardening file...
7. ...and NOTIFY a handler — restarts happen once at the end, and ONLY if something actually changed.
8. Modules for everything — ufw rules as data...
9. ...with loops.
10. Templates: your unit file with {{ variables }} substituted per host.
11. Handlers: the change-triggered restart section.





ansible-playbook -i inventory.ini site.yml --check --diff
ansible-playbook -i inventory.ini site.yml
ansible-playbook -i inventory.ini site.yml

1. DRY RUN with diffs — see every change before it happens. Make this a reflex.
2. Apply: yellow 'changed' lines do work...
3. ...run again: all green 'ok', zero changes — idempotence proven. Your infrastructure is now versioned in git,
reviewable, and reproducible. This is the skill gap between 'can set up a server' and 'can operate a fleet'.

PRACTICE EXERCISES
1. Inventory your real machines and get ansible -m ping green on all.
2. Convert three manual capstone steps into tasks; verify idempotence with a double run.
3. Break something on the server by hand (remove a ufw rule); watch --check --diff detect the drift; re-apply.
4. Template your goodo.service with variables for port and user; deploy to two hosts with different values.





14. Kubernetes Primer — k3s on One Node
What Kubernetes actually is (through Linux eyes)
You know systemd keeps one machine's services alive, and Docker packages processes. Kubernetes is the
same supervision idea across MANY machines: you declare desired state ('3 replicas of this image behind
this port') and controllers reconcile reality toward it — rescheduling containers off dead nodes, rolling out new
versions gradually. k3s is a production-grade single-binary distribution, ideal for learning and small
deployments.
curl -sfL https://get.k3s.io | sh sudo k3s kubectl get nodes
sudo kubectl get pods -A

1. k3s installs as — of course — a systemd service (systemctl status k3s: everything from Vol. 1 applies).
2. Your one-node cluster reporting Ready.
3. System pods across all namespaces — Kubernetes runs itself in itself.

Deploying — declarative like Ansible, live like systemd
# app.yaml
apiVersion: apps/v1
kind: Deployment
metadata: { name: goodo }
spec:
replicas: 2
selector: { matchLabels: { app: goodo } }
template:
metadata: { labels: { app: goodo } }
spec:
containers:
- name: api
image: goodo-api:1.2
ports: [{ containerPort: 8000 }]
resources:
limits: { memory: "512Mi" }
--apiVersion: v1
kind: Service
metadata: { name: goodo-svc }
spec:
selector: { app: goodo }
ports: [{ port: 80, targetPort: 8000 }]

1. A Deployment = desired state for pods:
2. TWO copies, always.
3. Label-matching wires everything together.
4. Your Ch. 19 (Vol. 1) Docker image, unchanged.
5. cgroup limits (Vol. 1 knowledge) as YAML.
6. A Service = stable internal address load-balancing across the replicas...
7. ...port 80 in, 8000 to containers.





sudo kubectl apply -f app.yaml
sudo kubectl get pods -w
sudo kubectl delete pod goodo-xxxxx
sudo kubectl logs -l app=goodo -f
sudo kubectl set image deployment/goodo api=goodo-api:1.3
sudo kubectl rollout undo deployment/goodo

1. Declare; controllers converge.
2. Watch pods appear.
3. The magic demo: kill a pod — a replacement is running within seconds. systemd's Restart=, generalized across a
cluster.
4. Aggregated logs from all replicas by label.
5. A rolling upgrade: new pods rise, old drain, traffic never stops.
6. And the one-command rollback. Where to next: ingress (nginx's role), volumes (storage), namespaces — but this
mental model (declared state + reconciliation) IS Kubernetes.

PRACTICE EXERCISES
1. Install k3s in a VM; deploy the manifest; run the kill-a-pod demo.
2. Roll a bad image tag out, watch it fail, rollout undo.
3. Scale to 4 replicas with kubectl scale and verify with get pods.
4. Map each k8s concept to its Vol. 1 ancestor aloud: Deployment↔unit file, Service↔reverse proxy,
limits↔cgroups.





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