# Top-level Makefile for Kernel Modules
# Supports both:
#   1. Safe user-space simulation harness (default, no root needed)
#   2. Real kernel module compilation (requires kernel headers)

KDIR ?= /lib/modules/$(shell uname -r)/build
PWD := $(shell pwd)

all: simulator-all

simulator-all:
	@echo "=== Building Kernel Modules in Safe User-Space Simulator ==="
	gcc -Wall -Wextra -pthread -DMOCK_KERNEL -I$(PWD)/mock_kernel \
		$(PWD)/02_char_device/char_dev.c \
		$(PWD)/mock_kernel/kernel_simulator.c \
		-o $(PWD)/mock_kernel/kernel_simulator
	@echo "Kernel simulator built successfully at mock_kernel/kernel_simulator"

test: simulator-all
	@echo "=== Running Kernel Subsystem Simulator Test ==="
	$(PWD)/mock_kernel/kernel_simulator

clean:
	rm -f $(PWD)/mock_kernel/kernel_simulator
	rm -f *.o *.ko *.mod.c *.order *.symvers
