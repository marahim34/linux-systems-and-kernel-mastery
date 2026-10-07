5. Silence everything: output to the void, errors follow output (2>&1 = 'send stream 2 where 1 goes').
6. tee splits the stream: show on screen AND save to file simultaneously — watch and log at once.

grep — complete treatment
grep -i "error" app.log
grep -rn "OdometerManager" lib/
grep -l "TODO" *.py
grep -A 3 -B 1 "Traceback" app.log
grep -w "port" nginx.conf
grep -o "https://[^ ]*" page.html
grep -E "^(GET|POST)" access.log