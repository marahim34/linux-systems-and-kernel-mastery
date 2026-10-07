5. Pipes — Composing Commands
5.1 Which pipelines make sense
Judge each; two are nonsense.
ls | cat | less # sensible
cat < file | less # sensible (= less file)
cat file | ls > file # nonsense: ls ignores stdin, and clobbers file
ls | less > cat file # nonsense: invalid syntax