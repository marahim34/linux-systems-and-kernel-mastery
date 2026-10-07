9. The process to run. Exec-form (JSON array) lets signals reach uvicorn properly for clean shutdowns.





docker build -t goodo-api:1.2 .
docker image ls
docker run --rm --env-file .env -p 8000:8000 goodo-api:1.2