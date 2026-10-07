# Tier 1 · Chapter 1: Terminal & Shell Foundations

## 1. The Anatomy of the Linux Terminal
In Linux, the terminal is a text-based interface connecting the user to the command interpreter.
When you type a command:
1. The terminal emulator captures keystrokes and transmits them to the pseudo-terminal slave (PTS).
2. The PTS delivers the character stream to the interactive shell (typically `/bin/bash` or `/bin/zsh`).
3. The shell parses the line into tokens, performs expansions, searches `$PATH`, and invokes `fork()` and `execve()`.

## 2. Standard Streams & Redirection Mechanics
Every Linux process starts with three default file descriptors:
- **0 (STDIN)**: Standard Input
- **1 (STDOUT)**: Standard Output
- **2 (STDERR)**: Standard Error

### Essential Redirection Operators
```bash
# Redirect stdout to file (overwrite)
echo "production" > config.txt

# Redirect stdout to file (append)
echo "new entry" >> config.txt

# Redirect stderr only
command 2> errors.log

# Combine stdout and stderr into one stream
command > output.log 2>&1
# Modern bash shorthand:
command &> output.log

# Discard all output (black hole)
command > /dev/null 2>&1
```

## 3. The Pipe Operator (`|`)
Pipes create an anonymous unidirectional data channel in kernel memory between two processes:
```bash
cat /var/log/syslog | grep "CRITICAL" | wc -l
```
