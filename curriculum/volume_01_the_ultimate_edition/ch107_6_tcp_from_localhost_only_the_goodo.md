6. TCP from localhost, only the goodo db, only its role, modern password hashing.
7. reload (not restart) applies HBA changes with zero downtime.

Backups — the part that defines you as an admin
sudo -u postgres pg_dump -Fc goodo > /backups/goodo_$(date +%F).dump
sudo -u postgres pg_dumpall --globals-only > /backups/roles.sql
pg_restore -l /backups/goodo_2026-07-02.dump | head
sudo -u postgres createdb goodo_restore
sudo -u postgres pg_restore -d goodo_restore /backups/goodo_2026-07-02.dump

1. -Fc = compressed custom format: smaller, and restorable table-by-table.