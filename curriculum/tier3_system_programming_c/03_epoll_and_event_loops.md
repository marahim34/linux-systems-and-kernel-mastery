# Tier 3 · Chapter 3: High-Performance I/O Multiplexing & epoll

Synthesized from *TLPI* Ch. 63.

## 1. Why `select` and `poll` Don't Scale: O(N) vs O(1)
- `select` and `poll` require the application to pass all N monitored file descriptors into the kernel on every call, and iterate through the entire set to find active fds. As connections reach 10,000+ (the C10K problem), performance collapses.
- Linux `epoll` maintains an interest list inside kernel memory using a **Red-Black Tree**. When network events arrive, hardware interrupts place ready descriptors into a ready **Doubly Linked List**. `epoll_wait` simply inspects this ready list in **O(1)** time!

## 2. Core epoll Syscalls
```c
// 1. Create epoll instance
int epoll_fd = epoll_create1(0);

// 2. Register / modify / unregister file descriptors
struct epoll_event ev;
ev.events = EPOLLIN | EPOLLET; // Edge-Triggered
ev.data.fd = socket_fd;
epoll_ctl(epoll_fd, EPOLL_CTL_ADD, socket_fd, &ev);

// 3. Wait for events
struct epoll_event events[64];
int nfds = epoll_wait(epoll_fd, events, 64, -1);
```
