/*
 * 02_process_tree.c - Process Lifecycle Management
 * Topics: fork, execve, waitpid, process status evaluation (WIFEXITED, WEXITSTATUS)
 * Inspired by: TLPI Ch. 24-26 & Advanced Linux Programming Ch. 3
 */

#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <errno.h>
#include <string.h>

int main(void) {
    pid_t parent_pid = getpid();
    printf("[Parent] Initialized master process: PID=%d, Parent PPID=%d\n", parent_pid, getppid());

    pid_t child_pid = fork();

    if (child_pid < 0) {
        perror("fork failed");
        return EXIT_FAILURE;
    }

    if (child_pid == 0) {
        /* Child Process */
        printf("[Child] Running inside child process! PID=%d, Parent PID=%d\n", getpid(), getppid());
        printf("[Child] Executing 'uname -a' via execvp...\n");

        char *args[] = {"uname", "-a", NULL};
        execvp(args[0], args);

        /* execvp only returns if error occurred */
        perror("execvp failed");
        exit(127);
    } else {
        /* Parent Process */
        printf("[Parent] Spawned child with PID=%d. Waiting for termination...\n", child_pid);

        int status;
        pid_t waited_pid = waitpid(child_pid, &status, 0);

        if (waited_pid == -1) {
            perror("waitpid failed");
            return EXIT_FAILURE;
        }

        if (WIFEXITED(status)) {
            printf("[Parent] Child PID=%d exited normally with exit code=%d.\n",
                   waited_pid, WEXITSTATUS(status));
        } else if (WIFSIGNALED(status)) {
            printf("[Parent] Child PID=%d killed by signal=%d.\n",
                   waited_pid, WTERMSIG(status));
        }
    }

    return EXIT_SUCCESS;
}
