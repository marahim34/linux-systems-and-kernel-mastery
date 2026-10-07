5. Leave the environment; PATH returns to normal.

PRO INSIGHT: The hard rule every Python developer learns, often painfully: NEVER run sudo pip install to put
packages in the system Python. apt and pip will fight over the same files and eventually break each other,
sometimes badly enough to damage system tools written in Python. ALWAYS use a virtual environment (venv) per
project, or pipx for standalone tools. This isolation is exactly the PATH mechanism from Chapter 3 at work — the
venv's bin goes first.

pipx install httpie
pipx list

1. pipx installs a Python TOOL (not a library) in its own hidden environment but makes it available everywhere — the
best of both worlds for command-line tools.