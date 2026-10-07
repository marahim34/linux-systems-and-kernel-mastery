7. Apply. From Windows Explorer: \\server-ip\projects. From Linux: sudo mount -t cifs //server/projects /mnt/p -o
username=abdur.

PRO INSIGHT: Permission truth for both: the share config AND normal Linux permissions (Vol. 1 Ch. 6) must
BOTH allow access. When a share mysteriously refuses writes, check the directory's chmod/chown first — it's the
cause more often than the share config.
PRACTICE EXERCISES