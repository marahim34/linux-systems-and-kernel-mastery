4. The professional version — split into DNS, TCP connect, and time-to-first-byte: the slow phase names the guilty layer
(DNS server / network path / the application itself).

PRACTICE EXERCISES
1. strace a program with a deliberately missing config; find the exact failing openat and the paths it searched.