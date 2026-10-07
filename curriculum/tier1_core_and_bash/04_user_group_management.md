# Tier 1 · Chapter 4: User & Group Management Mastery

Synthesized from *Linux User & Group Management Mastery Guide*.

## 1. Core Identity Database Files
- `/etc/passwd`: `username:password_flag:UID:GID:GECOS:home_dir:shell`
- `/etc/shadow`: Cryptographic salted hashes (mode 0640).
- `/etc/group` & `/etc/gshadow`: Group definitions and memberships.

## 2. Account Lifecycle Commands
```bash
# Create user
useradd -m -s /bin/bash -c "Developer" john

# Set password
passwd john

# Add to supplementary groups
usermod -aG sudo,docker john

# Password aging policy
chage -M 90 john
```
