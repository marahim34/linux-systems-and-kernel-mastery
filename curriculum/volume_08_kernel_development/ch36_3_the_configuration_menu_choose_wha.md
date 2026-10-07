3. The configuration menu — choose what to build into the kernel or as modules.
4. get_maintainer.pl tells you WHO maintains a file — essential before submitting a patch, since you email it to them.

Kernel coding style — non-negotiable
Rule

The kernel way

Indentation

TABS, 8 characters wide

Braces

Opening brace on same line (except functions)

Line length

Aim for 80 columns

Naming

lower_case_with_underscores, short

Comments

/* C-style */, explain WHY not what

No typedefs for structs

Use 'struct foo', not a hidden typedef

scripts/checkpatch.pl --file drivers/char/mydriver.c

1. checkpatch.pl automatically checks your code against the kernel style rules. Run it before EVER submitting —
maintainers will reject style violations immediately. It catches whitespace, naming, and structural issues.

How a contribution actually happens
The Linux kernel is developed by email patches, not pull requests. The workflow: make your change,
commit it with a clear message, generate a patch with git format-patch, check it with checkpatch, then send
it with git send-email to the maintainer and mailing list found via get_maintainer.pl. Maintainers review,
request changes, and eventually a patch is accepted into a subsystem tree, then Linus's tree. It is rigorous,
public, and meritocratic.
PRO INSIGHT: A realistic first contribution: start in drivers/staging/ (drivers being cleaned up) or with
Documentation fixes and checkpatch cleanups. These are welcomed from newcomers and teach the workflow
without deep subsystem knowledge. Every kernel contributor started with a small patch. Your name in the Linux
kernel git history is an achievable, career-defining goal — and it begins with one correctly-formatted,
checkpatch-clean patch emailed to the right maintainer.
PRACTICE EXERCISES