3. ACLs can add rules invisible to ls -l — check when normal perms look correct.

Scenario 7 — 'apt is broken'
sudo dpkg --configure -a
sudo apt -f install
sudo rm /var/lib/apt/lists/lock /var/lib/dpkg/lock* # ONLY if no apt runs
sudo apt update