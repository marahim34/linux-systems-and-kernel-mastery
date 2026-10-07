1. A leading /pattern/ restricts the s command to matching lines only. Here only lines beginning with 'Ike Deveron' and
containing 'phone' are edited, so 'Mike' (which does not start with 'Ike') is safe. Then the number pattern is replaced.

11.4 Delete matching lines
Remove every entry for Evelyn Jordan.
sed '/^Evelyn Jordan/d' names.txt

1. /pattern/d deletes lines matching the pattern. Anchoring with ^ ensures only lines that START with the name are
removed. This is the delete counterpart to substitution.

11.5 Swap two fields
Reformat 'First Last' into 'Last First'.
sed -E 's/^([A-Za-z]+)[[:space:]]+([A-Za-z]+)/\2 \1/' names.txt