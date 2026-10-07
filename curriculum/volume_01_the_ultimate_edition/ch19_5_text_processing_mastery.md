5. Text Processing Mastery
The philosophy: small tools, composed
Unix's founding idea: each program does one thing well and reads/writes plain text, so any output can feed
any input through a pipe. Mastering five tools — grep, sed, awk, sort, uniq — plus pipes gives you a
data-processing engine more flexible than most GUI software.

The three streams
command < input.txt
command > output.txt
command 2> errors.txt
command >> log.txt
command > /dev/null 2>&1
command | tee output.txt

1. stdin (stream 0): feed a file as input.
2. stdout (stream 1): capture normal output (overwrite).
3. stderr (stream 2): capture only errors — they are separate streams, which is why error messages 'escape' your
redirects.