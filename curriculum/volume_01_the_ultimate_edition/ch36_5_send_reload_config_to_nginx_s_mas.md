5. Send reload-config to nginx's master process — zero-downtime config change (systemctl reload does this for you).

Job control and priorities





python3 heavy_job.py &
disown -h %1
nice -n 10 tar -czf huge.tar.gz /data
sudo renice -5 -p 4321
ionice -c3 backup.sh