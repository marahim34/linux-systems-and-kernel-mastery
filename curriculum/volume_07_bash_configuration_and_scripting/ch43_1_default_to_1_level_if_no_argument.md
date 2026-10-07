1. Default to 1 level if no argument. Build a path of N '../' segments with a loop, then cd once. up 3 climbs three
directories. || return 1 handles failure safely.

Ch.5 — Prompt with time and history number
PS1='[\A \!] \w\$ '

1. \A is the time HH:MM, \! the history number, \w the directory. The result looks like [14:30 512] ~/project$ — context
plus a command number you can recall with !512.

Ch.6 — Prove export is needed
MSG="hi"
bash -c 'echo "child sees: $MSG"' # prints: child sees:
export MSG
bash -c 'echo "child sees: $MSG"' # prints: child sees: hi