1. In vim, a double quote begins a comment. Each set line toggles one option. ignorecase + smartcase together give the
smartest search behaviour: case-insensitive until you deliberately type an uppercase letter. autoindent, shiftwidth and
softtabstop are the three that make code editing comfortable.

1.3 Essential editing keys
The movements and edits you use constantly (press in Normal mode, Esc first).
0 -> beginning of line
$ -> end of line
dw -> delete a word
dd -> delete a line
dap -> delete a paragraph
gg -> go to first line
G -> go to last line
yy -> yank (copy) a line
yap -> yank a paragraph
:set number / :set nonumber -> line numbers on / off