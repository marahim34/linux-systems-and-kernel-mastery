4. For secrets, read from a locked-down file rather than writing the value into .bashrc...
5. ...and restrict that file to yourself. Never commit secrets into a dotfile that might reach GitHub.

PRO INSIGHT: The export rule in one line: if a PROGRAM you run needs to see the variable, it must be exported; if
only the shell itself uses it, a plain variable suffices. This is exactly why DATABASE_URL and API_KEY must be
exported for your FastAPI app to read them, while a loop counter in a script needs no export. Understanding this
prevents the 'my program can't see the variable' confusion.
PRACTICE EXERCISES