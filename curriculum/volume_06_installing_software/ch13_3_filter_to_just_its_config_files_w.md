3. Filter to just its config files — where are the settings I need to edit? This instantly answers 'where is nginx's config?'
(/etc/nginx/).

Question 2: which package owns this file?
dpkg -S /usr/bin/git
dpkg -S /etc/ssh/sshd_config
which nginx | xargs dpkg -S