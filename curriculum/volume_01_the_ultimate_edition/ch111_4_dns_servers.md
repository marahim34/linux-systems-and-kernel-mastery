4. DNS servers.
5. netplan try applies AND AUTO-REVERTS in 120 s unless you confirm — the seatbelt that prevents locking yourself
out of a remote machine with a bad network config. Never use plain 'apply' remotely.

Under ufw's hood — nftables/iptables literacy
ufw is a friendly front-end; the kernel's real firewall is nftables (successor to iptables). You don't need to write
raw rules often, but you must be able to READ them when debugging 'why is this blocked?' — especially
since Docker inserts its own rules that bypass ufw.
sudo nft list ruleset | less
sudo iptables -L -n -v | head -30
sudo iptables -t nat -L -n