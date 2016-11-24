from urllib.parse import urlencode
from helper.configuration import Configuration
import logging
import requests
import json


def get_access_token(
    configuration_object,
    auth_object
):
    if configuration_object is None:
        raise ValueError('Configuration object must be passed.')
    if not isinstance(configuration_object, Configuration):
        raise TypeError('Configuration must be a configuration object.')

    if auth_object is None or auth_object == {}:
        raise ValueError('Authorization dictionary must be passed.')
    if not isinstance(auth_object, dict):
        raise TypeError('Authorization object must be a dictionary.')

    # Use logging, if defined else where, to track what is being done
    # in the app.
    logging.debug('Creating authorization URL for request.')

    # Build the parameters that will be used to populate the authorize_url with
    # the correct information
    #
    request_body = {
        "grant_type": "authorization_code",
        "client_id": configuration_object.config_dict.get('app_id'),
        "redirect_uri": configuration_object.config_dict.get('app_redirect_uri'),
        'client_secret': configuration_object.config_dict.get('app_secret'),
        'code': auth_object['code'],
        'scope': configuration_object.config_dict.get('app_scope')
    }
    logging.debug('Params: {0}'.format(request_body))

    r = requests.post(
        url=configuration_object.config_dict.get('app_token'),
        data=request_body
    )
    if r.status_code != 200:
        raise PermissionError('The application does not have permission!')

    # Return the URL for authentication. No authentication has taken place yet - the
    # user must click on the link and will then be asked to authenticate or another
    # method might redirect to this URL.
    #authorize_url = authorize_url.format(urlencode(params))
    #logging.debug('Authorization URL is {0}'.format(authorize_url))
    return r



