4. Your public IP as the internet sees it (differs from ip a behind NAT).

SSH — the complete professional setup
ssh-keygen -t ed25519 -C "abdur@laptop-2026"
ssh-copy-id -i ~/.ssh/id_ed25519.pub deploy@server
ssh -v deploy@server