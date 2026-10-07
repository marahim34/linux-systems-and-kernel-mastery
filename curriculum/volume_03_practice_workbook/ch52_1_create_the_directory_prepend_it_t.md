1. Create the directory, prepend it to PATH in .bashrc, reload, then drop an executable script in ~/bin. Because ~/bin is
first in PATH, typing hi runs your script from anywhere.

13b. A custom prompt
echo "PS1='[\u@\h \w]\$ '" >> ~/.bashrc
source ~/.bashrc

1. \u user, \h host, \w directory, \$ the prompt sign. Reload with source to see it immediately. Colour codes can be
added later once the basics feel comfortable.

13c. Print PATH one entry per line
echo $PATH | tr ':' '\n'

1. tr translates each colon into a newline, so every PATH directory prints on its own line, easy to read.

Section 14 — User Commands
14a. Add the four functions
# paste _lsd _lsf _ps _lsize into ~/.bashrc, then:
source ~/.bashrc
_lsd ; _lsf ; _lsize