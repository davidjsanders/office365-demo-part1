import os
import uuid
import logging
from urllib.parse import quote, urlencode


class Authentication(object):
    """
    An authentication helper for authenticating an application against Microsoft Office 365
    """
    _certificate = {
        "client_id": None,
        "cert_path": None,
        "cert_thumb": None
    }

#    _client_id = None
#    _cert_path = None
#    _cert_thumb = None
    _return_uri = {
        "protocol": "http",
        "server": "localhost",
        "port": 8000,
        "path": "authenticated"
    }

    _authority = 'https://login.microsoftonline.com'
    _redirect_uri = None
    _resource = 'https://outlook.office365.com/'

    def __init__(self, redirect_uri):
        self._redirect_uri = redirect_uri

    def setup_from_env(self):
        """Instruct the helper to look for its configuration within environment variables. The
        Authentication helper will look for client_id, cert_path, and cert_thumb environment
        variables."""
        try:
            logging.debug('Setup with environment variables')
            self._certificate['client_id'] = os.environ["client_id"]
            self._certificate['cert_path'] = os.environ["cert_path"]
            self._certificate['cert_thumb'] = os.environ["cert_thumb"]
        except KeyError as ke:
            raise

    def setup(
            self,
            client_id
    ):
        """Pass the required variables (client_id, cert_path, and cert_thumb) to the helper
        instead of reading them from environment variables."""

        logging.debug('Setup with passed parameter(s)')
        self._certificate['client_id'] = client_id
        #self._certificate['cert_path'] = cert_path
        #self._certificate['cert_thumb'] = cert_thumb


    @property
    def client_id(self):
        """The client of the application as registered/configured in the Active Directory
        associated with the Office 365 tenant."""
        return self._certificate['client_id']

    @property
    def cert_path(self):
        """The path (/path/to/certs/filename.cert) to the certificate (including the name
        of the certificate)."""
        return self._certificate['cert_path']

    @property
    def cert_thumb(self):
        """The thumbprint of the certificate."""
        return self._certificate['cert_thumb']

    @property
    def dump(self):
        """Produce a dictionary containing the client id, cert. path, and cert. thumbprint."""
        return self._certificate

    @property
    def authority(self):
        return self._authority

    @authority.setter
    def authority(self, value):
        self._authority = value

    @property
    def redirect_uri(self):
        return self._redirect_uri

    @redirect_uri.setter
    def redirect_uri(self, value):
        self._redirect_uri = value

    @property
    def resource(self):
        return self._resource

    @resource.setter
    def resource(self, value):
        self._resource = value

    @property
    def signon_url(self):
        if self._certificate['client_id'] is None:
            raise ValueError(
                'The client id, certificate path, and certificate thumbprint must be set.'
            )
        nonce = str(uuid.uuid4())

        authorize_url = '{0}{1}'.format(self._authority, '/common/oauth2/authorize?{0}')
        #token_url = '{0}{1}'.format(self._authority, '/{0}/oauth2/token')

        params = \
            {
                'client_id': self._certificate['client_id'],
                'redirect_uri': self._redirect_uri,
                'response_type': 'code id_token',
                'scope': 'openid',
                'nonce': nonce,
                'prompt': 'admin_consent',
                'response_mode': 'form_post',
                'resource': self._resource,
            }

        authorization_url = authorize_url.format(urlencode(params))

        return authorization_url
