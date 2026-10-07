/*
 * 05_pipe_ipc.c - Inter-Process Communication via Anonymous Pipes
 * Topics: pipe, fork, dup2, stdin/stdout redirection, stream processing
 * Inspired by: TLPI Ch. 44 & William Shotts "The Linux Command Line"
 */

#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <string.h>

int main(void) {
    int pipefd[2];
    if (pipe(pipefd) == -1) {
        perror("pipe failed");
        return EXIT_FAILURE;
    }

    pid_t pid = fork();
    if (pid < 0) {
        perror("fork failed");
        return EXIT_FAILURE;
    }

    if (pid == 0) {
        /* Child: Consumer reads from pipe */
        close(pipefd[1]); /* Close unused write end */

        char buf[256];
        ssize_t bytes = read(pipefd[0], buf, sizeof(buf) - 1);
        if (bytes > 0) {
            buf[bytes] = '\0';
            printf("[Child PID=%d] Received message through pipe:\n  ==> '%s'\n", getpid(), buf);
        }
        close(pipefd[0]);
        exit(EXIT_SUCCESS);
    } else {
        /* Parent: Producer writes to pipe */
        close(pipefd[0]); /* Close unused read end */

        const char *msg = "Kernel & System Programming Mastery - Tampere 2026";
        printf("[Parent PID=%d] Sending payload into pipe...\n", getpid());
        ssize_t ret = write(pipefd[1], msg, strlen(msg)); (void)ret;
        close(pipefd[1]); /* Send EOF to reader */

        waitpid(pid, NULL, 0);
        printf("[Parent] Child finished. Pipe IPC demonstration succeeded.\n");
    }

    return EXIT_SUCCESS;
}
