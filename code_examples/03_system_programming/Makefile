# Makefile for Linux System Programming Examples
# Compiler flags: strict warnings, pthread, C11 standard, optimization

CC ?= gcc
CFLAGS ?= -Wall -Wextra -pthread -std=gnu11 -O2 -g

TARGETS = 01_copy_file \
          02_process_tree \
          03_signal_catcher \
          04_thread_pool \
          05_pipe_ipc \
          06_shm_posix \
          07_unix_domain_socket \
          08_tcp_epoll_server \
          09_mmap_file_indexer

all: $(TARGETS)

01_copy_file: 01_copy_file.c
	$(CC) $(CFLAGS) $< -o $@

02_process_tree: 02_process_tree.c
	$(CC) $(CFLAGS) $< -o $@

03_signal_catcher: 03_signal_catcher.c
	$(CC) $(CFLAGS) $< -o $@

04_thread_pool: 04_thread_pool.c
	$(CC) $(CFLAGS) $< -o $@

05_pipe_ipc: 05_pipe_ipc.c
	$(CC) $(CFLAGS) $< -o $@

06_shm_posix: 06_shm_posix.c
	$(CC) $(CFLAGS) $< -o $@ -lrt

07_unix_domain_socket: 07_unix_domain_socket.c
	$(CC) $(CFLAGS) $< -o $@

08_tcp_epoll_server: 08_tcp_epoll_server.c
	$(CC) $(CFLAGS) $< -o $@

09_mmap_file_indexer: 09_mmap_file_indexer.c
	$(CC) $(CFLAGS) $< -o $@

clean:
	rm -f $(TARGETS)

test: all
	@echo "=== Testing System Programming Binaries ==="
	./02_process_tree
	./04_thread_pool
	./05_pipe_ipc
	./06_shm_posix
	./07_unix_domain_socket
	./08_tcp_epoll_server 19099 --once
	./09_mmap_file_indexer ../../practice_data/employees.csv
	@echo "All system programming tests passed successfully!"
