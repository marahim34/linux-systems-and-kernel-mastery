10. Loops
for — iterate over a list
for name in Abdur Sara Ali; do
echo "Hello $name"
done
for f in *.log; do
gzip "$f"
done
for i in {1..5}; do
echo "Attempt $i"
done