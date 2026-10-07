/*
 * 06_shm_posix.c - POSIX Shared Memory and Synchronization
 * Topics: shm_open, ftruncate, mmap, munmap, shm_unlink, sem_open, sem_wait, sem_post
 * Inspired by: TLPI Ch. 53-54
 */

#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <sys/wait.h>
#include <semaphore.h>
#include <string.h>

#define SHM_NAME "/dojo_shm_demo"
#define SEM_MUTEX "/dojo_sem_mutex"
#define SHM_SIZE 1024

typedef struct {
    int counter;
    char last_updater[64];
} SharedData;

int main(void) {
    /* Create shared memory segment */
    int shm_fd = shm_open(SHM_NAME, O_CREAT | O_RDWR, 0666);
    if (shm_fd == -1) {
        perror("shm_open");
        return EXIT_FAILURE;
    }

    if (ftruncate(shm_fd, sizeof(SharedData)) == -1) {
        perror("ftruncate");
        shm_unlink(SHM_NAME);
        return EXIT_FAILURE;
    }

    SharedData *data = (SharedData *)mmap(NULL, sizeof(SharedData),
                                          PROT_READ | PROT_WRITE,
                                          MAP_SHARED, shm_fd, 0);
    if (data == MAP_FAILED) {
        perror("mmap");
        shm_unlink(SHM_NAME);
        return EXIT_FAILURE;
    }

    /* Create named semaphore */
    sem_unlink(SEM_MUTEX);
    sem_t *sem = sem_open(SEM_MUTEX, O_CREAT | O_EXCL, 0666, 1);
    if (sem == SEM_FAILED) {
        perror("sem_open");
        munmap(data, sizeof(SharedData));
        shm_unlink(SHM_NAME);
        return EXIT_FAILURE;
    }

    data->counter = 0;
    snprintf(data->last_updater, sizeof(data->last_updater), "initial");

    pid_t pid = fork();
    if (pid == 0) {
        /* Child updates shared memory 100 times */
        for (int i = 0; i < 50; i++) {
            sem_wait(sem);
            data->counter++;
            snprintf(data->last_updater, sizeof(data->last_updater), "child");
            sem_post(sem);
            usleep(500);
        }
        munmap(data, sizeof(SharedData));
        sem_close(sem);
        exit(EXIT_SUCCESS);
    } else {
        /* Parent also updates shared memory 100 times concurrently */
        for (int i = 0; i < 50; i++) {
            sem_wait(sem);
            data->counter++;
            snprintf(data->last_updater, sizeof(data->last_updater), "parent");
            sem_post(sem);
            usleep(500);
        }

        waitpid(pid, NULL, 0);

        printf("[POSIX SHM] Expected counter: 100, Actual counter: %d (Last updater: %s)\n",
               data->counter, data->last_updater);

        /* Cleanup */
        munmap(data, sizeof(SharedData));
        close(shm_fd);
        shm_unlink(SHM_NAME);
        sem_close(sem);
        sem_unlink(SEM_MUTEX);
    }

    return EXIT_SUCCESS;
}
