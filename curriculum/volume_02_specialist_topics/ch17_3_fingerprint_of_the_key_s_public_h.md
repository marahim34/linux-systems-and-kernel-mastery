3. Fingerprint of the key's public half...
4. ...and of the cert's public key. IDENTICAL hashes = this key and cert belong together — the 30-second check that
prevents the 'key values mismatch' nginx startup failure.

Testing TLS without a browser
openssl s_client -connect host:443 -tls1_2 </dev/null
curl --cacert internal.crt https://eq.internal/health
openssl s_client -connect host:5432 -starttls postgres </dev/null