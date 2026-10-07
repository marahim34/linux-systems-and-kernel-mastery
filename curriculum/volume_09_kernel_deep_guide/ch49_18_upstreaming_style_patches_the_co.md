18. Upstreaming — Style, Patches & the Community
The path from your code to the mainline kernel
scripts/checkpatch.pl --strict 0001-my-patch.patch
git format-patch -1 --signoff
./scripts/get_maintainer.pl 0001-my-patch.patch
git send-email --to=maintainer@... --cc=linux-kernel@vger.kernel.org 0001-*.patch

1. checkpatch --strict enforces kernel coding style; fix EVERY warning before sending, or reviewers stop reading.
2. format-patch produces a mailable patch; --signoff adds your Signed-off-by line, the legal Developer Certificate of
Origin attestation (required).
3. get_maintainer identifies who to email — patches go to the subsystem maintainer and relevant lists, not a web form.
4. send-email delivers it as plain-text email (never HTML). Maintainers review on the list; expect revisions across
several versions (v2, v3...).

What reviewers expect
Expectation

Meaning

One logical change per patch

Split large work into a reviewable series

Clear commit message

WHY the change, not just what; reference the problem

Signed-off-by

The DCO attestation of your right to submit

checkpatch-clean

No style violations

Responds to feedback

Revise and resend; engage respectfully

No regressions

'We do not break userspace' — tested

PRO INSIGHT: Upstreaming is a craft and a culture, not just a technical step. The kernel community values small,
well-explained, correct patches and rewards persistence through review. Your first patch will likely get critical
feedback — that is normal and not personal; revise and resend. Start with drivers/staging, Documentation fixes, or
a small real bug. Getting a patch into the mainline kernel is a permanent, verifiable credential that few engineers
hold, and for someone building a company like Aisora, it is a powerful signal of deep systems competence. The
path is open to anyone who does the work correctly.