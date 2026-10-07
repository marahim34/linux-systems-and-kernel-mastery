6. Use is_running as a condition — functions returning 0/non-zero work directly in if.

PRO INSIGHT: Exit codes are how the whole shell communicates success and failure: 0 means success, any other
number means failure. $? holds the last command's code. This is why if command works — it tests whether the
command exited 0. Your functions should follow the same convention: return 0 for success. This single convention
underlies all shell automation, error handling, and the && / || operators.
PRACTICE EXERCISES