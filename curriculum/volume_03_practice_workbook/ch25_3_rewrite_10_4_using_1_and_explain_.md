3. Rewrite 10.4 using {1} and explain why [56] and (5|6) are equivalent here.





11. sed — Stream Editing
11.1 Collapse extra spaces
Make every run of spaces a single space and trim trailing ones.
sed -E 's/[[:space:]]+/ /g; s/[[:space:]]+$//' names.txt