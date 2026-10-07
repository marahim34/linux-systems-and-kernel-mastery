#ifndef _MOCK_LINUX_TYPES_H
#define _MOCK_LINUX_TYPES_H

#include <stddef.h>
#include <stdint.h>
#include <stdbool.h>
#include <sys/types.h>

#define __user

typedef int64_t  loff_t;
typedef uint32_t gfp_t;

#define GFP_KERNEL 0
#define GFP_ATOMIC 1

#endif
