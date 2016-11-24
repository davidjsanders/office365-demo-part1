from urllib.parse import urlencode
import uuid
import logging


def get_azure_signon_uri(
    client_id=None,
    resource='https://outlook.office365.com/',
    redirect_uri=None,
    authority='https://login.microsoftonline.com'
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
    - resource  : Defines the name of the Microsoft resource being accessed. By default,
                  this is set to https://outlook.office365.com/ and would change if
                  another API was being used.
    - redirect_uri : This is the URI that Microsoft will post to on successful
                  authentication, e.g. http://localhost:8000/page.html. Note the redirect
                  URI MUST be defined in the application definition in Azure AD. Within
                  the Azure portal, there are a set of Reply URLs associated with the
                  app; if the redirect_uri is not one of them, an error will be thrown.
    authority   : The authority performing the sign-on, authentication, and authorization
                  of the app. For most cases, the default https://login.microsoftonline.com
                  will be used.
    """

    # Use logging, if defined else where, to track what is being done
    # in the app.
    logging.debug('Creating signon URL for request.')

    # Check the client ID is defined and throw a value error if it's not.
    if client_id is None:
        raise ValueError(
            'A client id (for the application) must be registered in Azure AD and provided to signon_url'
        )

    # Check the redirect URI is defined and throw a value error if it's not.
    if redirect_uri is None:
        raise ValueError('A redirection URI must be provided for after successful authentication')

    # Create a universally unique ID with four words and convert it to a string.
    nonce = str(uuid.uuid4())

    # Build the first part of the URL. Using the default values, this would produce
    # https://login.microsoftonline.com/common/oauth2/authorize?{0}
    #
    # Note: the {0} is substituted in a later format call.
    authorize_url = '{0}{1}'.format(authority, '/common/oauth2/authorize?{0}')

    # Build the parameters that will be used to populate the authorize_url with
    # the correct information
    params = \
        {
            'client_id': client_id,            # The client ID
            'redirect_uri': redirect_uri,      # The redirect URI to return to
            'response_type': 'code id_token',  # The response type expected
            'scope': 'openid',                 # Sign in with work or school accounts
            'nonce': nonce,                    # The uuid generated above
            'prompt': 'admin_consent',         # tbc
            'response_mode': 'form_post',      # Respond by posting to the redirect uri
            'resource': resource,              # The resource requested
        }

    # Return the URL for authentication. No authentication has taken place yet - the
    # user must click on the link and will then be asked to authenticate or another
    # method might redirect to this URL.
    return authorize_url.format(urlencode(params))
