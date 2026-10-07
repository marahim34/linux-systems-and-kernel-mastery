1. In your login-shell file...
2. ...if a .bashrc exists...
3. ...SOURCE it (the dot means 'run this file's commands in the current shell'). This one block makes login shells ALSO
read .bashrc, so your settings work everywhere — over SSH and in local terminals alike.

PRO INSIGHT: The practical rule that ends all confusion: put ALL your real settings in ~/.bashrc, and make
~/.bash_profile source it with the block above. Then you have ONE file to edit, and it applies to every kind of shell.
This is what experienced users do, and it is why most people only ever touch .bashrc. Ubuntu's default .profile
already sources .bashrc for you — which is why it 'just works' there.

Applying changes without logging out
source ~/.bashrc
. ~/.bashrc
exec bash