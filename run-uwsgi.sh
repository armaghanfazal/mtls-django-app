uwsgi \
    --https 0.0.0.0:8443,certs/server-cert.pem,certs/server-key.pem,HIGH,certs/ca-cert.pem \
    --https-export-cert \
    --module mtlsdemo.wsgi:application \
    --master \
    --processes 4 \
    --log-master