4. The powerful one: apt-file finds which PACKAGE PROVIDES a given file or command. Here it answers 'which
package gives me the dig command?' (answer: dnsutils). Install apt-file first with apt install apt-file.

PRO INSIGHT: The 'command not found, which package has it?' solution: apt-file search. When a tutorial tells you
to run a command you do not have, apt-file search bin/thatcommand names the package to install. Ubuntu even
does this automatically — try running an uninstalled command and it often suggests 'apt install X'. This closes the
most frustrating beginner gap: knowing the command name but not the package.

Judging a package before installing
apt show nginx
apt-cache depends nginx
apt-cache rdepends nginx | head