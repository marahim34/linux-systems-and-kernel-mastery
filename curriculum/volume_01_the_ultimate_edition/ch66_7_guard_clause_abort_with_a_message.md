7. Guard clause: abort with a message if a required env variable is missing — fail fast, fail loud.





Tests and branching — the full toolkit
if [[ -f "$conf" && -r "$conf" ]]; then
source "$conf"
fi
if (( count > 100 )); then echo "high"; fi
case "$1" in
start) systemctl start goodo ;;
stop) systemctl stop goodo ;;
logs) journalctl -u goodo -f ;;
*) echo "Usage: $0 {start|stop|logs}"; exit 1 ;;
esac

1. [[ ]] for strings/files: -f exists-and-file, -r readable, combined with &&.
2. source executes another file in THIS shell — loading config variables.
3. (( )) for arithmetic: natural math syntax, no -gt needed.
4. case: the clean way to build subcommands...
5. * is the catch-all; this five-liner is a complete service control wrapper.

Arrays and loops that don't break on spaces
servers=("hetzner" "cpouta" "backup-host")
for s in "${servers[@]}"; do
ssh "$s" 'df -h /' || echo "FAILED: $s"
done
while IFS= read -r file; do
gzip "$file"
done < <(find /var/log -name "*.log" -mtime +7)