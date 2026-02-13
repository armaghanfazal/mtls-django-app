import logging
from OpenSSL import crypto
from mtlsdemo.settings import CA_CERT_PATH
from rest_framework import authentication
from rest_framework import exceptions


logger = logging.getLogger(__name__)


class CertificateUser:
    def __init__(self, common_name, certificate_dn):
        self.username = common_name
        self.certificate_dn = certificate_dn
        self.is_authenticated = True
        self.is_anonymous = False

    def __str__(self):
        return f"CertificateUser({self.username})"


class CertificateAuthentication(authentication.BaseAuthentication):
    def __init__(self, *args, **kwargs):
        with open(CA_CERT_PATH, 'r') as f:
            ca_cert_pem = f.read()

        self.ca_cert = crypto.load_certificate(crypto.FILETYPE_PEM, ca_cert_pem)
        
        self.store = crypto.X509Store()
        self.store.add_cert(self.ca_cert)
    
    def authenticate(self, request):
        cert_pem = request.META.get('HTTPS_CC')

        if not cert_pem:
            raise exceptions.AuthenticationFailed('Invalid client certificate')

        try:
            cert = crypto.load_certificate(crypto.FILETYPE_PEM, cert_pem)

            store_ctx = crypto.X509StoreContext(self.store, cert)
            store_ctx.verify_certificate()

            subject = cert.get_subject()
            common_name = subject.CN
            certificate_dn = str(subject)

            user = CertificateUser(common_name, certificate_dn)

            return (user, None)
        except crypto.X509StoreContextError as e:
            raise exceptions.AuthenticationFailed(f'Certificate verification failed: {e}')
        except Exception as e:
            raise exceptions.AuthenticationFailed(f'Certificate verification error: {e}')
