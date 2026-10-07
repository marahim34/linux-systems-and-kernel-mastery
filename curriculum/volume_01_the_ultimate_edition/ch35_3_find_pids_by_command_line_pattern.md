3. Find PIDs by command-line pattern, showing the full command (-a).

Signals — the process control vocabulary
Signal

Number

Meaning

Can be ignored?

SIGTERM

15

Please shut down cleanly
(default of kill)

Yes — apps catch it to
save state

SIGKILL

9

Die immediately, no
cleanup

NO — kernel enforces it

SIGHUP

1

Terminal closed; many
daemons treat it as 'reload
config'

Yes

SIGINT

2

Ctrl+C from keyboard

Yes

SIGSTOP/SIGCONT

19/18

Pause / resume (Ctrl+Z
uses TSTP)

STOP cannot be ignored

kill 4321
kill -9 4321
killall python3
pkill -f "uvicorn main:app"
kill -HUP $(pgrep nginx | head -1)