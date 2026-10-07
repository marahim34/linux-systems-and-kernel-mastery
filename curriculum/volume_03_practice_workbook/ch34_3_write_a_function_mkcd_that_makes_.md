3. Write a function mkcd() that makes a directory and cd's into it in one step.

Work every exercise by hand. Reading the answer is learning; typing it is
remembering.
— End of Volume 3, The Practice Workbook —

Solutions to the Practice Exercises
Worked answers to every 'Practice Exercises' box in this workbook. Try each yourself first, then check here.
Where several answers are valid, one good approach is shown.

Section 1 — Vim
1a. Create ~/.vimrc and confirm behaviour
cp /dev/null ~/.vimrc # or: nano ~/.vimrc
printf 'set ruler\nset number\n' >> ~/.vimrc
vim testfile.txt