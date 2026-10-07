16. Terminal Multiplexing — tmux
Why tmux changes remote work
Problem: you SSH into a server, start a long job, your WiFi hiccups — the job dies with the connection. tmux
runs your terminal sessions on the server, detached from the connection. Disconnect, reconnect from
another machine, and everything is exactly where you left it: running processes, split panes, scrollback. It is
non-negotiable for server work.

The core workflow
tmux new -s deploy
# ... work happens, connection dies ...
tmux ls
tmux attach -t deploy
tmux kill-session -t deploy