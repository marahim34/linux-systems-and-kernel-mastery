/*
 * 04_thread_pool.c - POSIX Multithreading & Work Queue Pool
 * Topics: pthread_create, pthread_join, pthread_mutex_t, pthread_cond_t
 * Inspired by: TLPI Ch. 29-33 & Operating System Theory
 */

#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <pthread.h>

#define NUM_WORKERS 4
#define QUEUE_CAPACITY 16

typedef struct {
    int task_id;
    int payload;
} Task;

typedef struct {
    Task queue[QUEUE_CAPACITY];
    int head;
    int tail;
    int count;
    int shutdown;
    pthread_mutex_t lock;
    pthread_cond_t not_empty;
    pthread_cond_t not_full;
} WorkPool;

static WorkPool g_pool;

void pool_init(WorkPool *p) {
    p->head = 0;
    p->tail = 0;
    p->count = 0;
    p->shutdown = 0;
    pthread_mutex_init(&p->lock, NULL);
    pthread_cond_init(&p->not_empty, NULL);
    pthread_cond_init(&p->not_full, NULL);
}

void pool_submit(WorkPool *p, Task t) {
    pthread_mutex_lock(&p->lock);
    while (p->count == QUEUE_CAPACITY && !p->shutdown) {
        pthread_cond_wait(&p->not_full, &p->lock);
    }
    if (p->shutdown) {
        pthread_mutex_unlock(&p->lock);
        return;
    }
    p->queue[p->tail] = t;
    p->tail = (p->tail + 1) % QUEUE_CAPACITY;
    p->count++;
    pthread_cond_signal(&p->not_empty);
    pthread_mutex_unlock(&p->lock);
}

void *worker_thread(void *arg) {
    long worker_id = (long)arg;
    while (1) {
        pthread_mutex_lock(&g_pool.lock);
        while (g_pool.count == 0 && !g_pool.shutdown) {
            pthread_cond_wait(&g_pool.not_empty, &g_pool.lock);
        }
        if (g_pool.shutdown && g_pool.count == 0) {
            pthread_mutex_unlock(&g_pool.lock);
            break;
        }

        Task t = g_pool.queue[g_pool.head];
        g_pool.head = (g_pool.head + 1) % QUEUE_CAPACITY;
        g_pool.count--;
        pthread_cond_signal(&g_pool.not_full);
        pthread_mutex_unlock(&g_pool.lock);

        /* Process task */
        printf("  [Worker %ld] Processing task %d (payload=%d, result=%d)\n",
               worker_id, t.task_id, t.payload, t.payload * t.payload);
        usleep(15000); /* 15ms simulated work */
    }
    return NULL;
}

int main(void) {
    printf("[Main] Initializing thread pool with %d worker threads...\n", NUM_WORKERS);
    pool_init(&g_pool);

    pthread_t threads[NUM_WORKERS];
    for (long i = 0; i < NUM_WORKERS; i++) {
        pthread_create(&threads[i], NULL, worker_thread, (void *)i);
    }

    printf("[Main] Submitting 8 compute tasks...\n");
    for (int i = 1; i <= 8; i++) {
        Task t = {.task_id = i, .payload = i * 10};
        pool_submit(&g_pool, t);
    }

    /* Wait a moment for workers to process then shutdown */
    usleep(150000);

    pthread_mutex_lock(&g_pool.lock);
    g_pool.shutdown = 1;
    pthread_cond_broadcast(&g_pool.not_empty);
    pthread_mutex_unlock(&g_pool.lock);

    for (int i = 0; i < NUM_WORKERS; i++) {
        pthread_join(threads[i], NULL);
    }

    pthread_mutex_destroy(&g_pool.lock);
    pthread_cond_destroy(&g_pool.not_empty);
    pthread_cond_destroy(&g_pool.not_full);

    printf("[Main] All workers joined cleanly. Thread pool destroyed successfully.\n");
    return EXIT_SUCCESS;
}
