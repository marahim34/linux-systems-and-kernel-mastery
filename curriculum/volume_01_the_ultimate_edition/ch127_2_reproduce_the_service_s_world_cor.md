2. Reproduce the service's world: correct user, EMPTY environment, no rc files. 90% of these bugs are PATH
assumptions, missing env vars, or relative paths — fix by absolute paths + EnvironmentFile + WorkingDirectory.





Scenario 5 — 'The server is suddenly slow'
Run the Ch. 13 triage in order. Decision tree: load high + %us high → a process burns CPU (top names it).
Load high + %wa high → disk (iostat; find the writer with iotop). si/so nonzero in vmstat → swapping (memory
pressure; find the eater, add RAM/swap). Load LOW but app slow → not the machine: database queries (Ch.
20 stuck-query view), external API latency (curl timing breakdown), or connection pool exhaustion.

Scenario 6 — 'Permission denied' that makes no sense
namei -l /opt/goodo/backend/.env
sudo -u deploy cat /opt/goodo/backend/.env
getfacl /opt/goodo/backend/.env