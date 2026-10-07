5. Full history of one file. Every event carries auid — the ORIGINAL login identity, surviving sudo: 'root did it' becomes
'abdur, via sudo, did it'.

PRO INSIGHT: A useful audit setup is small: watch identity files (/etc/passwd, shadow, sudoers), your secrets, your
app configs, and exec by real users. Watching everything drowns the signal and the disk.
PRACTICE EXERCISES