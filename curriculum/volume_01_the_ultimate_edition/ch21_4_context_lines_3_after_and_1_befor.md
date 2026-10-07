4. Context lines: 3 After and 1 Before each match — see the whole Python traceback, not just its first line.
5. -w whole words only: matches 'port' but not 'export' or 'important'.
6. -o prints only the matching part, not the whole line — extracts every URL from a page.
7. -E enables extended regex: lines beginning (^) with GET or POST.

Regex in 10 minutes — the 20% you use 95% of the time
Symbol

Means

Example

^$

start / end of line

^root — lines starting with root

.

any single character

b.t matches bat, bit, but





Symbol

Means

Example

*+?

0+, 1+, 0-or-1 of previous

go+gle matches google, gooogle

[abc] [^abc]

set / negated set

[0-9]+ — one or more digits

(|)

grouping and OR

(jpg|png|gif)$

\.

literal dot (escape specials)

192\.168\. — an IP prefix

{n,m}

repetition count

[0-9]{1,3} — 1 to 3 digits

grep -E "^[a-zA-Z0-9._]+@[a-z]+\.[a-z]{2,}$" emails.txt