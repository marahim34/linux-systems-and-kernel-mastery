4. The writer copies, modifies the copy (Read-COPY-Update)...
5. rcu_assign_pointer atomically publishes the new version — new readers see it, old readers still use the old.
6. synchronize_rcu blocks until every reader that MIGHT hold the old pointer has finished...
7. ...only THEN is it safe to free the old version. No reader ever sees freed memory, with no reader-side locking.

PRO INSIGHT: RCU is the single most distinctive and powerful concurrency mechanism in Linux, and
understanding it marks a serious kernel developer. The mental model: readers are free and never block; the cost is
moved entirely to writers, who must wait out a grace period before reclaiming old data. It fits read-mostly data
perfectly — which describes much of the kernel. It is subtle: readers must not sleep (in classic RCU), and you must
use rcu_dereference/rcu_assign_pointer for the ordering. But mastered, it is how Linux achieves its legendary
multi-core scalability.

Deadlock avoidance, enforced
Volume 5's lock-ordering rule is enforced here by lockdep, the runtime dependency validator. Enable
CONFIG_PROVE_LOCKING in your development kernel and it tracks every lock acquisition order,
screaming the moment two code paths could form a cycle — catching deadlocks that might otherwise appear
only once a year in production. No serious kernel work is done without lockdep on in testing.
PRACTICE EXERCISES