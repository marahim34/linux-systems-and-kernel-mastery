6. Identify which package a command came from, in one line.

PRO INSIGHT: The decision tree for 'find my file': Is it a COMMAND? Use which/type. Do you know its NAME? Use
locate (fast) or find (flexible). Do you know it belongs to a PACKAGE? Use dpkg -L. Are you searching for TEXT
inside files? Use grep -r. Matching the tool to the question is the whole skill — and it turns 'I can't find anything on
Linux' into 'I can find anything on Linux'.

The modern fast alternatives





fd conf /etc
rg "server_name" /etc/nginx/

1. fd is a faster, friendlier find (Volume 2) — fd conf /etc finds config files quickly.
2. rg (ripgrep) is a much faster grep -r — the modern tool for searching text in files. Both are optional upgrades over the
classics, which exist everywhere.

PRACTICE EXERCISES