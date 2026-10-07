1. The monitor wraps the data...
2. ...and its operations. The runtime ensures only one thread is inside ANY of these procedures at once, so balance can
never be corrupted by a race. The programmer cannot forget to lock, because locking is the construct itself.

Condition variables
Sometimes a thread inside a monitor must WAIT for a condition (a consumer waiting for the buffer to be
non-empty). Condition variables provide wait (release the monitor and sleep until signalled) and signal
(wake a waiting thread). They let threads coordinate on events, not just guard data.

Message passing — sharing nothing
A completely different philosophy: instead of sharing memory and protecting it, share nothing and
communicate by sending messages. Two processes exchange data through send and receive
operations. There is no shared state to race over. This is how separate machines cooperate (there is no
shared memory across a network), and the model behind Go's channels and the actor model.
Approach

Philosophy

Real examples

Shared memory + locks

Share data, protect access

Threads, mutexes, monitors

Message passing

Share nothing, send copies

Pipes, sockets, Go channels, actors





PRO INSIGHT: A famous principle from the Go language captures the shift: 'Do not communicate by sharing
memory; instead, share memory by communicating.' Message passing trades the raw speed of shared memory for
safety and scalability — no locks to forget, and it works across machines. Understanding both models, and when
each fits, is what separates a coder from a systems engineer.

mkfifo /tmp/mypipe
echo "hello" > /tmp/mypipe &
cat /tmp/mypipe