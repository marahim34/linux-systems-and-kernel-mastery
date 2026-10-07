13. Logs, Monitoring & Performance Debugging
The USE method — how experts think
For every resource (CPU, memory, disk, network) check three things: Utilization (how busy), Saturation (how
much is queued waiting), Errors. A resource can show low utilization yet be saturated — the method catches
what intuition misses.

The 60-second triage, annotated
uptime
dmesg -T | tail -20
free -h
vmstat 1 5
top -o %CPU
iostat -xz 1 3
ss -s