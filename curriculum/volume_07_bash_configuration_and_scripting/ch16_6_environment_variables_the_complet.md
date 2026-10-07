6. Environment Variables — the Complete Picture
Shell variables versus environment variables
A shell variable exists only in the current shell. An environment variable is exported, so it is inherited by
every program the shell launches. This distinction decides whether a program you run can see your variable.
NAME="Abdur"
echo $NAME
export EDITOR="nano"
env | sort | less
printenv PATH