1. Vim — Configuration and Editing
1.1 Vim configuration location
Where is the user's personal Vim configuration file?
~/.vimrc

1. ~ is your HOME directory; .vimrc is the personal config vim reads on startup. It holds all your personal settings. A
leading dot makes it hidden from a normal ls.

1.2 A useful .vimrc
Set common editing preferences, each explained inline with Vim comments (").
set ruler " show cursor position in status line
set nojoinspaces " no double space after punctuation on join
set showcmd " show partial commands bottom-right
set showmatch " highlight matching bracket
set incsearch " show matches while typing a search
set ignorecase " search ignores case...
set smartcase " ...unless the query has a capital
set nobackup " do not leave backup~ files
set autoindent " new lines keep the previous indent
set shiftwidth=4 " indent step is 4 columns
set softtabstop=4 " Tab key inserts 4 spaces
set nolist " do not draw whitespace symbols