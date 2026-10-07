2. How many threads a given process currently has, straight from its kernel record.
3. top in thread mode (-H) shows individual threads and their CPU use — see a multithreaded program spread across
cores.

PRO INSIGHT: Linux detail worth knowing: to the Linux kernel a thread and a process are almost the same thing —
both are 'tasks' created by clone(). A process is just a task with its own memory; a thread is a task that SHARES
memory with its creator. This unified model (unusual among operating systems) is why Linux threading is efficient
and why fork and thread-creation share machinery. It is a recurring Linux theme: one clean mechanism instead of
two special cases.
PRACTICE EXERCISES