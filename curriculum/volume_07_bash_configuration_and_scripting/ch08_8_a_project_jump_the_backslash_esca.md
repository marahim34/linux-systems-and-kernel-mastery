8. A project jump — the backslash escapes the space in the path. One word to reach GoOdo.

PRO INSIGHT: An important subtlety: aliases only do simple word-for-word replacement and cannot take
arguments in the middle. When you need to USE an argument, you need a FUNCTION (Chapter 4), not an alias.
Rule of thumb: no argument, or argument at the end only, use an alias; argument used in the middle, use a
function.

Useful shell options
shopt -s autocd
shopt -s cdspell
shopt -s checkwinsize
shopt -s globstar