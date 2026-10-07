6. A Service = stable internal address load-balancing across the replicas...
7. ...port 80 in, 8000 to containers.





sudo kubectl apply -f app.yaml
sudo kubectl get pods -w
sudo kubectl delete pod goodo-xxxxx
sudo kubectl logs -l app=goodo -f
sudo kubectl set image deployment/goodo api=goodo-api:1.3
sudo kubectl rollout undo deployment/goodo