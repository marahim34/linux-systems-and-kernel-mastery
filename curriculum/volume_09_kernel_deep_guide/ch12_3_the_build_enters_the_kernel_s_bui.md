3. The build enters the KERNEL's build system (-C) and points it back at your code (M=$(PWD)) — Kbuild does the
actual work.
4. modules_install copies the .ko into /lib/modules so modprobe can find it. Out-of-tree is how you develop; in-tree
(Chapters above) is how you upstream.





PRO INSIGHT: The build-system distinction that matters: OUT-OF-TREE (obj-m in your own directory) is for
development and third-party drivers — fast iteration, no kernel source needed beyond headers. IN-TREE
(obj-$(CONFIG_x) inside the kernel source with a Kconfig entry) is for code you intend to UPSTREAM. Start
out-of-tree to build and test, then convert to in-tree with proper Kconfig when you are ready to contribute. Knowing
both, and when to use each, marks the transition from hobbyist to contributor.