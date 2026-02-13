
# CREATA CA
openssl genrsa -out ca-key.pem 4096
openssl req -new -x509 -days 365 -key ca-key.pem -out ca-cert.pem -subj "/C=US/ST=State/L=City/O=MyOrg/CN=MyCA"

# 2. Create server certificate with SANs
openssl genrsa -out server-key.pem 4096

# Create OpenSSL config for server cert with SANs
cat > server.cnf <<EOF
[req]
default_bits = 4096
prompt = no
default_md = sha256
distinguished_name = dn
req_extensions = v3_req

[dn]
C=US
ST=State
L=City
O=MyOrg
CN=localhost

[v3_req]
subjectAltName = @alt_names

[alt_names]
DNS.1 = localhost
DNS.2 = *.localhost
IP.1 = 127.0.0.1
IP.2 = ::1
EOF

openssl req -new -key server-key.pem -out server.csr -config server.cnf
openssl x509 -req -days 365 -in server.csr -CA ca-cert.pem -CAkey ca-key.pem -CAcreateserial -out server-cert.pem -extensions v3_req -extfile server.cnf

# client cert
openssl genrsa -out client-key.pem 4096
openssl req -new -key client-key.pem -out client.csr -subj "/C=US/ST=State/L=City/O=MyOrg/CN=client1"
openssl x509 -req -days 365 -in client.csr -CA ca-cert.pem -CAkey ca-key.pem -CAcreateserial -out client-cert.pem

rm server.csr client.csr server.cnf