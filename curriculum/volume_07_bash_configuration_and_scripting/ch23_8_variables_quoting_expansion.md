8. Variables, Quoting & Expansion
The quoting rules that prevent 80% of bugs
name="Abdur Rahim"
echo "$name"
echo '$name'
echo $name
files="my file.txt"
rm "$files"
rm $files