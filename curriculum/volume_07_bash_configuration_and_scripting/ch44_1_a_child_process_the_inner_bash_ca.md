1. A child process (the inner bash) cannot see MSG until it is exported. Before export, the child prints nothing for $MSG;
after export, it sees 'hi'. This is exactly why your app needs exported env vars.

Part B — Scripting
Ch.8 — Quoting a name with a space





name="Abdur Rahim"
echo "$name" # Abdur Rahim (one piece)
echo $name # Abdur Rahim (two words to any command)