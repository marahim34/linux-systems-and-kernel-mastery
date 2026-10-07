9. Conditionals & Tests
if and the test brackets
if [[ -f "config.yaml" ]]; then
echo "Config exists"
elif [[ -d "config/" ]]; then
echo "Config directory exists"
else
echo "No config found"
fi

1. [[ ]] is bash's test construct; -f asks 'is this a regular file?'. Always use double brackets in bash — safer than single [ ].
2. elif chains another test; -d asks 'is this a directory?'.
3. else for the fallback.
4. fi closes the if (if backwards).

The test operators worth memorising
Test

True if...

Test

True if...

-f FILE

regular file exists

-z STR

string is empty

-d DIR

directory exists

-n STR

string is non-empty

-e PATH

path exists (any type)

STR = STR

strings equal

-r / -w / -x

readable/writable/executab
le

STR != STR

strings differ

-s FILE

file exists and non-empty

N -eq M

numbers equal

A && B

both true

N -lt M

N less than M

A || B

either true

N -gt M

N greater than M

PRO INSIGHT: Two brackets that trip people up: use [[ ]] for strings and files, and (( )) for numbers. Inside (( )) you
write natural math: if (( count > 100 )). Inside [[ ]] you use -gt, -lt, -eq for numbers and = for strings. Mixing them up
('>' inside [[ ]] means redirection, not greater-than!) is a classic bug. Strings and files: [[ ]]. Pure numbers: (( )).

case — cleaner than many elifs





case "$1" in
start) echo "Starting..." ;;
stop) echo "Stopping..." ;;
restart) echo "Restarting..." ;;
*) echo "Usage: $0 {start|stop|restart}" ;;
esac

1. case matches $1 against patterns — far cleaner than a chain of elif for fixed choices.