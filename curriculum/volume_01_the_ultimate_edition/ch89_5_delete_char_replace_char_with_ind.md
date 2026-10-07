5. Delete char / replace char with " / indent / unindent line.

Command-mode power
:w :q :wq :q!
:%s/localhost/127.0.0.1/g
:%s/DEBUG/INFO/gc
:g/^#/d
:5,20y
:!ls
:r !date