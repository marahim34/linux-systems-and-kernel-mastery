4. This makes your device a first-class citizen in any event-driven program.

PRO INSIGHT: The difference between a toy driver and a real one is these behaviours: it must handle multiple
concurrent openers safely (locking around shared state), let readers block efficiently rather than busy-wait (wait
queues), respect signals (ERESTARTSYS), and support poll for event loops. Each is a well-established pattern. A
char driver with correct blocking I/O, signal handling, poll support, and driver-model integration is genuinely
production-grade — and demonstrates you understand the kernel's I/O contract, not just its syntax.