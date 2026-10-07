6. Unquoted: rm sees TWO arguments 'my' and 'file.txt' — deletes the wrong things. The classic space-in-filename
disaster.

PRO INSIGHT: The single most important bash rule: ALWAYS quote your variables — "$var", not $var. Unquoted
variables break on spaces and are the number-one source of bash bugs, from failed scripts to accidental deletions.
The only time you leave a variable unquoted is when you deliberately WANT word-splitting, which is rare. When in
doubt, add the quotes.

Parameter expansion — defaults and manipulation
echo "${name:-Guest}"
echo "${count:=0}"
echo "${file%.txt}"
echo "${file##*/}"
echo "${#name}"
echo "${path//\//-}"