#ifndef _MOCK_LINUX_MODULE_H
#define _MOCK_LINUX_MODULE_H

#include "types.h"
#include <stdio.h>

#define MODULE_LICENSE(x)     static const char *__mod_license __attribute__((unused)) = x
#define MODULE_AUTHOR(x)      static const char *__mod_author __attribute__((unused)) = x
#define MODULE_DESCRIPTION(x) static const char *__mod_desc __attribute__((unused)) = x
#define MODULE_VERSION(x)     static const char *__mod_ver __attribute__((unused)) = x
#define MODULE_PARM_DESC(p,d) static const char *__mod_parm_##p __attribute__((unused)) = d

#define __init
#define __exit

#define printk(fmt, ...) printf("[dmesg] " fmt, ##__VA_ARGS__)
#define pr_info(fmt, ...) printf("[dmesg INFO] " fmt, ##__VA_ARGS__)
#define pr_err(fmt, ...)  printf("[dmesg ERR]  " fmt, ##__VA_ARGS__)
#define pr_warn(fmt, ...) printf("[dmesg WARN] " fmt, ##__VA_ARGS__)

typedef int (*module_init_t)(void);
typedef void (*module_exit_t)(void);

extern module_init_t __mock_init_fn;
extern module_exit_t __mock_exit_fn;

#define module_init(fn) module_init_t __mock_init_fn = fn
#define module_exit(fn) module_exit_t __mock_exit_fn = fn
#define module_param(name, type, perm) /* mock param */

#endif
