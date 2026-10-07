2. Transform

execve()

The copy REPLACES its own
program with the new one it wants to
run.

# conceptually, when bash runs 'ls':
pid = fork(); # bash duplicates itself
if (pid == 0) { # in the child copy:
execve("/usr/bin/ls", ...); # become ls
} else { # in the parent (bash):
wait(pid); # wait for ls to finish
}

1. bash clones itself with fork; now two bash processes exist, parent and child.