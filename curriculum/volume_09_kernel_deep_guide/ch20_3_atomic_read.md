3. Atomic read.
4. dec_and_test atomically decrements AND tells you if it hit zero — the classic reference-counting primitive.
5. cmpxchg: set to new ONLY if it currently equals old, atomically — the building block of all lock-free algorithms.

Memory barriers — enforcing order
Barrier

Guarantees

Use

smp_mb()

Full barrier: all prior loads/stores
before later

General ordering

smp_wmb()

Write barrier: prior stores before later
stores

Publishing data then a flag

smp_rmb()

Read barrier: prior loads before later
loads

Reading a flag then the data

READ_ONCE / WRITE_ONCE

Prevents compiler tearing/reordering
one access

Any shared-variable access without a
lock

smp_load_acquire / store_release

Acquire/release ordering (like
C++11)

The modern, preferred pairing





/* Producer publishes data, THEN sets ready flag: */
obj->data = 42;
smp_wmb(); /* ensure data write lands first */
WRITE_ONCE(obj->ready, 1);
/* Consumer sees flag, THEN reads data: */
if (READ_ONCE(obj->ready)) {
smp_rmb(); /* ensure we read data AFTER seeing flag */
use(obj->data);
}