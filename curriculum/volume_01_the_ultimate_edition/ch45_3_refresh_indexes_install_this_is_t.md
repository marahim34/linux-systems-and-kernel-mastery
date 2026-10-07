3. Refresh indexes; install. This is the modern, correct pattern (the old apt-key is deprecated).

Python, Node and language packages — avoiding the classic traps





python3 -m venv ~/venvs/goodo
source ~/venvs/goodo/bin/activate
pip install -r requirements.txt
deactivate
pipx install httpie