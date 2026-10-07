# Tier 1 · Chapter 6: The Text-Processing Trio (Grep, Sed, Awk)

Synthesized from *Grep, Sed & Awk Mastery Complete*.

## 1. Division of Labor
- **grep**: *Search & Filter* - Finds lines matching regular expressions.
- **sed**: *Stream Editor* - Modifies, replaces, and transforms text line-by-line.
- **awk**: *Field & Report Processor* - Complete programming language for columnar data and math.

## 2. Real-World Cheatsheets
### Grep
```bash
grep -i PATTERN file    # Case-insensitive
grep -v PATTERN file    # Invert match
grep -c PATTERN file    # Count matching lines
grep -n PATTERN file    # Line numbers
grep -oE '^[0-9.]+' log # Extract matching segment
grep -C 2 PATTERN file  # Context lines
```

### Sed
```bash
sed 's/old/new/g' file             # Replace all
sed -i.bak 's/8080/9090/' conf     # In-place with backup
sed '/^#/d; /^$/d' conf            # Strip comments & blanks
sed -n '5,10p' file                # Line range
sed -E 's/port ([0-9]+)/\1 is port/' conf # Backreferences
```

### Awk
```bash
awk '{print $1, $9}' access.log                 # Columns
awk -F: '{print $1, $6}' /etc/passwd            # Custom delimiter
awk '$9 == 500 {print $1}' access.log           # Conditions
awk '{sum += $10} END {print sum}' access.log   # Sum
awk '{c[$1]++} END {for (i in c) print c[i], i}' log | sort -rn # Group-by count
```
