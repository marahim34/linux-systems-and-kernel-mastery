14. Exercises with Full Solutions
Answers to the key exercises across the volume. Build and test each in your VM.

Ch.4 — Observing a tainted kernel
/* Remove this line, rebuild, load: */
/* MODULE_LICENSE("GPL"); */
/* dmesg shows: */
/* module verification failed: signature and/or */
/* required key missing - tainting kernel */