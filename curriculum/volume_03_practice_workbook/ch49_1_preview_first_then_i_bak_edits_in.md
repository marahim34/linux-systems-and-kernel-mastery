1. Preview first, then -i.bak edits in place while saving a backup. diff confirms exactly what changed.

11b. Delete blank lines
sed '/^$/d' file

1. ^$ matches a line that starts and immediately ends (empty); d deletes it. Add -i to modify the file.

11c. Swap two comma fields
sed -E 's/^([^,]+),([^,]+)/\2,\1/' data.csv