3. Handle Ctrl+C gracefully: message, conventional exit code 130.

Worked example — a deployment script with everything
#!/usr/bin/env bash
set -euo pipefail
readonly APP="goodo" HOST="hetzner"
readonly RELEASE="/opt/$APP/releases/$(date +%Y%m%d%H%M%S)"
log() { printf '\033[32m[deploy]\033[0m %s\n' "$*"; }
fail() { printf '\033[31m[error]\033[0m %s\n' "$*" >&2; exit 1; }
git diff --quiet || fail "Uncommitted changes — commit first"
log "Testing..."
./run_tests.sh || fail "Tests failed"
log "Uploading to $RELEASE"
ssh "$HOST" "mkdir -p $RELEASE"
rsync -az --exclude '.git' ./ "$HOST:$RELEASE/"
log "Switching symlink + restarting"
ssh "$HOST" "ln -sfn $RELEASE /opt/$APP/current \
&& sudo systemctl restart $APP"
sleep 3
curl -fsS "https://api.goodo.app/health" >/dev/null \
|| fail "Health check FAILED — investigate now"
log "Deployed successfully ✔"