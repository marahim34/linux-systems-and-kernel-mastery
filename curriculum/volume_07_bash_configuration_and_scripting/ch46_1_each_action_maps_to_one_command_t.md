1. Each action maps to one command; the * default prints usage to stderr and exits with failure. This is the exact shape
of real service-control scripts.

Ch.10 — Files with line counts
for f in *.txt; do
[[ -e "$f" ]] || continue
printf '%s: %s lines\n' "$f" "$(wc -l < "$f")"
done