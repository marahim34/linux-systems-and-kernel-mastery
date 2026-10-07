3. Symlinks show as: config.yaml -> /opt/goodo/config.yaml with an 'l' as the first permission character.
OUTPUT

lrwxrwxrwx 1 abdur abdur 24 Jul 2 10:15 /home/abdur/config.yaml -> /opt/goodo/config.yaml

Common beginner mistakes
Mistake 1: Spaces in names break commands — my file.txt is two arguments. Fix: quote it ("my file.txt") or
Tab-complete which auto-escapes. Mistake 2: Confusing / (root of tree) with ~ (your home). Mistake 3:
Working as root 'because permissions are annoying' — one typo can end the system. Mistake 4: Case
matters: File.txt and file.txt are different files.
PRACTICE EXERCISES