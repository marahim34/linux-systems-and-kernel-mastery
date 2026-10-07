5. Clean up when finished.

The prefix and the essential keys
Every tmux command starts with the prefix: Ctrl+b, then a key. Muscle memory forms within two days of
forced use.
Keys (after Ctrl+b)

Action

d

Detach — leave everything running, return to your normal
shell

c

New window (like a browser tab)

n / p / 0-9

Next / previous / jump to window number

%

Split pane vertically (side by side)

"

Split pane horizontally (stacked)

arrow keys

Move between panes

z

Zoom: current pane fullscreen; z again to restore

x

Kill current pane

[

Scroll mode — arrows/PgUp to read history, q to exit

s

Interactive session switcher

A practical layout for server work





tmux new -s goodo
# pane 1: Ctrl+b % -> journalctl -u goodo -f
# pane 2: Ctrl+b " -> htop
# pane 3: your working shell