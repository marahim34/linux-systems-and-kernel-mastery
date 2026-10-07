5. Finding & Choosing Packages
You know what you want to DO, not the package name
The real-world problem: you want 'a tool to edit photos' or 'the thing that provides the dig command', but you
do not know the package's name. These commands bridge the gap between intent and package name — a
skill used constantly.
apt search "image editor"
apt show gimp
apt-cache search pdf | head
apt-file update && apt-file search bin/dig