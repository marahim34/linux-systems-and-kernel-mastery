11. Finding Any File on the System — the Complete
Toolkit
Five tools, five jobs
'Where is that file?' has several answers depending on what you are looking for. Here is the complete toolkit,
each tool for its purpose. Together they mean nothing on your system is ever truly lost.
Tool

Finds

Speed

Best for

which / type

A command in your PATH

Instant

'Where is the git
executable?'

locate

Any file, by a prebuilt index

Very fast

'Where is that file called
nginx.conf?'

find

Any file, by live search +
any criterion

Slower

Complex searches: by
size, time, permission

dpkg -S / -L

Files belonging to
packages

Fast

'What installed this / where
did it go?'

grep -r

TEXT inside files

Slower

'Which file contains this
setting?'

The tools in action
which docker
locate nginx.conf
sudo updatedb
find /etc -name "*.conf" -mtime -7
grep -rn "server_name" /etc/nginx/
dpkg -S $(which docker)