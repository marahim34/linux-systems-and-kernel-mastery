4. Plugin picks: git aliases; z = jump to any directory by fragment (z goodo); sudo = double-press Esc prefixes sudo;
docker completion. Everything from both volumes still works — zsh runs your bash knowledge.

The new-generation tools
Tool

Replaces

Why it wins

ripgrep (rg)

grep -rn

5–50x faster, respects .gitignore,
sane defaults: rg TODO

fd

find

fd -e py pattern — intuitive syntax,
fast, gitignore-aware

fzf

—

fuzzy-finds ANYTHING: Ctrl+R
history, Ctrl+T files, ** completion

bat

cat

syntax highlighting + line numbers +
git markers

eza

ls

eza -la --git — colors, tree mode, git
status column

zoxide

cd

learns your habits: z back(end) jumps
to your most-used match

jq / yq

—

query JSON/YAML in pipes: curl api |
jq '.items[].name'

btop

top/htop

the monitor you'll actually enjoy
reading

tldr

man (for recall)

examples-first help: tldr tar





sudo apt install ripgrep fd-find bat fzf jq
rg "OdometerManager" --type dart
fd -e log -x gzip {}
history | fzf
curl -s https://api.github.com/repos/flutter/flutter | jq '.stargazers_count'