2. Dispatch on the command...
3. ...each case performs a device-specific action...
4. ...or returns a value.
5. -ENOTTY is the conventional 'this ioctl is not supported' error.
6. ioctl is how tools like hdparm and mount configure devices — commands that do not fit the read/write model.

PRACTICE EXERCISES