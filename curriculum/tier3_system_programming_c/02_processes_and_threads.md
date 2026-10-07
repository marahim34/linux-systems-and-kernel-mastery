# Tier 3 · Chapter 2: Process Lifecycle & POSIX Multithreading

Synthesized from *TLPI* Ch. 24-33.

## 1. Process Lifecycle
- `fork()`: Creates an almost identical clone of the calling process. Uses **Copy-On-Write (COW)**: memory pages are shared read-only until either process writes to a page, which triggers a page fault and duplicates only that page.
- `execve()`: Replaces current process image with a new executable program.
- `waitpid()`: Parent collects child exit status and prevents **Zombie processes** (terminated child whose entry remains in the kernel process table until parent calls wait).

## 2. POSIX Threads (pthreads)
Unlike processes which have independent virtual address spaces, threads in the same process share:
- Memory address space (heap, global variables, code)
- Open file descriptors
- Signal actions

Each thread gets its own private:
- Stack
- Register state
- Thread-Local Storage (TLS)

### Concurrency Primitives
- `pthread_mutex_t`: Mutual exclusion lock.
- `pthread_cond_t`: Signaling mechanism between threads for condition synchronization.
- `pthread_rwlock_t`: Multiple-reader single-writer lock.
