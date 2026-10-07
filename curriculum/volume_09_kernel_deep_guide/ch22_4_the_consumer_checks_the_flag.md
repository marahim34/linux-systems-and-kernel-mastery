4. The consumer checks the flag...
5. ...a READ barrier ensures it reads the payload AFTER observing the flag...
6. ...so the data it uses is the published value. This paired barrier pattern is the essence of lock-free publication.

PRO INSIGHT: If you have done C++11 std::atomic with memory_order_acquire/release, this will feel familiar —
the kernel's smp_load_acquire/smp_store_release are the same concept, and the preferred modern style. The
crucial warning: lock-free code without correct barriers is WRONG even when it passes every test on your machine,
because reordering is timing- and architecture-dependent (x86 is forgiving; ARM is not). Never write lock-free kernel
code by intuition. Use established patterns, use acquire/release, and when in doubt, use a lock — correctness first.