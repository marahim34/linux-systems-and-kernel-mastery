19. Containers — Docker on Linux
What a container really is (now you can understand it)
A container is not a VM. It is a normal Linux process that the kernel isolates using namespaces (its own
view of PIDs, network, filesystem mounts, hostname) and limits using cgroups (CPU/RAM caps). One
kernel, many isolated userspaces. That's why containers start in milliseconds and why everything you've
learned — processes, permissions, networking — applies inside them.
docker run -d --name web -p 8080:80 nginx
docker ps
docker exec -it web bash
docker logs -f web
docker stats
docker stop web && docker rm web