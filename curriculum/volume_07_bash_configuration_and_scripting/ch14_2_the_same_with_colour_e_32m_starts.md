2. The same with COLOUR: \e[32m starts green, \e[34m blue, \e[0m resets. The \[ \] wrappers tell bash these are
non-printing characters (crucial, or long commands wrap wrongly). Green user@host, blue directory.

PRO INSIGHT: The \[ \] wrappers around colour codes are not optional. They tell bash 'these characters take no
screen space'. Omit them and bash miscalculates the line length, causing the cursor and text to wrap and overwrite
themselves on long commands — a maddening bug with a trivial cause. Any colour code in PS1 must be wrapped
this way.

Adding the git branch
parse_git_branch() {
git branch 2>/dev/null | grep '^*' | sed 's/* //'
}
PS1='\w$(parse_git_branch)\$ '