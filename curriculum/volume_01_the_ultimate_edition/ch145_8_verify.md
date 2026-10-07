8. Verify

the acceptance tests below

all

Acceptance tests — prove it works
curl -s https://yourdomain/health # 1
ssh root@server # 2
sudo systemctl kill -s KILL app && sleep 6 && curl -fs https://yourdomain/health # 3
sudo reboot # then wait and: # 4
curl -fs https://yourdomain/health
systemctl list-timers | grep backup # 5
sudo ss -tulpn | grep -v 127.0.0.1 # 6