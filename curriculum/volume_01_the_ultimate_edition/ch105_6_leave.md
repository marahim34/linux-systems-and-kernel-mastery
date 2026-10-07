6. Leave.

Creating an application database — the correct minimal-privilege setup
sudo -u postgres psql <<'SQL'
CREATE ROLE goodo_app LOGIN PASSWORD 'use-a-long-random-one';
CREATE DATABASE goodo OWNER goodo_app;
\c goodo
REVOKE ALL ON SCHEMA public FROM PUBLIC;
GRANT ALL ON SCHEMA public TO goodo_app;
SQL