5. Prefix+r reloads config without restarting.

WARNING: Long operations on servers — database migrations, big rsyncs, apt full-upgrades over SSH — belong
inside tmux, always. An upgrade killed halfway by a dropped connection can leave a system unbootable.
PRACTICE EXERCISES