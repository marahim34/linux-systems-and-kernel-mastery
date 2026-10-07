2. Live status: peers, last handshake, transferred bytes — 'latest handshake' seconds ago = tunnel healthy.

Client setup (laptop/phone)





# laptop /etc/wireguard/wg0.conf
[Interface]
Address = 10.8.0.2/24
PrivateKey = <laptop private key>
DNS = 1.1.1.1
[Peer]
PublicKey = <server public key>
Endpoint = 95.216.x.x:51820
AllowedIPs = 0.0.0.0/0
PersistentKeepalive = 25