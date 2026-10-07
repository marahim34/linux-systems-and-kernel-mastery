7. Remove dependencies that were installed for other packages but are no longer needed — keeps the system lean.

PRO INSIGHT: The command that fixes most 'package not found' errors: sudo apt update. If apt says it cannot find
a package you KNOW exists, your local catalogue is stale. Refresh it first. The rule of thumb: always run apt update
before apt install on a machine you have not touched in a while, or right after adding a new repository.

Understanding what apt is about to do
apt list --installed | wc -l
apt list --upgradable
apt-cache policy git
apt-mark hold postgresql-16
apt-mark unhold postgresql-16