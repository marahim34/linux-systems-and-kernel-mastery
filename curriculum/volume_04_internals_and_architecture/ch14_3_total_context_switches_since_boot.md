3. Total context switches since boot — the sheer scale of the juggling act.

Fairness and priority
The modern Linux scheduler (the Completely Fair Scheduler, and its successor) tries to give every process a
FAIR share of CPU, weighted by priority. Priority is set by niceness: a value from -20 (greedy, high priority)
to +19 (nice to others, low priority). A 'nicer' process yields more readily to others.
nice -n 10 ./heavy_job.sh
sudo renice -5 -p 1234
ps -eo pid,ni,comm --sort=ni | head