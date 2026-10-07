5. What listens on v6. Note: many services bind BOTH protocols via one v6 socket (shown as *:80).

The three practical implications
# 1. firewall BOTH stacks — ufw does automatically; raw nftables must:
sudo ip6tables -L -n | head -5
# 2. nginx must listen on both:
listen 80;
listen [::]:80;
# 3. v6 addresses in URLs and configs need brackets:
curl http://[2a01:4f9::1]:8000/health