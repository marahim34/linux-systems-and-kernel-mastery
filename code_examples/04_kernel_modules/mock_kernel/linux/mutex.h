#ifndef _MOCK_LINUX_MUTEX_H
#define _MOCK_LINUX_MUTEX_H

#include <pthread.h>

struct mutex {
    pthread_mutex_t lock;
};

#define DEFINE_MUTEX(m) struct mutex m = { .lock = PTHREAD_MUTEX_INITIALIZER }

static inline void mutex_init(struct mutex *lock) {
    pthread_mutex_init(&lock->lock, NULL);
}

static inline void mutex_lock(struct mutex *lock) {
    pthread_mutex_lock(&lock->lock);
}

static inline void mutex_unlock(struct mutex *lock) {
    pthread_mutex_unlock(&lock->lock);
}

static inline void mutex_destroy(struct mutex *lock) {
    pthread_mutex_destroy(&lock->lock);
}

#endif
