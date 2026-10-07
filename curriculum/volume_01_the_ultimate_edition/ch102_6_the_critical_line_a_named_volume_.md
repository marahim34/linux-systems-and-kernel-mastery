6. THE critical line: a named volume keeps database files when containers are rebuilt. No volume = data dies with the
container.
docker compose up -d
docker compose logs -f api
docker compose exec db psql -U postgres
docker compose down
docker compose down -v