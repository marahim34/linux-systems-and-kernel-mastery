3. All installed shells the system knows about.
4. $$ is the current shell's process ID; this shows which shell you are running RIGHT NOW (useful if you switched).

The distinction that controls startup: login vs interactive
Bash decides WHICH configuration files to read based on how it was started. There are two independent
questions, and the answers determine everything in Chapter 2.
Question

Yes means

Example

Is it a LOGIN shell?

Started by logging in (SSH, console)

ssh into a server

Is it INTERACTIVE?

You type commands at a prompt

Any terminal you type in

A terminal you open on your desktop is usually interactive but NOT login. An SSH connection is both login
AND interactive. A script runs in a shell that is neither. These combinations decide which startup files run,
which is the single most confusing thing about bash — and Chapter 2 makes it simple.
PRO INSIGHT: Why this matters in practice: if you put a setting in the wrong startup file, it works when you open a
local terminal but NOT over SSH, or vice versa. Almost every '.bashrc doesn't work over SSH' problem comes from
not understanding login vs interactive. Learn this distinction once and those mysteries vanish.
PRACTICE EXERCISES