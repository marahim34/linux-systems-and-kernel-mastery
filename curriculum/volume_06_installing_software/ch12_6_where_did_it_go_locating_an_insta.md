6. Where Did It Go? — Locating an Installed
Program's Files
The two questions you will always ask
After installing something, two questions recur: 'WHERE did all its files go?' and 'WHICH package does this
file belong to?'. dpkg answers both. These are among the most useful commands in daily Linux life, and
almost no beginner knows them.

Question 1: what files did this package install?
dpkg -L nginx
dpkg -L nginx | grep bin
dpkg -L nginx | grep etc