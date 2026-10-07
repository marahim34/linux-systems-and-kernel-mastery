18. WSL Mastery — Linux Inside Windows
What WSL2 actually is
WSL2 runs a real Linux kernel in a lightweight VM, with deep Windows integration: shared clipboard,
network, and cross-mounted filesystems. It is a genuine Linux — everything in this book applies — with a few
boundary rules worth mastering since it is your daily GoOdo development environment.

Managing WSL from Windows (PowerShell)
wsl --list --verbose
wsl --shutdown
wsl --terminate Ubuntu
wsl --export Ubuntu D:\backups\ubuntu.tar
wsl --import Ubuntu-Dev D:\wsl\dev D:\backups\ubuntu.tar
wsl --update