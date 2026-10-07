5. A fully private remote for client code (eQuorum!) that never touches GitHub. This is all GitHub fundamentally is, plus a
web UI.





Deploy-on-push — the classic hook
# server: /home/git/repos/goodo.git/hooks/post-receive (chmod +x)
#!/usr/bin/env bash
GIT_WORK_TREE=/opt/goodo git checkout -f main
sudo /usr/bin/systemctl restart goodo

1. post-receive runs after every push arrives.