from urllib.parse import urlencode
from helper.configuration import Configuration
import uuid
import logging


def get_azure_signon_uri(
    configuration_object=None
):
    """
    get_azure_signon_url(client_id, resource, redirect_uri, authority).
    This definition is designed to be a helper to rapidly produce a URI to enable
    an application to jump out to Azure Active Directory, sign in with their Azure
    AD credentials, accept the permissions required from the app, and then return.

    - client_id : The Application Identifier defined in Azure. This is a universally
                  unique identifier (see https://en.wikipedia.org/wiki/Universally_unique_identifier)
                  which identifies the application. This needs to be passed to the
                  application BUT should not be hard-coded or stored in the app,
                  especially if the source is placed in a public repository. Ideally,
                  the client id should be stored outside the code repository and its
                  name and location passed as an environment variable.
    """

    if configuration_object is None:
        raise ValueError('Configuration object must be passed.')
    if not isinstance(configuration_object, Configuration):
        raise TypeError('Configuration must be a configuration object.')

    # Use logging, if defined else where, to track what is being done
    # in the app.
    logging.debug('Creating signon URL for request.')

    # Create a universally unique ID with four words and convert it to a string.
    nonce = str(uuid.uuid4())

    # Build the first part of the URL; for example:
    #
    #    https://login.microsoftonline.com/common/oauth2/v2.0/authorize?{0}
    #
    # The url is taken from the configuration object.
    #
    authorize_url = '{0}authorize?'.format(configuration_object.config_dict.get('app_root'))+"{0}"

    # Build the parameters that will be used to populate the authorize_url with
    # the correct information
    #
    params = \
        {
            # The client ID
            'client_id': configuration_object.config_dict.get('app_id'),
            # The redirect URI to return to
            'redirect_uri': configuration_object.config_dict.get('app_redirect_uri'),
            # The response type expected
            'response_type': configuration_object.config_dict.get('app_response_type'),
            # Sign in with work or school accounts
            'scope': configuration_object.config_dict.get('app_scope'),
            # The nonce - a uuid generated above
            'nonce': nonce,
            # The response mode (best practice ALWAYS form_post
            'response_mode': configuration_object.config_dict.get('app_response_mode')
        }
    logging.debug('Params: {0}'.format(params))

    # Return the URL for authentication. No authentication has taken place yet - the
    # user must click on the link and will then be asked to authenticate or another
    # method might redirect to this URL.
    authorize_url = authorize_url.format(urlencode(params))
    logging.debug('Authentication URL is {0}'.format(authorize_url))
    return authorize_url
