# Tier 1 · Chapter 3: Permissions, Ownership, and Special Bits

## 1. Traditional POSIX Permission Triplet
Linux file modes consist of 9 permission bits:
- **User (Owner)**: `rwx`
- **Group**: `rwx`
- **Others (World)**: `rwx`

## 2. Octal Numerical Representation
- Read (`r`) = 4
- Write (`w`) = 2
- Execute (`x`) = 1
Common modes: `755` (`rwxr-xr-x`), `644` (`rw-r--r--`), `600` (`rw-------`).

## 3. Special Permissions: SUID, SGID, and Sticky Bit
- **SUID (Octal 4000)**: Executable runs with permissions of the file OWNER (e.g. `/usr/bin/passwd`).
- **SGID (Octal 2000)**: On directories, newly created files inherit the parent directory GID.
- **Sticky Bit (Octal 1000)**: On world-writable directories (`/tmp`), only file owners can delete or rename files.

## 4. POSIX Access Control Lists (ACLs)
```bash
getfacl document.pdf
setfacl -m u:aisha:rw document.pdf
setfacl -x u:aisha document.pdf
```
