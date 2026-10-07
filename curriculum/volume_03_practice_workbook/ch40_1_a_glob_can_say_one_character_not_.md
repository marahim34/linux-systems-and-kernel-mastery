1. A glob can say 'one character not in this set' at a fixed position, but it cannot scan a whole variable-length name for
ANY disallowed character. grep with a negated class and -E does that across the entire name.





Section 4 — Redirection
4a. Predict and verify 4.3 and 4.6
echo 2 2>2 ; ls -l 2 ; cat 2 # file '2' exists but empty
: > ls ; ls < ls > ls ; cat ls # listing went into file 'ls'