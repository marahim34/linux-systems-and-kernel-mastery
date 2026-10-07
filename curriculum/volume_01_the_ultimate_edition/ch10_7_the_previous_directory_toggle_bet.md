7. The previous directory — toggle between two work locations.

Hidden files and dotfiles
ls -a ~
ls -d ~/.*

1. -a reveals entries starting with a dot: .bashrc, .ssh, .gitconfig — hidden by convention, not security. These 'dotfiles'
hold your personal configuration.
2. -d lists the dot-entries themselves without descending into them.

Links — two kinds of shortcuts
ln -s /opt/goodo/config.yaml ~/config.yaml
ln /data/report.pdf /backup/report.pdf
ls -l ~/config.yaml