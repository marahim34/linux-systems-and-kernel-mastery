3. Check the kernel log: your 'Hello, kernel!' message appears, proving init ran.
4. lsmod lists loaded modules; yours is now among them.
5. modinfo shows the metadata you set (author, license, description).
6. rmmod REMOVES it — the exit function runs.