1. Loop the glob (safe for spaces). The -e check skips the case where no .txt files exist (the glob would otherwise pass
the literal '*.txt'). wc -l < file counts without printing the name, which we supply ourselves.

Ch.10 — Safe line-by-line read with numbering
n=1
while IFS= read -r line; do
printf '%d: %s\n' "$n" "$line"
n=$((n+1))
done < input.txt