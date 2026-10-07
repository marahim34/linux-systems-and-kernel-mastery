8. The + variant batches many files into one command — much faster. This line: clean week-old temp files.

Wildcards (globs) — the shell's pattern language
Pattern

Matches

Example

*

anything, any length

*.py — all Python files





Pattern

Matches

Example

?

exactly one character

log?.txt — log1.txt, logA.txt

[abc]

one char from the set

report[12].pdf

[0-9]

one char in range

backup-202[0-6]*

{a,b}

either alternative

cp app.{py,py.bak} — expands to two
names

**

recursive (bash: shopt -s globstar)

ls **/*.md — all markdown, any depth

PRACTICE EXERCISES