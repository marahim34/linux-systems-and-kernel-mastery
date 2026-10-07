10. IPv6 — The Essentials That Matter Now
Reading IPv6 without fear
An IPv6 address is eight 16-bit groups: 2a01:4f9:c010:1a2b:0000:0000:0000:0001 — compressible by
dropping leading zeros and collapsing ONE zero-run with :: → 2a01:4f9:c010:1a2b::1. Your VPS typically
gets a whole /64 (18 quintillion addresses). Addresses starting fe80:: are link-local (every interface has one,
never routed); ::1 is localhost.
ip -6 a
ping -6 -c3 google.com
dig AAAA goodo.app +short
curl -6 -sI https://ifconfig.co
sudo ss -6 -tulpn