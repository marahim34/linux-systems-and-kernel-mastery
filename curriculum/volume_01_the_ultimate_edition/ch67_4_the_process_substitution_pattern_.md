4. The process-substitution pattern < <(...) feeds find results line-by-line safely — the professional replacement for the
broken `for f in $(find ...)`.

Arguments like a real CLI tool — getopts





while getopts "e:vh" opt; do
case $opt in
e) ENV="$OPTARG" ;;
v) VERBOSE=1 ;;
h) usage; exit 0 ;;
*) usage; exit 1 ;;
esac
done
shift $((OPTIND - 1))