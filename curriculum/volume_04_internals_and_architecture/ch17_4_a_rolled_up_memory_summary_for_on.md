4. A rolled-up memory summary for one process — real physical memory it occupies.

PRO INSIGHT: Unique point: Linux treats free RAM as WASTED RAM. Spare memory is filled with disk cache to
speed everything up, and instantly released when a program needs it. This is why new users panic at 'only 200MB
free' — they are reading the wrong number. The 'available' figure is what matters. This aggressive caching is a big
reason Linux file operations feel fast.

The out-of-memory killer
If RAM and swap are both exhausted and a process still demands more, the kernel must act or the whole
system freezes. It invokes the OOM killer, which selects and terminates the process judged 'least valuable
but most memory-hungry' to save the system. This is the 3 AM 'my backend mysteriously died' from Volume
1 — now you know the exact mechanism, and why swap and MemoryMax limits tame it.