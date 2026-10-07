1. A practical email validator: start, allowed name characters (one or more), @, domain letters, a literal dot, a 2+ letter
TLD, end. Read regex left to right like a sentence and it stops being scary.

sed — complete treatment
sed reads line by line, applies your instruction, prints the result. Its core instruction is s/find/replace/flags —
but it can also delete, insert, and slice.
sed 's/localhost/127.0.0.1/' app.conf
sed 's/old/new/g' file.txt
sed -i.bak 's/DEBUG = True/DEBUG = False/' settings.py
sed -n '/server {/,/}/p' nginx.conf
sed '/^$/d' data.txt
sed '3i\# inserted comment' script.sh
sed 's|/opt/old|/opt/new|g' paths.txt