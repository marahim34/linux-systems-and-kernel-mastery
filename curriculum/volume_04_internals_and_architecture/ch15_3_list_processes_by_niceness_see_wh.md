3. List processes by niceness — see which are being greedy and which are yielding.

PRO INSIGHT: Unique point: because the scheduler is preemptive and fair, a single runaway process cannot
freeze a well-configured Linux server — it just gets its fair slice while everything else keeps running. This is why a
Linux box under 100% CPU load still responds to your SSH session, where a lesser system would lock up. The
scheduler is quietly the reason Linux feels rock-solid under pressure.

Why this matters for your work





When your GoOdo backend feels slow under load, the question becomes precise: is it waiting for CPU
(scheduler saturation — check load average against core count), waiting for disk (state D, check iostat), or
waiting for the database (sleeping on a network reply)? The scheduler's vocabulary — running, ready, waiting
— turns a vague 'it's slow' into a diagnosable condition. This is the difference between guessing and
knowing.