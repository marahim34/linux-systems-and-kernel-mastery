7. Processes, Signals & systemd — Complete
What a process is
A process = a running program + its memory + open files + an ID (PID) + a parent (PPID). Everything running
descends from PID 1 — which on modern Linux is systemd itself. Kill a parent shell and its children usually
die too; that's why nohup and systemd exist.
ps aux --sort=-%mem | head -8
pstree -p | head -20
pgrep -af uvicorn