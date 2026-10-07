5. Verify the caller has the required privilege before a sensitive operation — omitting this is a real, common CVE pattern.

PRO INSIGHT: Kernel code is the ultimate trust boundary: it runs with full privilege, and its inputs come from
untrusted userspace and hardware. Every value crossing into the kernel is hostile until validated. The mindset —
validate all input, check every arithmetic operation for overflow, track ownership to prevent use-after-free, hold locks
across whole check-and-use sequences, zero memory before it can leak, and verify privileges — is not paranoia; it
is the difference between a driver and a CVE. For your eQuorum work serving banks, this security-first kernel
mindset transfers directly to writing trustworthy systems.