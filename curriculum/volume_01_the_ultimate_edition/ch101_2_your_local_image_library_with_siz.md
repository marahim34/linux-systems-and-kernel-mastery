2. Your local image library with sizes.
3. --rm auto-cleans on exit; --env-file injects secrets the 12-factor way (never bake them into images).

Compose — whole stacks as one file
# docker-compose.yml
services:
api:
build: .
ports: ["8000:8000"]
env_file: .env
depends_on: [db]
restart: unless-stopped
db:
image: postgres:16
environment:
POSTGRES_PASSWORD: ${DB_PASS}
volumes:
- pgdata:/var/lib/postgresql/data
volumes:
pgdata: