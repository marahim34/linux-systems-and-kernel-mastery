14c. mkcd — make and enter
mkcd() {
mkdir -p "$1" && cd "$1"
}

1. $1 is the first argument. mkdir -p creates the directory (and parents), and on success (&&) cd moves into it. A
daily-use convenience function.

Every answer here is a starting point, not the only route. If your working command
differs but produces the right result, you have understood it.
— End of Solutions —

LINUX MASTERY
VOLUME 7 — BASH:
CONFIGURATION & SCRIPTING
The Complete Shell Book — Startup Files, .bashrc, Aliases, Functions, the Prompt,
Environment & History, then Writing Real Programs: Variables, Loops, Conditionals,
Arguments, Error Handling & Debugging — with Worked Examples and Solutions

Everything about the shell you type into and program with · Prepared for MD Abdur
Rahim · 2026





Table of Contents — Volume 7
PART A — Configuring Your Shell