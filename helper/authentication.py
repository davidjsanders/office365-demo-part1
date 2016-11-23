import os
import uuid
import logging
from urllib.parse import quote, urlencode


def get_azure_signon_uri(
    client_id=None,
    resource='https://outlook.office365.com/',
    redirect_uri=None,
    authority='https://login.microsoftonline.com'
):
    logging.debug('Creating signon URL for request.')

    if client_id is None:
        raise ValueError(
            'A client id (for the application) must be registered in Azure AD and provided to signon_url'
        )

    if redirect_uri is None:
        raise ValueError('A redirection URI must be provided for after successful authentication')

    nonce = str(uuid.uuid4())

    authorize_url = '{0}{1}'.format(authority, '/common/oauth2/authorize?{0}')

    params = \
        {
            'client_id': client_id,
            'redirect_uri': redirect_uri,
            'response_type': 'code id_token',
            'scope': 'openid',
            'nonce': nonce,
            'prompt': 'admin_consent',
            'response_mode': 'form_post',
            'resource': resource,
        }

    authorization_url = authorize_url.format(urlencode(params))
    return authorization_url
