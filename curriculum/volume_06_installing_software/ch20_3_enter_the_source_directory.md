3. Enter the source directory.
4. configure inspects your system and prepares the build, checking that dependencies exist. Read its output for
missing-library errors.
5. make actually COMPILES the source into an executable — this can take a while.
6. make install COPIES the built program into place, by default under /usr/local (Chapter 2's convention), so it never
clashes with apt's files.

PRO INSIGHT: The reason source installs default to /usr/local: it keeps YOUR compiled software cleanly separated
from the package manager's territory in /usr. But there is a cost — apt does not know this software exists, so it will
never update or track it. You are now the package manager for that program. This is why source-installing is a
deliberate choice, not a default, and why tools like checkinstall or building your own .deb exist for people who do it
often.

Uninstalling a source install
# from the same source directory, IF the project supports it:
sudo make uninstall
# otherwise you must remove files manually — which is why
# many people avoid source installs for casual software