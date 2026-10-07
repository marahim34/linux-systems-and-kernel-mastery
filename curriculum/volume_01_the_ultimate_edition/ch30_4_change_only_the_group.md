4. Change only the group.

Groups — collaboration without chaos
sudo groupadd developers
sudo usermod -aG developers abdur
groups abdur
sudo mkdir /srv/shared
sudo chgrp developers /srv/shared
sudo chmod 2775 /srv/shared