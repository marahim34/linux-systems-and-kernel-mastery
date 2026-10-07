3. How many certs the server sends — should be 2+ (leaf + intermediate); exactly 1 = the classic 'incomplete chain' that
browsers accept but strict clients (and Flutter apps!) reject.
4. curl's verdict on the whole setup.

Self-signed certificates — internal services done right
openssl req -x509 -newkey rsa:4096 -sha256 -days 825 \
-nodes -keyout internal.key -out internal.crt \
-subj "/CN=eq.internal" \
-addext "subjectAltName=DNS:eq.internal,IP:10.0.0.5"
chmod 400 internal.key
sudo cp internal.crt /usr/local/share/ca-certificates/
sudo update-ca-certificates