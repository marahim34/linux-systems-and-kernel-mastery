3. Patterns work: any tuni.fi host automatically uses your student username.

Tunnels — SSH's superpower
ssh -L 5432:localhost:5432 hetzner
ssh -L 8080:internal-db:80 jumphost
ssh -R 9000:localhost:8000 hetzner
ssh -D 1080 hetzner