3. Remove it again. This modularity is how one kernel supports thousands of devices without being one giant fixed blob.

PRO INSIGHT: Unique point: Linux gets the performance of a monolithic kernel AND much of the flexibility of a
microkernel, through modules. Windows and macOS kernels are hybrids that made different trade-offs. Linux's
choice — fast core, hot-swappable drivers — is a big reason it dominates servers, where you load exactly the
drivers you need and nothing more.