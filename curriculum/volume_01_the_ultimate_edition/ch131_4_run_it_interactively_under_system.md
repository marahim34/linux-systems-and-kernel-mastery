4. Run it interactively under systemd's own conditions — crashes now happen in front of your eyes.

Scenario 9 — 'DNS changed but the site shows the old server'
Check propagation from multiple resolvers: dig @1.1.1.1, dig @8.8.8.8, and your local resolver — differences
= caching still expiring (that TTL you should have lowered in advance, Ch. 21). Flush local: resolvectl
flush-caches. Remember browsers keep their own cache too. Meanwhile verify the NEW server answers by
forcing the connection: curl --resolve goodo.app:443:NEW_IP https://goodo.app — tests the future before
DNS agrees.

Scenario 10 — 'Certificate expired'




echo | openssl s_client -connect goodo.app:443 2>/dev/null | openssl x509 -noout -dates
sudo certbot renew --dry-run
systemctl list-timers | grep certbot
sudo certbot renew --force-renewal && sudo systemctl reload nginx