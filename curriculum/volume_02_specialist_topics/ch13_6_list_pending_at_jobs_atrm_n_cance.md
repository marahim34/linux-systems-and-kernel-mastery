6. List pending at jobs (atrm N cancels).

Choosing between cron and systemd timers
Criterion

cron

systemd timer

Setup effort

one line

two files (.service + .timer)

Logging

manual redirection

automatic via journalctl

Missed runs (machine off)

lost (unless anacron)

Persistent=true catches up

Random delay (avoid stampedes)

hand-rolled sleep

RandomizedDelaySec=

Resource limits

no

full unit options (MemoryMax etc.)

Verdict

quick personal jobs

production services — prefer this

PRACTICE EXERCISES