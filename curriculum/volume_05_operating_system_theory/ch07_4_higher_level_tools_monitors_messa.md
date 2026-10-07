4. Higher-Level Tools — Monitors & Message
Passing
Why semaphores are not enough
Semaphores work, but they are error-prone: forget one up, or order two down operations wrongly, and you
get a deadlock or a race that is nearly impossible to find. The operations are scattered through the code with
nothing tying them together. Higher-level constructs package the discipline so the compiler or runtime helps
you get it right.

Monitors
A monitor bundles shared data together with the procedures that operate on it, and guarantees that only
one thread executes inside the monitor at a time — the mutual exclusion is automatic, built into the
construct. You do not write lock/unlock; entering any monitor procedure locks it, leaving unlocks it. Java's
synchronized keyword and Python's with lock: are monitors in practice.
# conceptual monitor
monitor BankAccount {
balance = 0
procedure deposit(n) { balance = balance + n } # auto-exclusive
procedure withdraw(n){ balance = balance - n } # auto-exclusive
}