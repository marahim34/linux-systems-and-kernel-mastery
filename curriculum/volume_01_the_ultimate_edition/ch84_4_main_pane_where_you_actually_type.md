4. Main pane: where you actually type. The whole cockpit survives disconnects and is waiting tomorrow.

A sane ~/.tmux.conf starter
set -g mouse on
set -g history-limit 50000
set -g base-index 1
setw -g mode-keys vi
bind r source-file ~/.tmux.conf \; display "Reloaded"