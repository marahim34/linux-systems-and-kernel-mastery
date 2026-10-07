3. System pods across all namespaces — Kubernetes runs itself in itself.

Deploying — declarative like Ansible, live like systemd
# app.yaml
apiVersion: apps/v1
kind: Deployment
metadata: { name: goodo }
spec:
replicas: 2
selector: { matchLabels: { app: goodo } }
template:
metadata: { labels: { app: goodo } }
spec:
containers:
- name: api
image: goodo-api:1.2
ports: [{ containerPort: 8000 }]
resources:
limits: { memory: "512Mi" }
--apiVersion: v1
kind: Service
metadata: { name: goodo-svc }
spec:
selector: { app: goodo }
ports: [{ port: 80, targetPort: 8000 }]