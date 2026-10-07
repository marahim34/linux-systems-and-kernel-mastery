3. The NAT table — where Docker's port mappings live. THE gotcha: docker run -p 5432:5432 publishes to the world
even with ufw denying it, because Docker's NAT rules run first. Bind consciously: -p 127.0.0.1:5432:5432.

WARNING: Memorize the Docker/ufw trap: published container ports bypass ufw. Always publish sensitive ports
bound to 127.0.0.1, or configure Docker's iptables integration explicitly. Countless 'hardened' servers have leaked
databases this way.

DNS — a working mental model plus tools





resolvectl status | head -15
dig goodo.app A +short
dig goodo.app MX
dig @1.1.1.1 goodo.app
dig +trace goodo.app | tail -8
dig -x 95.216.1.2