/*
 * 01_copy_file.c - Low-level Robust File Copy using Direct Syscalls
 * Topics: open, read, write, close, errno, buffer chunking, permissions
 * Inspired by: The Linux Programming Interface (Michael Kerrisk) Ch. 4
 */

#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include <errno.h>
#include <string.h>

#define BUFFER_SIZE 4096

int main(int argc, char *argv[]) {
    if (argc != 3) {
        fprintf(stderr, "Usage: %s <source_file> <destination_file>\n", argv[0]);
        return EXIT_FAILURE;
    }

    const char *src_path = argv[1];
    const char *dst_path = argv[2];

    int src_fd = open(src_path, O_RDONLY);
    if (src_fd == -1) {
        fprintf(stderr, "Error opening source '%s': %s (errno=%d)\n",
                src_path, strerror(errno), errno);
        return EXIT_FAILURE;
    }

    /* Open destination: create if missing, truncate if exists, rw-r--r-- (0644) */
    int dst_fd = open(dst_path, O_WRONLY | O_CREAT | O_TRUNC, 0644);
    if (dst_fd == -1) {
        fprintf(stderr, "Error creating destination '%s': %s (errno=%d)\n",
                dst_path, strerror(errno), errno);
        close(src_fd);
        return EXIT_FAILURE;
    }

    char buffer[BUFFER_SIZE];
    ssize_t bytes_read;
    ssize_t total_copied = 0;

    while ((bytes_read = read(src_fd, buffer, sizeof(buffer))) > 0) {
        char *ptr = buffer;
        ssize_t bytes_left = bytes_read;

        /* Ensure entire buffer is written even in partial writes */
        while (bytes_left > 0) {
            ssize_t bytes_written = write(dst_fd, ptr, bytes_left);
            if (bytes_written <= 0) {
                if (bytes_written == -1 && errno == EINTR) {
                    continue; /* Interrupted by signal, retry */
                }
                fprintf(stderr, "Error writing data: %s\n", strerror(errno));
                close(src_fd);
                close(dst_fd);
                return EXIT_FAILURE;
            }
            bytes_left -= bytes_written;
            ptr += bytes_written;
        }
        total_copied += bytes_read;
    }

    if (bytes_read == -1) {
        fprintf(stderr, "Error reading source: %s\n", strerror(errno));
        close(src_fd);
        close(dst_fd);
        return EXIT_FAILURE;
    }

    close(src_fd);
    close(dst_fd);
    printf("Successfully copied %zd bytes from '%s' to '%s'.\n", total_copied, src_path, dst_path);
    return EXIT_SUCCESS;
}
