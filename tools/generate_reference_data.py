import json

commands = [
    # File & Directory
    {"cmd": "ls", "category": "files", "desc": "List directory contents", "syntax": "ls [options] [path]", "flags": "-l (long), -a (all/hidden), -h (human sizes), -t (sort by time), -R (recursive)", "example": "ls -lah --sort=size"},
    {"cmd": "cd", "category": "files", "desc": "Change working directory", "syntax": "cd [dir]", "flags": "cd - (previous dir), cd ~ (home), cd .. (parent)", "example": "cd /var/log/nginx"},
    {"cmd": "pwd", "category": "files", "desc": "Print working directory", "syntax": "pwd [-P|-L]", "flags": "-P (physical path resolving symlinks)", "example": "pwd -P"},
    {"cmd": "mkdir", "category": "files", "desc": "Create directories", "syntax": "mkdir [options] dir...", "flags": "-p (create parent directories without error)", "example": "mkdir -p /opt/app/{src,bin,logs}"},
    {"cmd": "rm", "category": "files", "desc": "Remove files or directories", "syntax": "rm [options] file...", "flags": "-r (recursive), -f (force/no prompt), -i (interactive)", "example": "rm -rf /tmp/cache/*"},
    {"cmd": "cp", "category": "files", "desc": "Copy files and directories", "syntax": "cp [options] src dst", "flags": "-r (recursive), -a (archive: preserves perms, timestamps, owners), -u (update)", "example": "cp -a /etc/nginx /backup/nginx-conf"},
    {"cmd": "mv", "category": "files", "desc": "Move or rename files", "syntax": "mv [options] src dst", "flags": "-i (prompt before overwrite), -n (no clobber), -u (update)", "example": "mv server.conf.new server.conf"},
    {"cmd": "touch", "category": "files", "desc": "Change timestamps or create empty file", "syntax": "touch file...", "flags": "-c (do not create file if missing), -d (custom date)", "example": "touch .env.production"},
    {"cmd": "ln", "category": "files", "desc": "Make links between files", "syntax": "ln [options] target linkname", "flags": "-s (symbolic soft link), -f (force overwrite)", "example": "ln -s /etc/nginx/sites-available/app /etc/nginx/sites-enabled/"},
    {"cmd": "find", "category": "files", "desc": "Search for files in directory hierarchy", "syntax": "find [where] [criteria] [action]", "flags": "-type f/d/l, -name, -mtime, -size, -perm, -exec", "example": "find /var/log -type f -name \"*.log\" -mtime +7 -delete"},
    {"cmd": "file", "category": "files", "desc": "Determine file type via magic bytes", "syntax": "file [options] filename", "flags": "-b (brief), -i (mime type)", "example": "file /bin/bash /dev/sda"},
    {"cmd": "stat", "category": "files", "desc": "Display file or filesystem status", "syntax": "stat [options] filename", "flags": "-c (custom format: %a permissions, %s size, %i inode)", "example": "stat -c \"%a %n (inode: %i)\" /etc/passwd"},

    # Text & Streams
    {"cmd": "cat", "category": "text", "desc": "Concatenate and print files", "syntax": "cat [options] [file...]", "flags": "-n (number all lines), -b (number non-blank lines)", "example": "cat -n server.conf"},
    {"cmd": "less", "category": "text", "desc": "Interactive file pager", "syntax": "less [options] filename", "flags": "-N (line numbers), -F (quit if one screen), / (search)", "example": "less +F /var/log/syslog"},
    {"cmd": "head", "category": "text", "desc": "Output first part of files", "syntax": "head -n [lines] file", "flags": "-n 20 (first 20 lines)", "example": "head -n 5 /etc/passwd"},
    {"cmd": "tail", "category": "text", "desc": "Output last part of files", "syntax": "tail [options] file", "flags": "-n [num], -f (follow live stream), -F (follow across log rotation)", "example": "tail -Fn 50 /var/log/nginx/access.log"},
    {"cmd": "grep", "category": "text", "desc": "Print lines matching pattern", "syntax": "grep [options] PATTERN [file...]", "flags": "-i (ignore case), -v (invert), -c (count), -n (line num), -E (ERE regex), -o (only match), -r (recursive)", "example": "grep -rnE \"(ERROR|CRITICAL)\" /var/log/apps/"},
    {"cmd": "sed", "category": "text", "desc": "Stream editor for filtering and transforming text", "syntax": "sed [options] 'script' [input]", "flags": "-i (in-place edit), -E (extended regex), -n (suppress auto-print)", "example": "sed -i.bak 's/port 8080/port 9090/g' server.conf"},
    {"cmd": "awk", "category": "text", "desc": "Pattern scanning and processing language", "syntax": "awk [options] 'pattern {action}' [file]", "flags": "-F [delim] (field separator), -v var=val (set variable)", "example": "awk -F: '$3>=1000 {print $1, $3}' /etc/passwd"},
    {"cmd": "cut", "category": "text", "desc": "Remove sections from each line of files", "syntax": "cut -d[delim] -f[fields]", "flags": "-d (delimiter), -f (field numbers)", "example": "cut -d: -f1,7 /etc/passwd"},
    {"cmd": "sort", "category": "text", "desc": "Sort lines of text files", "syntax": "sort [options] [file...]", "flags": "-n (numeric), -r (reverse), -k (key column), -t (field separator), -u (unique)", "example": "sort -t: -k3,3n /etc/passwd"},
    {"cmd": "uniq", "category": "text", "desc": "Report or omit repeated lines", "syntax": "uniq [options] [input]", "flags": "-c (prefix count), -d (only duplicate lines), -u (only unique lines)", "example": "awk '{print $1}' access.log | sort | uniq -c | sort -rn"},
    {"cmd": "tr", "category": "text", "desc": "Translate or delete characters", "syntax": "tr [options] SET1 [SET2]", "flags": "-d (delete), -s (squeeze repeats)", "example": "cat input.txt | tr 'a-z' 'A-Z'"},
    {"cmd": "wc", "category": "text", "desc": "Print newline, word, and byte counts", "syntax": "wc [options] [file...]", "flags": "-l (lines), -w (words), -c (bytes), -m (chars)", "example": "wc -l < /etc/passwd"},

    # System & Process Management
    {"cmd": "ps", "category": "process", "desc": "Report current process snapshot", "syntax": "ps [options]", "flags": "aux (all users, BSD style), -ef (standard syntax), -eo pid,user,%cpu,%mem,comm", "example": "ps -eo pid,user,%cpu,%mem,comm --sort=-%cpu | head -10"},
    {"cmd": "top / htop", "category": "process", "desc": "Dynamic real-time process viewer", "syntax": "htop", "flags": "P (sort by CPU), M (sort by MEM), k (kill process)", "example": "top -b -n 1 | head -20"},
    {"cmd": "kill", "category": "process", "desc": "Send signal to process", "syntax": "kill -SIGNAL PID", "flags": "-15 (SIGTERM: graceful), -9 (SIGKILL: uncatchable), -1 (SIGHUP: reload config)", "example": "kill -TERM 1420"},
    {"cmd": "killall", "category": "process", "desc": "Kill processes by name", "syntax": "killall [options] name", "flags": "-w (wait for processes to die)", "example": "killall -9 nginx"},
    {"cmd": "pkill / pgrep", "category": "process", "desc": "Signal or list processes based on name and attributes", "syntax": "pgrep [options] pattern", "flags": "-u [user], -f (full commandline match)", "example": "pgrep -l -u root sshd"},
    {"cmd": "systemctl", "category": "process", "desc": "Control the systemd system and service manager", "syntax": "systemctl [command] [unit]", "flags": "start, stop, restart, reload, status, enable, disable, daemon-reload", "example": "systemctl enable --now docker.service"},
    {"cmd": "journalctl", "category": "process", "desc": "Query the systemd journal", "syntax": "journalctl [options]", "flags": "-u [unit], -f (follow live), -b (current boot), -p err (filter by priority)", "example": "journalctl -u nginx.service -f --since \"1 hour ago\""},
    {"cmd": "lsof", "category": "process", "desc": "List open files and network sockets", "syntax": "lsof [options]", "flags": "-i :[port] (filter by port), -p [pid], +D [dir] (files open in dir)", "example": "lsof -i :8080 -sTCP:LISTEN"},
    {"cmd": "strace", "category": "process", "desc": "Trace system calls and signals", "syntax": "strace [options] command", "flags": "-p [pid] (attach), -e trace=[syscalls], -c (summary count), -f (follow forks)", "example": "strace -e openat,read,write -p 1234"},

    # Users, Groups & Security
    {"cmd": "useradd", "category": "security", "desc": "Create a new user account", "syntax": "useradd [options] username", "flags": "-m (create home), -s (login shell), -G (supplementary groups)", "example": "useradd -m -s /bin/bash -G sudo,docker devuser"},
    {"cmd": "usermod", "category": "security", "desc": "Modify a user account", "syntax": "usermod [options] username", "flags": "-aG (append supplementary group), -s (change shell), -L (lock account)", "example": "usermod -aG sudo aisha"},
    {"cmd": "userdel", "category": "security", "desc": "Delete a user account", "syntax": "userdel [-r] username", "flags": "-r (remove home directory and mail spool)", "example": "userdel -r tempuser"},
    {"cmd": "passwd", "category": "security", "desc": "Change user password", "syntax": "passwd [username]", "flags": "-l (lock), -u (unlock), -e (force expire)", "example": "passwd devuser"},
    {"cmd": "chown", "category": "security", "desc": "Change file owner and group", "syntax": "chown [options] user[:group] file...", "flags": "-R (recursive)", "example": "chown -R www-data:www-data /var/www/html"},
    {"cmd": "chmod", "category": "security", "desc": "Change file access permissions", "syntax": "chmod [options] mode file...", "flags": "-R (recursive), 755 / 644 / u+x", "example": "chmod 600 ~/.ssh/id_ed25519"},
    {"cmd": "chage", "category": "security", "desc": "Change user password expiry information", "syntax": "chage [options] username", "flags": "-l (list aging info), -M (max days), -W (warning days)", "example": "chage -l aisha"},
    {"cmd": "sudo", "category": "security", "desc": "Execute a command as another user (typically superuser)", "syntax": "sudo [options] command", "flags": "-u (as user), -i (login shell), -l (list privileges)", "example": "sudo -u postgres psql"},

    # Network & Connectivity
    {"cmd": "ip", "category": "network", "desc": "Show / manipulate routing, network devices, interfaces and tunnels", "syntax": "ip [object] [command]", "flags": "addr (show IP), route (show routing table), link (show interfaces)", "example": "ip -br addr show"},
    {"cmd": "ss", "category": "network", "desc": "Investigate sockets (modern replacement for netstat)", "syntax": "ss [options]", "flags": "-t (tcp), -u (udp), -l (listening), -p (process info), -n (numeric ports)", "example": "ss -tulpn"},
    {"cmd": "ping", "category": "network", "desc": "Send ICMP ECHO_REQUEST to network hosts", "syntax": "ping [options] destination", "flags": "-c [count], -i [interval], -W [timeout]", "example": "ping -c 4 8.8.8.8"},
    {"cmd": "curl", "category": "network", "desc": "Transfer data from or to a server", "syntax": "curl [options] [URL...]", "flags": "-I (headers only), -s (silent), -L (follow redirects), -X (HTTP method), -d (body)", "example": "curl -sI https://api.github.com | head -5"},
    {"cmd": "dig", "category": "network", "desc": "DNS lookup utility", "syntax": "dig [@server] name [type]", "flags": "+short (concise answer), +trace (full delegation path)", "example": "dig +short github.com A"},
    {"cmd": "nc / netcat", "category": "network", "desc": "Arbitrary TCP and UDP connections and listens", "syntax": "nc [options] host port", "flags": "-z (port scan/zero I/O), -v (verbose), -l (listen mode)", "example": "nc -zv 127.0.0.1 8080"},

    # Storage & Kernel
    {"cmd": "df", "category": "storage", "desc": "Report file system disk space usage", "syntax": "df [options] [file...]", "flags": "-h (human readable), -T (print filesystem type), -x tmpfs", "example": "df -hT -x tmpfs"},
    {"cmd": "du", "category": "storage", "desc": "Estimate file space usage", "syntax": "du [options] [path...]", "flags": "-s (summary), -h (human readable), -d [depth]", "example": "du -sh /var/log/* | sort -hr | head -10"},
    {"cmd": "lsblk", "category": "storage", "desc": "List information about block devices", "syntax": "lsblk [options]", "flags": "-f (filesystem info), -m (permissions), -p (full path)", "example": "lsblk -f"},
    {"cmd": "uname", "category": "kernel", "desc": "Print system information", "syntax": "uname [options]", "flags": "-r (kernel release), -m (hardware machine), -a (all info)", "example": "uname -a"},
    {"cmd": "dmesg", "category": "kernel", "desc": "Print or control the kernel ring buffer", "syntax": "dmesg [options]", "flags": "-T (human timestamps), -l [level] (filter err,warn,info), -w (follow)", "example": "dmesg -T -l err,warn | tail -20"},
    {"cmd": "lsmod", "category": "kernel", "desc": "Show the status of modules in the Linux Kernel", "syntax": "lsmod", "flags": "Reads from /proc/modules", "example": "lsmod | grep kvm"},
    {"cmd": "insmod / rmmod", "category": "kernel", "desc": "Insert or remove a module from Linux Kernel", "syntax": "insmod file.ko / rmmod modname", "flags": "Direct syscalls init_module / delete_module", "example": "sudo insmod char_dev.ko"},
    {"cmd": "modinfo", "category": "kernel", "desc": "Show information about a Linux Kernel module", "syntax": "modinfo [options] filename", "flags": "-p (parameters), -a (author), -d (description)", "example": "modinfo e1000e"}
]

interview_questions = [
    {
        "id": "q01",
        "level": "Junior / Core",
        "category": "Processes",
        "question": "What is the difference between a process and a thread in Linux?",
        "answer": "In Linux, a process has its own private address space (memory page tables, heap, globals), file descriptor table, and credentials. A thread is an execution context (created via clone() with CLONE_VM, CLONE_FS, CLONE_FILES flags) that shares the parent process's memory space and open descriptors, but retains its own execution stack, register state, and TID (Task ID). Under the Linux kernel, both are represented by struct task_struct; the kernel scheduler schedules 'tasks' regardless of whether they share memory."
    },
    {
        "id": "q02",
        "level": "Junior / Core",
        "category": "Filesystems",
        "question": "What is an Inode, and what happens when you delete a file that is currently held open by a running process?",
        "answer": "An Inode (index node) is a kernel data structure on disk storing all file metadata (size, permissions, timestamps, owner, pointers to data blocks) except the filename. A directory entry (dentry) maps a filename string to an inode number. Each inode maintains a reference link counter (i_nlink). When you run 'rm', it decrements the link counter and unlinks the name. If a process still has the file open, the kernel holds an open file descriptor reference. The disk data blocks are NOT freed until the last open file descriptor is closed (or the process exits). You can verify this using 'lsof +L1'."
    },
    {
        "id": "q03",
        "level": "Intermediate / Sysadmin",
        "category": "Memory",
        "question": "What is the Linux Page Cache, and why does 'free -m' show high RAM usage even on an idle server?",
        "answer": "Unused RAM is wasted RAM. Linux automatically utilizes free physical memory as a Page Cache to cache disk read and write blocks (dirty pages). When user applications demand more memory, the kernel immediately and transparently reclaims pages from the page cache. The true measure of available memory is 'MemAvailable' in /proc/meminfo, not 'free'."
    },
    {
        "id": "q04",
        "level": "Intermediate / Sysadmin",
        "category": "Security",
        "question": "What are SUID and SGID permissions, and why can SUID binaries be dangerous?",
        "answer": "SUID (octal 4000) causes an executable to run with the permissions of the file's owner (often root) rather than the executing user (e.g. /usr/bin/passwd). SGID (2000) on files does the same for the group; on directories, it forces new files to inherit the parent directory's group ID. SUID binaries are high-risk attack surfaces: buffer overflows, environment variable injection (e.g. LD_PRELOAD), or path hijacking inside a root-owned SUID program can immediately yield a root shell."
    },
    {
        "id": "q05",
        "level": "Advanced / Systems",
        "category": "Syscalls & I/O",
        "question": "Why is epoll superior to select() and poll() for high-concurrency network servers (C10K)?",
        "answer": "select() and poll() have O(N) complexity: on every single invocation, the application must copy an array of N file descriptors from user space into kernel space, and the kernel must iterate linearly through all N descriptors. In contrast, epoll creates an in-kernel interest list backed by a Red-Black tree. File descriptors are added once via epoll_ctl(). When network packets arrive, NIC hardware interrupts cause the kernel to add ready sockets to a ready doubly-linked list. epoll_wait() returns in O(1) time containing only descriptors with pending events."
    },
    {
        "id": "q06",
        "level": "Advanced / Systems",
        "category": "Processes & IPC",
        "question": "Explain Copy-on-Write (COW) during fork(), and what happens when the child process calls execve()?",
        "answer": "When fork() is called, the kernel does not duplicate physical memory pages. Instead, it copies the parent's page table entries and marks all shared pages as read-only. Both parent and child read from the same physical RAM. If either process attempts to write to a page, a CPU Page Fault occurs; the kernel handles the fault by allocating a new physical page, copying the 4KB data, updating that process's page table with write permission, and resuming execution. If the child immediately calls execve(), the kernel simply discards the duplicated page table and loads the new ELF binary, avoiding massive memory copy overhead."
    },
    {
        "id": "q07",
        "level": "Kernel Hacker",
        "category": "Kernel Subsystems",
        "question": "Why can you never sleep or call copy_to_user() inside an Interrupt Handler (Top Half) or while holding a spinlock?",
        "answer": "Interrupt Handlers execute in Interrupt Context, not Process Context. In interrupt context, there is no associated struct task_struct to put to sleep, no user context to switch from, and the scheduler cannot be invoked. Calling any function that might sleep (e.g., kmalloc with GFP_KERNEL, msleep, down_interruptible, or copy_to_user which might trigger a page fault needing disk swap) will cause a kernel panic or CPU hang. Spinlocks also disable preemption; sleeping while holding a spinlock results in deadlocks if another thread spins on the same lock on the same CPU."
    },
    {
        "id": "q08",
        "level": "Kernel Hacker",
        "category": "Kernel Concurrency",
        "question": "What is Read-Copy-Update (RCU) in the Linux kernel and how does it achieve lockless reads?",
        "answer": "RCU separates read operations from updates. Readers enter an RCU critical section with rcu_read_lock(), which merely disables preemption (essentially zero cost, no memory bus locks, no cache-line invalidation). Readers safely dereference pointers with rcu_dereference(). Writers make modifications by copying the data structure, modifying the private copy, and atomically publishing the new pointer using rcu_assign_pointer(). The writer then waits for a 'grace period' (via synchronize_rcu() or asynchronously with call_rcu()) during which all CPUs undergo at least one context switch, guaranteeing that all preexisting readers have finished. The writer can then safely free the old data structure."
    }
]

with open("simulator/commands_reference.json", "w") as f:
    json.dump(commands, f, indent=2)

with open("simulator/interview_questions.json", "w") as f:
    json.dump(interview_questions, f, indent=2)

print("Generated commands reference and interview questions successfully!")
