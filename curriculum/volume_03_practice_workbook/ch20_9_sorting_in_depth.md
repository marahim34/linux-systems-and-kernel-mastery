9. Sorting in Depth
A shared data file helps here: lines like 'Lastname, Firstname area-local' with fields separated by commas,
spaces and hyphens.

9.1 Reverse by last name
Sort by the first field (before the comma), descending.
sort -t"," -k1,1 -r data.txt

1. -t sets the field separator to a comma; -k1,1 sorts by field 1 only (from key 1 to key 1); -r reverses to descending
order. Limiting the key with 1,1 stops sort from using the rest of the line as a tiebreaker in unexpected ways.

9.2 By whole phone number
Sort by the third whitespace field.
sort -k3,3 data.txt