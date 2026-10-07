6. Distribute the cert to client machines...
7. ...and register it as trusted system-wide — curl and apps now accept your internal service. This is the pattern for
eQuorum installs inside bank networks with no internet.

Keys, CSRs, and checking they match





openssl genpkey -algorithm ed25519 -out server.key
openssl req -new -key server.key -out server.csr -subj "/CN=api.bank.internal"
openssl pkey -in server.key -pubout | sha256sum
openssl x509 -in server.crt -pubkey -noout | sha256sum