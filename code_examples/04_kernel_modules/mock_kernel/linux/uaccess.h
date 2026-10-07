#ifndef _MOCK_LINUX_UACCESS_H
#define _MOCK_LINUX_UACCESS_H

#include <string.h>

/* Mock user/kernel memory transfers */
static inline unsigned long copy_to_user(void *to, const void *from, unsigned long n) {
    if (!to || !from) return n;
    memcpy(to, from, n);
    return 0; /* 0 uncopied bytes = success */
}

static inline unsigned long copy_from_user(void *to, const void *from, unsigned long n) {
    if (!to || !from) return n;
    memcpy(to, from, n);
    return 0; /* 0 uncopied bytes = success */
}

#endif
