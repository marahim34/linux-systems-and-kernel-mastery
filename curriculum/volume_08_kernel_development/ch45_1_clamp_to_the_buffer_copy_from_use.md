1. Clamp to the buffer, copy_from_user safely, null-terminate before treating as a string, log it, and return len so the
writing program believes all its bytes were accepted. Returning fewer would make it retry. Note the mandatory
copy_from_user, never a raw dereference.

Ch.8 — Correct allocation with error path
buffer = kzalloc(BUF_SIZE, GFP_KERNEL);
if (!buffer)
return -ENOMEM;
/* ...later, always: */
kfree(buffer);

1. kzalloc gives zeroed memory; the NULL check is mandatory because kernel allocations fail for real. Every allocation
is paired with a kfree on every exit path — the discipline that prevents permanent kernel memory leaks.

Ch.9 — Choosing the right lock