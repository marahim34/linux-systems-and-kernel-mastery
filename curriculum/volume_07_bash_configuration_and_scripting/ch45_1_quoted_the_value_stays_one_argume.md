1. Quoted, the value stays one argument. Unquoted, bash splits it on the space into two words — harmless for echo, but
disastrous for rm or cp. Always quote.

Ch.8 — Strip extension and get basename
file="/home/abdur/report.txt"
echo "${file##*/}" # report.txt (basename)
echo "${file##*/%.txt}" # WRONG: cannot chain like this
base="${file##*/}"; echo "${base%.txt}" # report

1. ${file##*/} strips the longest leading match up to the last slash, giving the basename. To also drop the extension, do it
in two steps: first the basename, then %.txt removes the trailing extension. Parameter expansions do not chain in one
expression.

Ch.9 — case for start/stop/status
case "$1" in
start) systemctl start goodo ;;
stop) systemctl stop goodo ;;
status) systemctl status goodo ;;
*) echo "Usage: $0 {start|stop|status}" >&2; exit 1 ;;
esac