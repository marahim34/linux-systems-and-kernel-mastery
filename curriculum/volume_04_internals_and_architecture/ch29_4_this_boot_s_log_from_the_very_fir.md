4. This boot's log from the very first message — watch the machine assemble itself in real time.

PRO INSIGHT: Unique point: each boot stage is deliberately minimal and does ONE thing — hand off to the next.
This staged design is why you can repair a broken system at any layer (Volume 1's rescue and emergency modes
drop you in BETWEEN stages). It is also why the same kernel boots identically on wildly different hardware: the
firmware and initramfs absorb the hardware differences, and by stage 6 everything looks the same.