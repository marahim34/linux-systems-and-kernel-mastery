5. Unfreeze it again when you are ready.





The dpkg layer underneath
apt is a friendly front-end over dpkg, the low-level tool that actually installs .deb files and tracks what is
installed. You use dpkg directly mainly to ASK questions about installed packages, which Chapter 6 covers in
full. For now, know that apt handles downloading and dependencies, while dpkg handles the actual
unpacking and record-keeping.
PRACTICE EXERCISES