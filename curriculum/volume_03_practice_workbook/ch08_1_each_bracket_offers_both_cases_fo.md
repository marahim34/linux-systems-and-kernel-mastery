1. Each bracket offers both cases for one letter, so every combination of upper and lower case across the three letters is
covered by a single glob.

3.5 Suspicious filenames
List names containing anything other than letters, numbers, _ - or dot.
ls | grep -E '[^A-Za-z0-9_.-]'