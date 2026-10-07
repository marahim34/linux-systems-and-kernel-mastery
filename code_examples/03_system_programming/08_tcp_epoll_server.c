/*
 * 08_tcp_epoll_server.c - High-Performance Asynchronous Event Loop using epoll
 * Topics: epoll_create1, epoll_ctl, epoll_wait, non-blocking sockets, fcntl
 * Inspired by: TLPI Ch. 63 (Alternative I/O Models) & Modern Linux Network Systems
 */

#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <sys/epoll.h>
#include <errno.h>
#include <string.h>

#define MAX_EVENTS 16
#define TEST_PORT 18088

static int set_nonblocking(int fd) {
    int flags = fcntl(fd, F_GETFL, 0);
    if (flags == -1) return -1;
    return fcntl(fd, F_SETFL, flags | O_NONBLOCK);
}

int main(int argc, char *argv[]) {
    int port = (argc > 1) ? atoi(argv[1]) : TEST_PORT;
    int listen_fd = socket(AF_INET, SOCK_STREAM, 0);
    if (listen_fd == -1) { perror("socket"); return 1; }

    int opt = 1;
    setsockopt(listen_fd, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt));
    set_nonblocking(listen_fd);

    struct sockaddr_in saddr;
    memset(&saddr, 0, sizeof(saddr));
    saddr.sin_family = AF_INET;
    saddr.sin_addr.s_addr = INADDR_ANY;
    saddr.sin_port = htons(port);

    if (bind(listen_fd, (struct sockaddr *)&saddr, sizeof(saddr)) == -1) {
        perror("bind");
        close(listen_fd);
        return 1;
    }

    if (listen(listen_fd, SOMAXCONN) == -1) {
        perror("listen");
        close(listen_fd);
        return 1;
    }

    int epoll_fd = epoll_create1(0);
    if (epoll_fd == -1) { perror("epoll_create1"); close(listen_fd); return 1; }

    struct epoll_event ev, events[MAX_EVENTS];
    ev.events = EPOLLIN;
    ev.data.fd = listen_fd;
    epoll_ctl(epoll_fd, EPOLL_CTL_ADD, listen_fd, &ev);

    printf("[epoll Server] Listening on 0.0.0.0:%d using Linux epoll event loop...\n", port);
    printf("[epoll Server] Ready for connections (press Ctrl+C to terminate or send test request).\n");

    /* For demonstration test mode: loop with a 500ms timeout for 2 ticks if no client arrives */
    int loop_limit = (argc > 2 && strcmp(argv[2], "--once") == 0) ? 2 : 1000;
    int iterations = 0;

    while (iterations++ < loop_limit) {
        int nfds = epoll_wait(epoll_fd, events, MAX_EVENTS, 200 /* 200ms timeout */);
        if (nfds == -1) {
            if (errno == EINTR) continue;
            perror("epoll_wait");
            break;
        }

        for (int i = 0; i < nfds; i++) {
            if (events[i].data.fd == listen_fd) {
                /* Accept new client */
                struct sockaddr_in caddr;
                socklen_t clen = sizeof(caddr);
                int client_fd = accept(listen_fd, (struct sockaddr *)&caddr, &clen);
                if (client_fd != -1) {
                    set_nonblocking(client_fd);
                    struct epoll_event client_ev;
                    client_ev.events = EPOLLIN | EPOLLET; /* Edge-triggered */
                    client_ev.data.fd = client_fd;
                    epoll_ctl(epoll_fd, EPOLL_CTL_ADD, client_fd, &client_ev);
                    printf("  [epoll] Accepted new client fd=%d\n", client_fd);
                }
            } else {
                /* Client data ready */
                int fd = events[i].data.fd;
                char buf[512];
                ssize_t n = read(fd, buf, sizeof(buf) - 1);
                if (n > 0) {
                    buf[n] = '\0';
                    printf("  [epoll] Read %zd bytes from fd=%d: %s", n, fd, buf);
                    /* Echo back */
                    { ssize_t w = write(fd, "HTTP/1.1 200 OK\r\nContent-Length: 17\r\n\r\nepoll echo pong\n", 53); (void)w; }
                }
                epoll_ctl(epoll_fd, EPOLL_CTL_DEL, fd, NULL);
                close(fd);
            }
        }
    }

    close(listen_fd);
    close(epoll_fd);
    printf("[epoll Server] Shutdown cleanly.\n");
    return 0;
}
