2. Loop over files matching a glob — compress each .log. Quote "$f" for safety.
3. {1..5} generates 1 2 3 4 5 — a numeric range loop.

while — loop until a condition changes
count=1
while [[ $count -le 3 ]]; do
echo "Count is $count"
count=$((count + 1))
done
while IFS= read -r line; do
echo "Line: $line"
done < input.txt

1. while repeats as long as the test is true.