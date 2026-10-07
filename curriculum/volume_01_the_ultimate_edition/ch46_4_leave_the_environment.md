4. Leave the environment.
5. pipx: for TOOLS (not libraries) — each gets its own hidden venv, available globally. Best of both worlds.

Cleaning and system maintenance
sudo apt autoremove --purge
sudo apt clean
du -sh /var/cache/apt
sudo journalctl --vacuum-time=14d