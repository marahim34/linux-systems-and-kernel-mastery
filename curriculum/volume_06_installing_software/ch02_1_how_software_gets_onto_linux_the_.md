1. How Software Gets Onto Linux — the Big Picture
The Linux way is different from Windows
On Windows you download an .exe from a website and double-click it. On Linux, the normal way is the
opposite: you ask a package manager to fetch and install software from a trusted repository — a central,
curated collection of thousands of programs. You rarely download from random websites. This is safer,
faster, and keeps everything updatable from one place.

The five ways to install software — and when to use each
This is the map for the whole volume. Nearly every installation you ever do falls into one of these five
categories. Knowing which to reach for is half the skill.
Method

What it is

When to use it

Chapter

System package manager

apt fetches from official
repos

DEFAULT choice —
always try this first

4

Universal packages

Snap, Flatpak, AppImage

Newer apps not in the
repos, or GUI apps

7

Language managers

pip, npm, cargo, etc.

Developer libraries and
tools for a language

8

From source

compile the code yourself

Latest version, or software
not packaged anywhere

9

Downloaded files

.deb, tarball, single binary

Vendor gives you a file
directly (Docker, Chrome)

10

PRO INSIGHT: The golden rule of installing on Linux: ALWAYS try the system package manager (apt) first. It
handles dependencies, security updates, and clean removal automatically. Only move down the list — to snaps,
language managers, source, or downloaded files — when apt does not have what you need or has too old a
version. Reaching for a website download first is a Windows habit worth unlearning.

Why repositories are safer
A repository's packages are cryptographically signed by the distribution. When apt installs one, it verifies the
signature, guaranteeing the software really came from the trusted source and was not tampered with.
Downloading a random .deb or piping a website script into your shell (curl ... | bash) skips this protection —
sometimes necessary, but always a step down in safety. Understanding this trade-off is part of thinking like a
Linux administrator.