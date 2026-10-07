10. Networking — Complete
The mental model
A connection = source IP:port → destination IP:port over TCP or UDP. Your server has interfaces (eth0)
with IPs; services listen on ports; a firewall filters what may pass; DNS translates names to IPs. Every
network problem is one of these four layers failing — diagnose in order: interface up? → DNS resolves? →
route exists? → port open?

Layer-by-layer diagnosis — the professional sequence
ip -br a
ping -c2 1.1.1.1
ping -c2 google.com
dig +short api.goodo.app
curl -v https://api.goodo.app/health 2>&1 | tail -15