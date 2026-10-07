3. Alternative: run it by passing to bash explicitly; no execute bit needed this way.

PRO INSIGHT: The safety trio 'set -euo pipefail' is the difference between amateur and professional bash. Without
it, a script whose command fails just keeps going, often making things worse (imagine a backup script that fails to
create the archive but then deletes the old one). With it, the script STOPS at the first sign of trouble. Type it at the
top of every script from now on, as a reflex.
PRACTICE EXERCISES