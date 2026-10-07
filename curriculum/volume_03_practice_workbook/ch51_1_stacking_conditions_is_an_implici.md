1. Stacking conditions is an implicit AND: a match must be a file, end in .log, AND exceed 10 kilobytes. No -a is needed,
though it is allowed.

Section 13 — Shell Environment
13a. Add ~/bin to PATH permanently
mkdir -p ~/bin
echo 'export PATH="$HOME/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
printf '#!/bin/bash\necho hello\n' > ~/bin/hi
chmod +x ~/bin/hi
hi