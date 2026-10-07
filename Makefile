# Top-level Makefile for Linux Mastery Platform
# Controls compilation, test suites, kernel simulator, and web server

.PHONY: all clean test web status run-kernel

PYTHON ?= python3

all:
	@echo "=== Building C System Programming Examples ==="
	$(MAKE) -C code_examples/03_system_programming all
	@echo "=== Building Kernel Subsystem Simulator ==="
	$(MAKE) -C code_examples/04_kernel_modules all
	@echo "Build complete!"

clean:
	$(MAKE) -C code_examples/03_system_programming clean
	$(MAKE) -C code_examples/04_kernel_modules clean

test: all
	@echo "=== Running Full Unit & Integration Test Suite ==="
	$(PYTHON) -m unittest discover -s tests -p "test_*.py"
	@echo "=== Running 50 Graded Text Processing Exercises ==="
	./code_examples/02_text_processing/50_grep_sed_awk_solutions.sh > /dev/null
	@echo "=== All platform tests and solutions verified successfully! ==="

web:
	./linux-mastery web --port 8080

status:
	./linux-mastery status

run-kernel:
	$(MAKE) -C code_examples/04_kernel_modules test
