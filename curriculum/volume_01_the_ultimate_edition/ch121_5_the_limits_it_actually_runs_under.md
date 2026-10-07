5. The limits it actually runs under — service limits (Ch. 15) verified from the inside.

When it's slow, not broken
cat /proc/1123/stack
perf top
time curl -s https://api/endpoint -o /dev/null
curl -w "dns:%{time_namelookup} conn:%{time_connect} ttfb:%{time_starttransfer}\n" -o
/dev/null -s https://api/endpoint