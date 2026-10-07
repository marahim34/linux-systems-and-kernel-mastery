12. Real-World Scripts — Input, Files & Error
Handling
Reading user input
read -p "Enter your name: " name
echo "Hello, $name"
read -sp "Password: " pass; echo
read -p "Continue? [y/N] " ans
[[ "$ans" == "y" ]] || exit 0

1. read -p prompts and stores the reply in a variable.
2. -s hides input (for passwords); the echo adds the missing newline.