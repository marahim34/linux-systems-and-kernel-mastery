6. Update the WSL kernel itself.

The filesystem boundary — the #1 performance rule
Location

What it is

Speed for Linux tools

~ (ext4, inside WSL)

Native Linux filesystem

FAST — keep code, git repos,
node_modules here

/mnt/c, /mnt/d

Windows drives via 9P bridge

SLOW for many-small-files work (git
status, builds can be 10x slower)

\\wsl$\Ubuntu\home\...

Linux files seen from Windows
Explorer

How Windows apps reach your Linux
files

PRO INSIGHT: Your GoOdo project lives at /mnt/d — Flutter builds and git operations there pay the 9P tax on
every file. Ideal setup: repo cloned inside ~ for speed; Windows-side tools access it via \\wsl$. If you must keep it on
D:, at least run flutter pub get and gradle builds from Windows-side tooling.

Windows ↔ Linux interop tricks





explorer.exe .
code .
notepad.exe file.txt
cmd.exe /c dir
cat report.md | clip.exe
powershell.exe -c "Get-Process" | head
wslpath 'D:\GoOdo\GoOdo App'
adb devices