6. Meta Characters — Command Substitution
6.1 Embed a command's result
Print a sentence that includes a computed line count.
echo "The result of this command is $(ls -la | wc -l)"

1. $( ) runs the inner command first and substitutes its output into the surrounding text. Inside it, ls -la lists the directory
and wc -l counts the lines. The shell replaces the whole $( ... ) with that number before echo prints the sentence.

6.2 Insert the current time
Display the time as HH:MM:SS using no variables.
echo "Time is $(date +%H:%M:%S)"

1. date +%H:%M:%S formats the current time. Wrapped in $( ), its output is pasted into the string, so echo prints a live
timestamp. The + introduces a custom format where %H %M %S are hours, minutes, seconds.

PRACTICE EXERCISES