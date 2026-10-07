4. Stop and remove containers — volumes SURVIVE.
5. -v also deletes volumes — the data-destroying flag; respect it like rm -rf.

Housekeeping and debugging





docker system df
docker system prune -a
docker inspect web | jq '.[0].NetworkSettings.IPAddress'
docker run -it --entrypoint bash goodo-api:1.2