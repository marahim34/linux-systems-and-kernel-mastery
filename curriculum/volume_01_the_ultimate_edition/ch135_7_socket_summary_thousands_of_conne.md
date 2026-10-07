7. Socket summary — thousands of connections where you expect dozens tells its own story.

Interpreting a real incident
OUTPUT

$ free -h
total used free shared buff/cache available
Mem: 1.9Gi 1.7Gi 80Mi 12Mi 190Mi 89Mi
Swap: 0B 0B 0B
$ dmesg -T | grep -i oom
[Thu Jul 2 03:12:44] Out of memory: Killed process 1123 (uvicorn)

Diagnosis in two commands: 89 Mi available, no swap, and the kernel confesses it killed uvicorn at 03:12.
Root cause: memory exhaustion. Fixes, in order: add swap (Ch. 9), cap the service's memory in its unit
(MemoryMax=1G makes systemd restart it gracefully instead), find the leak (Ch. 13 tools), or upsize the VPS.

journalctl — the complete query language





journalctl -u goodo --since today
journalctl -u goodo -p warning --since "2 days ago"
journalctl _PID=1123
journalctl -u goodo -o json-pretty -n 1
journalctl -f -u goodo -u nginx