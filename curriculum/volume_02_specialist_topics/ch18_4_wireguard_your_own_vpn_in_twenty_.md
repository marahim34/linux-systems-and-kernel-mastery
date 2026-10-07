4. WireGuard — Your Own VPN in Twenty Minutes
Why WireGuard won
WireGuard is ~4,000 lines of code (OpenVPN: ~100,000), lives in the kernel, uses modern cryptography
only, and configures like SSH: each side has a keypair; you exchange public keys; done. Use cases: reach
your home/office network from Berlin or Tivat, give your laptop a Finnish IP abroad, or link servers into a
private network where databases can safely listen.

Server setup (the VPS)
sudo apt install wireguard
wg genkey | sudo tee /etc/wireguard/server.key | wg pubkey | sudo tee
/etc/wireguard/server.pub
sudo chmod 600 /etc/wireguard/server.key
# /etc/wireguard/wg0.conf
[Interface]
Address = 10.8.0.1/24
ListenPort = 51820
PrivateKey = <contents of server.key>
PostUp = sysctl -w net.ipv4.ip_forward=1
[Peer]
# laptop
PublicKey = <laptop public key>
AllowedIPs = 10.8.0.2/32