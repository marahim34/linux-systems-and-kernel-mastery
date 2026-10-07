6. Replace every / with - in the value. These built-in manipulations avoid calling sed for simple jobs.

Command substitution and arithmetic





today=$(date +%F)
count=$(ls | wc -l)
total=$((5 + 3))
echo $((count * 2))