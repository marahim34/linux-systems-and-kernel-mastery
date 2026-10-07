3. Chain them: find a command's path with which, then ask dpkg which package owns it. A two-step identification of any
command on the system.

PRO INSIGHT: These two commands, dpkg -L (package to files) and dpkg -S (file to package), are the answer to
'where is this program's config?' and 'what installed this mystery file?'. Master them and the filesystem stops being a
mystery. Example workflow: you install a service, it does not work, you need its config — dpkg -L servicename |
grep etc shows you exactly where to look. No guessing, no googling.

Verifying and inspecting an installed package
dpkg -l | grep nginx
dpkg -s nginx
dpkg -L nginx | xargs -I{} sh -c 'test -f "{}" && echo "{}"' | head