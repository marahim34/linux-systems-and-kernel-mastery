4. Redirection — stdin, stdout, stderr
Every command has three streams: input (fd 0), normal output (fd 1), and errors (fd 2). Redirection sends
each stream to or from a file. Getting this precise is what separates confident users from hopeful ones.

4.1 Save output to a file
Write the current date into date.txt.
date > date.txt

1. > sends stdout (fd 1) to a file, creating or overwriting it. The terminal shows nothing because the output went to the
file instead.

4.2 Save only errors
Run a non-existent command and capture its error.
qwerty 2> error.log

1. 2> redirects stderr (fd 2) only. The shell's 'command not found' message is an error, so it lands in error.log while
stdout (empty here) is untouched.

4.3 A subtle one: echo 2 2>2
What does this create?
echo 2 2>2

1. echo writes the text 2 to stdout (the terminal). The 2>2 part redirects stderr to a file literally named 2. echo produces
no errors, so the file 2 is created but stays empty. A neat trap that tests whether you can separate the two streams.

4.4 Split output and errors
Send stdout and stderr to different files; order does not matter.
cat qwerty 2> error.log 1> file.tmp

1. cat on a missing file prints normal output nowhere and an error to stderr. 1> file.tmp catches stdout, 2> error.log
catches stderr. Writing them in either order gives the same result, so the error message reliably lands in error.log.

4.5 Feed a file as input
Page through a log by redirecting stdin.
less < /var/log/dpkg.log

1. < redirects stdin from a file. less with no filename argument reads stdin, so this is equivalent to less /var/log/dpkg.log.
Useful to know because many filters read stdin the same way.

4.6 The self-referential trap
With an empty file named ls present, what does ls < ls > ls do?





ls < ls > ls