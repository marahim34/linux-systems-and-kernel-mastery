6. CPU cores for the VM.
7. localhost:8000 in a Windows browser reaches your FastAPI dev server inside WSL automatically.

WSL gotchas and their fixes
Symptom

Cause

Fix

bad interpreter: ^M

Script saved with Windows line
endings

dos2unix file.sh (or the tr -d '\r' trick
from Ch. 5)

Clock wrong after laptop sleep

VM clock drift

sudo hwclock -s or wsl --shutdown

Permissions all 777 on /mnt/d

Windows drives don't store Linux
perms

metadata option in wsl.conf (above)





Symptom

Cause

Fix

git thinks every file changed

Line-ending translation

git config --global core.autocrlf input

DNS broken on some VPNs

resolv.conf regeneration conflicts

See [network] generateResolvConf
option in wsl.conf

PRACTICE EXERCISES