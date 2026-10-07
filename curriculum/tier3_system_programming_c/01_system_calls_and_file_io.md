# Tier 3 · Chapter 1: Linux System Calls & File I/O Architecture

Synthesized from *The Linux Programming Interface (TLPI)* by Michael Kerrisk.

## 1. User Space vs Kernel Space & The Syscall Boundary
Applications cannot access hardware directly. To perform I/O, they invoke a **System Call** (syscall).
1. Application calls wrapper function in glibc (e.g. `open()`).
2. Wrapper loads syscall number into register (`%rax` on x86_64) and arguments into `%rdi`, `%rsi`, `%rdx`, `%r10`, `%r8`, `%r9`.
3. CPU executes `syscall` instruction, transitioning CPU mode from Ring 3 (User) to Ring 0 (Kernel).
4. Kernel executes `sys_call_table[rax]`.
5. Kernel transitions CPU back to Ring 3 with return code in `%rax`.

## 2. Core Low-Level I/O Calls
```c
int open(const char *pathname, int flags, mode_t mode);
ssize_t read(int fd, void *buf, size_t count);
ssize_t write(int fd, const void *buf, size_t count);
off_t lseek(int fd, off_t offset, int whence);
int close(int fd);
```

### Critical Flags
- `O_RDONLY`, `O_WRONLY`, `O_RDWR`
- `O_CREAT | O_EXCL`: Atomic file creation (fails if file exists, prevents symlink race conditions).
- `O_TRUNC`: Truncate file to 0 bytes.
- `O_APPEND`: Atomic append to end of file on every write.
- `O_NONBLOCK`: Non-blocking mode (returns `EAGAIN` or `EWOULDBLOCK` instead of sleeping).
- `O_DIRECT`: Bypasses the Linux page cache for direct DMA disk transfer.
