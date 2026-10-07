5. Report how many were given.

Functions with arguments and return values





greet() {
local name="$1"
echo "Hello, $name"
}
is_running() {
systemctl is-active --quiet "$1"
return $?
}
greet "Abdur"
if is_running nginx; then echo "nginx up"; fi