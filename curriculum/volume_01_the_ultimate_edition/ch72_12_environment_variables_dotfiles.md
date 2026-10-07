12. Environment, Variables & Dotfiles
How environment variables flow
FOO=bar python3 -c "import os; print(os.environ['FOO'])"
export DATABASE_URL="postgres://..."
env | sort | less
echo $PATH | tr ':' '\n'