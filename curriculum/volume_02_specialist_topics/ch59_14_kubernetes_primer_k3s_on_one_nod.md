14. Kubernetes Primer — k3s on One Node
What Kubernetes actually is (through Linux eyes)
You know systemd keeps one machine's services alive, and Docker packages processes. Kubernetes is the
same supervision idea across MANY machines: you declare desired state ('3 replicas of this image behind
this port') and controllers reconcile reality toward it — rescheduling containers off dead nodes, rolling out new
versions gradually. k3s is a production-grade single-binary distribution, ideal for learning and small
deployments.
curl -sfL https://get.k3s.io | sh sudo k3s kubectl get nodes
sudo kubectl get pods -A

1. k3s installs as — of course — a systemd service (systemctl status k3s: everything from Vol. 1 applies).