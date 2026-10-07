8. Mandatory Access Control — AppArmor &
SELinux
Why rwx isn't the whole story
Classic permissions are discretionary: whatever a process's user may touch, the process may touch. If
nginx (as www-data) is exploited, the attacker gets everything www-data can reach. Mandatory access
control adds a second, non-negotiable layer: a policy says 'the nginx PROGRAM may only read /var/www
and its configs — regardless of user'. Exploited nginx now hits a wall. Ubuntu ships AppArmor; RedHat ships
SELinux.

AppArmor — Ubuntu's guardian
sudo aa-status
sudo apparmor_status | grep -A3 "enforce"
sudo dmesg | grep -i apparmor | tail -5
sudo aa-complain /etc/apparmor.d/usr.sbin.mysqld
sudo aa-enforce /etc/apparmor.d/usr.sbin.mysqld