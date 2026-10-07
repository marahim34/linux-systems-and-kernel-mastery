8. The only top-level statement: run main with the original arguments. This skeleton scales from 10 lines to 1000.

Variables and quoting — where 80% of bugs live
name="Abdur Rahim"
echo "Hello, $name"
echo 'Hello, $name'
file_count=$(ls | wc -l)
echo "There are ${file_count} files"
default="${1:-/tmp}"
: "${API_KEY:?API_KEY must be set}"