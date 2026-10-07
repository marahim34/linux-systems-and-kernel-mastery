4. Restore drill into a scratch database...
5. ...because an untested backup is a hope, not a backup. Schedule the dump with a systemd timer (Ch. 7) and
test-restore monthly.

Health and performance queries every admin knows
SELECT pid, state, now()-query_start AS age, left(query,50)
FROM pg_stat_activity WHERE state != 'idle' ORDER BY age DESC;
SELECT pg_size_pretty(pg_database_size('goodo'));
SELECT relname, n_live_tup, n_dead_tup
FROM pg_stat_user_tables ORDER BY n_dead_tup DESC LIMIT 5;
SELECT pg_terminate_backend(12345);