8. Language Package Managers — pip, npm &
friends
A different layer of software
Developer libraries — a Python HTTP library, a Node.js framework — are not installed with apt. Each
programming language has its OWN package manager pulling from its OWN repository (PyPI for Python,
npm registry for Node). These install language-specific code, usually for a project or a user, not system-wide.
Language

Manager

Repository

Installs

Python

pip

PyPI

pip install requests

Node.js

npm

npm registry

npm install express

Rust

cargo

crates.io

cargo install ripgrep

Ruby

gem

RubyGems

gem install rails

The critical rule: never pollute the system Python
python3 -m venv ~/venvs/myproject
source ~/venvs/myproject/bin/activate
pip install requests fastapi
pip list
deactivate