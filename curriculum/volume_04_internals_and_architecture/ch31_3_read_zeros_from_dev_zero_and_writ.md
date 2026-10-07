3. Read zeros from /dev/zero and write a 10 MB blank file — creating storage from a virtual device. dd is the low-level
copy tool.

PRO INSIGHT: Unique point: because devices are files, the ENTIRE toolset you learned — cat, dd, redirection,
permissions — works on hardware. Backing up a whole disk is cat /dev/sda > backup.img. Wiping one is cat
/dev/zero > /dev/sda. Controlling access to a device is chmod on its file. No other design gives you the whole
operating system's vocabulary for talking to hardware. This is the deepest meaning of 'everything is a file', and it is
uniquely Linux/Unix.