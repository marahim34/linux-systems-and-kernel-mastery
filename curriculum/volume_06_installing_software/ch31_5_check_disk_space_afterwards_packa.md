5. Check disk space afterwards — package caches and old kernels are common space eaters.

Troubleshooting the common failures
Problem

Cause

Fix

'Unable to locate package'

Stale catalogue

sudo apt update first

'held broken packages'

Dependency conflict

sudo apt install -f (fix broken)

Interrupted install

apt/dpkg stopped mid-way

sudo dpkg --configure -a

'Could not get lock'

Another apt is running

Wait, or find it: ps aux | grep apt

Command exists but not found

Not in PATH

Find it (Ch. 11), add its dir to PATH
(Ch. 3)

Wrong version runs

Another copy earlier in PATH

type -a CMD to see all; fix PATH
order

sudo dpkg --configure -a
sudo apt install -f
sudo apt update --fix-missing