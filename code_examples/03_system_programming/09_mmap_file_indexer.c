/*
 * 09_mmap_file_indexer.c - Zero-Copy Memory-Mapped File Processing
 * Topics: mmap, munmap, fstat, PROT_READ, MAP_PRIVATE, pointer arithmetic
 * Inspired by: TLPI Ch. 49 & Bovet "Understanding the Linux Kernel" Memory chapter
 */

#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <errno.h>

int main(int argc, char *argv[]) {
    const char *filepath = (argc > 1) ? argv[1] : "practice_data/employees.csv";

    int fd = open(filepath, O_RDONLY);
    if (fd == -1) {
        perror("open failed");
        return EXIT_FAILURE;
    }

    struct stat sb;
    if (fstat(fd, &sb) == -1) {
        perror("fstat failed");
        close(fd);
        return EXIT_FAILURE;
    }

    if (sb.st_size == 0) {
        printf("File is empty (0 bytes).\n");
        close(fd);
        return EXIT_SUCCESS;
    }

    /* Map entire file directly into process address space */
    char *addr = (char *)mmap(NULL, sb.st_size, PROT_READ, MAP_PRIVATE, fd, 0);
    if (addr == MAP_FAILED) {
        perror("mmap failed");
        close(fd);
        return EXIT_FAILURE;
    }

    /* Process mapped memory without userspace buffer copying (zero-copy) */
    size_t line_count = 0;
    size_t char_count = sb.st_size;

    for (off_t i = 0; i < sb.st_size; i++) {
        if (addr[i] == '\n') {
            line_count++;
        }
    }

    printf("[mmap Indexer] File: '%s'\n", filepath);
    printf("  Size       : %zd bytes\n", char_count);
    printf("  Line count : %zu lines\n", line_count);
    printf("  First 40 bytes: \"%.*s...\"\n", (int)(sb.st_size < 40 ? sb.st_size : 40), addr);

    if (munmap(addr, sb.st_size) == -1) {
        perror("munmap failed");
    }

    close(fd);
    return EXIT_SUCCESS;
}
