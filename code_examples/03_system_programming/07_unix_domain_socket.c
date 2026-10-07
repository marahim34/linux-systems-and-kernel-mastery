/*
 * 07_unix_domain_socket.c - Local High-Speed IPC via UNIX Domain Sockets
 * Topics: AF_UNIX, SOCK_STREAM, sockaddr_un, bind, listen, connect, accept
 * Inspired by: TLPI Ch. 57
 */

#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/socket.h>
#include <sys/un.h>
#include <sys/wait.h>
#include <string.h>

#define SOCKET_PATH "/tmp/dojo_unix_sock.socket"

void run_server(void) {
    int server_fd = socket(AF_UNIX, SOCK_STREAM, 0);
    if (server_fd == -1) { perror("server socket"); exit(1); }

    struct sockaddr_un addr;
    memset(&addr, 0, sizeof(addr));
    addr.sun_family = AF_UNIX;
    strncpy(addr.sun_path, SOCKET_PATH, sizeof(addr.sun_path) - 1);
    unlink(SOCKET_PATH);

    if (bind(server_fd, (struct sockaddr *)&addr, sizeof(addr)) == -1) {
        perror("server bind");
        exit(1);
    }

    if (listen(server_fd, 5) == -1) {
        perror("server listen");
        exit(1);
    }

    int client_fd = accept(server_fd, NULL, NULL);
    if (client_fd == -1) { perror("server accept"); exit(1); }

    char buf[128];
    ssize_t n = read(client_fd, buf, sizeof(buf) - 1);
    if (n > 0) {
        buf[n] = '\0';
        printf("  [UDS Server] Received from client: '%s'\n", buf);
        const char *reply = "PONG: Unix Domain Socket Verified!";
        ssize_t ret = write(client_fd, reply, strlen(reply)); (void)ret;
    }

    close(client_fd);
    close(server_fd);
    unlink(SOCKET_PATH);
}

void run_client(void) {
    usleep(50000); /* Wait for server socket bind */
    int client_fd = socket(AF_UNIX, SOCK_STREAM, 0);
    if (client_fd == -1) { perror("client socket"); exit(1); }

    struct sockaddr_un addr;
    memset(&addr, 0, sizeof(addr));
    addr.sun_family = AF_UNIX;
    strncpy(addr.sun_path, SOCKET_PATH, sizeof(addr.sun_path) - 1);

    if (connect(client_fd, (struct sockaddr *)&addr, sizeof(addr)) == -1) {
        perror("client connect");
        exit(1);
    }

    const char *msg = "PING: Client requesting service";
    ssize_t ret = write(client_fd, msg, strlen(msg)); (void)ret;

    char buf[128];
    ssize_t n = read(client_fd, buf, sizeof(buf) - 1);
    if (n > 0) {
        buf[n] = '\0';
        printf("  [UDS Client] Received server response: '%s'\n", buf);
    }

    close(client_fd);
}

int main(void) {
    printf("[Main] Forking UNIX Domain Socket server and client...\n");
    pid_t pid = fork();
    if (pid == 0) {
        run_server();
        exit(0);
    } else {
        run_client();
        waitpid(pid, NULL, 0);
        printf("[Main] UNIX Domain Socket exchange completed.\n");
    }
    return 0;
}
