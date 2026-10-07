23. Troubleshooting Scenarios — Ten Real Incidents
Each scenario below is a real-world pattern. Cover the resolution, work it from the symptom yourself, then
read on. This chapter is the book's dojo.

Scenario 1 — 'The website is down'
systemctl status nginx goodo # both active?
sudo ss -tulpn | grep -E ':80|:8000' # both listening?
curl -s localhost:8000/health # app OK locally?
curl -sI localhost # nginx OK locally?
journalctl -u goodo -n 30 # if not: why?