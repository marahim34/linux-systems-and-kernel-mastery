14. Worked Examples & Full Solutions
Complete answers to the practice exercises across both parts. Try each yourself first, then check your
reasoning here.

Part A — Configuration
Ch.3 — An alias needing a mid-argument (why it fails)
# This alias does NOT work as hoped:
alias backup='cp $1 $1.bak' # $1 is NOT substituted in aliases
# The fix is a function:
backup() { cp "$1" "$1.bak"; }