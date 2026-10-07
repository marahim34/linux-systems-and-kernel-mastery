#ifndef _MOCK_LINUX_SLAB_H
#define _MOCK_LINUX_SLAB_H

#include "types.h"
#include <stdlib.h>
#include <string.h>

static inline void *kmalloc(size_t size, gfp_t flags) {
    (void)flags;
    return malloc(size);
}

static inline void *kzalloc(size_t size, gfp_t flags) {
    (void)flags;
    return calloc(1, size);
}

static inline void kfree(const void *ptr) {
    free((void *)ptr);
}

#endif
