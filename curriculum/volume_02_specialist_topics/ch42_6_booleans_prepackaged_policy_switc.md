6. Booleans: prepackaged policy switches — this one lets a web app make outbound connections (reverse proxy
setups). -P persists.

PRO INSIGHT: The professional pattern on both systems: when something fails with correct permissions, CHECK
THE MAC LAYER before disabling it. dmesg/AppArmor or ausearch/SELinux names the exact denial; the fix is one
profile line or one boolean — not turning off the guard.
PRACTICE EXERCISES