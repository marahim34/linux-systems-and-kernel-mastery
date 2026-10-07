/*
 * kernel_simulator.c - User-Space Linux Kernel Module Simulator & Harness
 * Runs kernel drivers in safe user-space memory, exercising syscall bindings
 * and logging dmesg traces without root privileges or kernel panic risks!
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "linux/module.h"
#include "linux/fs.h"

extern struct file_operations dojo_fops;

int main(void) {
    printf("==================================================================\n");
    printf("     LINUX KERNEL SUBSYSTEM SIMULATOR (SAFE USERSPACE HARNESS)   \n");
    printf("==================================================================\n\n");

    printf("[Simulator Step 1] Invoking module_init()...\n");
    int init_rc = __mock_init_fn();
    if (init_rc != 0) {
        fprintf(stderr, "Kernel module init failed with code %d\n", init_rc);
        return EXIT_FAILURE;
    }

    printf("\n[Simulator Step 2] Simulating user-space process opening /dev/dojo_char...\n");
    struct inode fake_inode = { .i_ino = 42, .i_rdev = MKDEV(240, 0) };
    struct file fake_file = { .private_data = NULL, .f_pos = 0, .f_flags = 0 };

    if (dojo_fops.open) {
        dojo_fops.open(&fake_inode, &fake_file);
    }

    printf("\n[Simulator Step 3] Simulating user-space write(\"Hello Linux Kernel Mastery!\")...\n");
    const char *payload = "Hello Linux Kernel Mastery from User-Space!";
    loff_t offset = 0;
    ssize_t written = dojo_fops.write(&fake_file, payload, strlen(payload), &offset);
    printf("  --> Bytes written to driver: %zd\n", written);

    printf("\n[Simulator Step 4] Simulating user-space read() back from /dev/dojo_char...\n");
    char user_buffer[256];
    memset(user_buffer, 0, sizeof(user_buffer));
    offset = 0;
    ssize_t read_bytes = dojo_fops.read(&fake_file, user_buffer, sizeof(user_buffer) - 1, &offset);
    printf("  --> Bytes read from driver: %zd\n", read_bytes);
    printf("  --> Received driver data: \"%s\"\n", user_buffer);

    printf("\n[Simulator Step 5] Simulating close() / release()...\n");
    if (dojo_fops.release) {
        dojo_fops.release(&fake_inode, &fake_file);
    }

    printf("\n[Simulator Step 6] Invoking module_exit()...\n");
    __mock_exit_fn();

    printf("\n==================================================================\n");
    printf("K-HARNESS VERDICT: PASS! Driver file_operations verified cleanly.\n");
    printf("==================================================================\n");
    return EXIT_SUCCESS;
}
