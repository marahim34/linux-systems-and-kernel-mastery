7. The Other Package Systems — Snap, Flatpak,
AppImage
Why these exist
APT packages are built for one specific distribution version. Newer 'universal' formats bundle an app WITH
its dependencies so one file runs on any distro, and can update independently of the system. They are
heavier but more portable. You meet them when an app is not in the apt repos, or the apt version is too old.
Format

How it works

Install / run

Trade-off

Snap

Sandboxed, auto-updating,
from Canonical's store

snap install code

Convenient, but larger and
slower to start

Flatpak

Sandboxed, from Flathub,
popular for desktop apps

flatpak install flathub
org.gimp.GIMP

Great for GUI apps; needs
setup

AppImage

One self-contained file you
just run

chmod +x app.AppImage
&amp;&amp;
./app.AppImage

No install at all; you
manage updates yourself

snap find spotify
sudo snap install code --classic
snap list
snap info code
sudo snap remove code