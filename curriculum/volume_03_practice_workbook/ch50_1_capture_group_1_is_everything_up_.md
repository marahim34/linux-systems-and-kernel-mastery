1. Capture group 1 is everything up to the first comma, group 2 the next field; the replacement prints them swapped.
[^,]+ means 'one or more non-comma characters'.

Section 12 — find
12a. Files over 1 MB, listed
find ~ -type f -size +1M -exec ls -lh {} +

1. -size +1M finds files larger than a megabyte; -exec ls -lh {} + lists them with human-readable sizes, batching many
files into each ls call for speed.

12b. Files changed in the last day, counted
find ~ -type f -mtime -1 | wc -l

1. -mtime -1 means modified within the last 24 hours; piping to wc -l counts them.





12c. Combine name and size
find ~ -type f -name "*.log" -size +10k