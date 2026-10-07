5. Only deletes EMPTY directories — a built-in safety when that is what you intend.

PRO INSIGHT: Expert habit: before any rm with a wildcard, run ls with the SAME pattern first. ls *.tmp shows
exactly what rm *.tmp will destroy. Two seconds of checking, years of regret avoided.





Viewing files — choosing the right tool
Tool

Best for

Key moves

cat

Short files, feeding pipes

cat -n adds line numbers

less

Anything long

/search, n next, G end, g start, q quit

head / tail

First/last N lines

tail -n 50; tail -f = live follow

watch

Repeating a command

watch -n 2 df -h — live disk
dashboard

diff

Comparing files

diff -u old.conf new.conf — what
changed?

tail -f /var/log/nginx/access.log
diff -u nginx.conf nginx.conf.bak
watch -n 1 "ss -tulpn | grep 8000"