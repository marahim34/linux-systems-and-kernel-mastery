4. The emergency fix, plus reload so nginx serves the new cert. Root causes are usually: port 80 blocked, changed
DNS, or a broken renewal hook.

PRO INSIGHT: Across all ten scenarios one method repeats: observe (logs, status, probes) → isolate the failing
layer → reproduce minimally → fix the cause, not the symptom → write the incident down. Your incident notes
become the runbook that makes the next occurrence a two-minute fix.
PRACTICE EXERCISES