/*
 * 03_signal_catcher.c - Robust Signal Handling & Masking
 * Topics: sigaction, SA_SIGINFO, volatile sig_atomic_t, sigprocmask
 * Inspired by: TLPI Ch. 20-22
 */

#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <signal.h>
#include <string.h>
#include <time.h>

static volatile sig_atomic_t g_keep_running = 1;
static volatile sig_atomic_t g_signal_count = 0;

static void handle_signal(int sig, siginfo_t *info, void *ucontext) {
    (void)ucontext;
    g_signal_count++;

    /* Async-signal-safe I/O using write() directly */
    const char *msg = "Caught signal!\n";
    if (sig == SIGINT) {
        msg = "\n[Signal Handler] Intercepted SIGINT (Ctrl+C). Initiating graceful shutdown...\n";
    } else if (sig == SIGTERM) {
        msg = "\n[Signal Handler] Intercepted SIGTERM. Terminating loop...\n";
    }
    ssize_t ret = write(STDOUT_FILENO, msg, strlen(msg)); (void)ret;

    if (info) {
        /* Note: In production handlers, only call async-safe functions */
    }

    g_keep_running = 0;
}

int main(void) {
    printf("[Main] Process PID: %d. Setting up POSIX signal actions...\n", getpid());

    struct sigaction sa;
    memset(&sa, 0, sizeof(sa));
    sa.sa_sigaction = handle_signal;
    sa.sa_flags = SA_SIGINFO;
    sigemptyset(&sa.sa_mask);

    if (sigaction(SIGINT, &sa, NULL) == -1) {
        perror("sigaction SIGINT");
        return EXIT_FAILURE;
    }
    if (sigaction(SIGTERM, &sa, NULL) == -1) {
        perror("sigaction SIGTERM");
        return EXIT_FAILURE;
    }

    printf("[Main] Handlers attached. Simulating work loop (will auto-terminate after 3 ticks or on Ctrl+C)...\n");

    int ticks = 0;
    while (g_keep_running && ticks < 3) {
        printf("  Tick %d: process working...\n", ++ticks);
        sleep(1);
    }

    if (g_keep_running) {
        printf("[Main] Loop ended naturally without signals.\n");
    } else {
        printf("[Main] Graceful shutdown completed after receiving signal (total signals: %d).\n", g_signal_count);
    }

    return EXIT_SUCCESS;
}
