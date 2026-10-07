1. Four ? match exactly four name characters, the dot is literal, and * matches any extension. So it matches abcd.txt but
not abc.txt.

3c. Why 3.5 needs grep
ls | grep -E '[^A-Za-z0-9_.-]'