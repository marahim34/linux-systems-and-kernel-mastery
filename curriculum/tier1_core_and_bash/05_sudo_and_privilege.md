# Tier 1 · Chapter 5: Sudo & Privilege Escalation

Synthesized from *Sudo Mastery Complete*.

## 1. Why sudo Exists
- Granular least privilege.
- Full audit logging (`/var/log/auth.log`).
- Individual accountability (no shared root password).

## 2. Sudoers Syntax Grammar
`WHO  WHERE=(AS_WHOM)  TAGS: WHAT`

```sudoers
aisha ALL=(ALL:ALL) ALL
%sudo ALL=(ALL:ALL) ALL
marcus ALL=(ALL) NOPASSWD: /usr/bin/systemctl restart nginx
```

Always edit with `visudo` to prevent lockouts!
