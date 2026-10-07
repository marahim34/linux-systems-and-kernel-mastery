4. Syscall statistics summary — a profile of what the program spends kernel time doing.
OUTPUT

openat(AT_FDCWD, "/opt/goodo/.env", O_RDONLY) = 3
connect(4, {sa_family=AF_INET, sin_port=htons(4000),
sin_addr=inet_addr("18.156.x.x")}, 16) = -1 ETIMEDOUT

Read the story: it opened .env successfully (returned file descriptor 3), then tried TiDB on port 4000 and
timed out. Diagnosis in two lines: the config loads fine; the network path to the database is the problem. No
print-statements needed.

lsof — who holds what
sudo lsof -p 1123 | head -20
sudo lsof -i :8000
sudo lsof /mnt/data
sudo lsof +L1 | head
sudo lsof -u deploy -i