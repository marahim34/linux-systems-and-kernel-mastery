5. All network activity of one user.

/proc — interrogating a live process





ls -l /proc/1123/cwd /proc/1123/exe
cat /proc/1123/environ | tr '\0' '\n' | head
ls -l /proc/1123/fd | head
cat /proc/1123/status | grep -E "VmRSS|Threads"
cat /proc/1123/limits | grep "open files"