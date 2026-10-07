6. Users, Groups & Permissions — Complete
The model
Every file carries: an owner (user), a group, and three permission triplets — what the owner may do, what
group members may do, what everyone else may do. Each triplet is rwx: read, write, execute. That's the
whole model; everything else is detail.

What rwx really means — files vs directories
Permission

On a file

On a directory

r (4)

read contents

list the names inside (ls)

w (2)

modify contents

create/delete/rename entries inside

x (1)

run as a program

enter it (cd) and access things inside

WARNING: Directory subtlety that trips everyone: to delete a file you need w on its DIRECTORY, not on the file
itself. A read-only file inside a writable directory can still be deleted.

Numeric permissions — do the math once
Each triplet sums: r=4, w=2, x=1. So rwx=7, r-x=5, rw-=6, r--=4. Three triplets → three digits: 754 = rwxr-xr-(owner everything, group read+exec, others read only).
chmod 644 index.html
chmod 755 deploy.sh
chmod 600 ~/.ssh/id_ed25519
chmod 700 ~/.ssh
chmod -R 755 /var/www/html
chmod u+x,go-w script.sh
chmod +x script.sh