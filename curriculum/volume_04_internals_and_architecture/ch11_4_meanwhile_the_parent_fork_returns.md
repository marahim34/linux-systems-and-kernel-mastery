4. Meanwhile the parent (fork returns the child's PID)...
5. ...waits for the child (now ls) to finish, then continues. This fork-then-exec dance starts EVERY program on the
system.





PRO INSIGHT: Unique point: separating fork (copy) from exec (transform) seems wasteful but is genius. It means
the brief moment BETWEEN them is where the shell sets up redirections and pipes (Volume 3). The child can
rearrange its own file descriptors before becoming the new program. This is exactly how command > file.txt and
pipelines work under the hood — the plumbing is done in the gap between fork and exec. No other design makes
I/O redirection so clean.

The process tree — everything has a parent
Because every process is forked from another, all processes form one giant family tree. At the root sits PID 1,
systemd, started directly by the kernel at boot. Kill a parent and its orphaned children are adopted by PID 1.
This tree structure is why signals, permissions and cleanup all cascade predictably.
pstree -p | head -20
ps -ef --forest | head -20
cat /proc/self/status | grep -E "^(Name|Pid|PPid)"