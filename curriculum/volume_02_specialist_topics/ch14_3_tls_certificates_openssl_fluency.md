3. TLS & Certificates — openssl Fluency
The trust model in one paragraph
A certificate binds a public key to a name (api.goodo.app), signed by a Certificate Authority the client
already trusts. TLS then uses the key pair to negotiate an encrypted session. Everything else — chains,
expiry, SANs — is bookkeeping around that one idea.

Inspecting certificates — the four commands
echo | openssl s_client -connect goodo.app:443 -servername goodo.app 2>/dev/null | openssl
x509 -noout -dates -subject -issuer
openssl x509 -in cert.pem -noout -text | less
openssl s_client -connect goodo.app:443 -showcerts </dev/null 2>/dev/null | grep -c "BEGIN
CERT"
curl -vI https://goodo.app 2>&1 | grep -E "expire|issuer|SSL"