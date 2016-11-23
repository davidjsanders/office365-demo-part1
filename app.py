import os
import logging
from flask import Flask, request, render_template, current_app, url_for
from helper.authentication import Authentication
from helper.configuration import Configuration
from datetime import datetime


# Configure logging to a basic level. We will allow logging to be configured
# later if there is a setting in the config_dict file.
logging.basicConfig(level=logging.DEBUG)

# Create the Flask app
app = Flask(__name__)
app.config.from_object(__name__)

# Load the configuration file from a file specified in an environment variable
# called config_dict
logging.debug('Instantiating a configuration object')
configuration = Configuration()
try:
    configuration_file = os.environ['config']

    logging.debug('Loading configuration from the file: {0}'.format(configuration_file))
    configuration.configure_from_file(configuration_file, append=True)

    required_items_list = ['client_id']
    logging.debug('Validating configuration contains non-empty items for: {0}'.format(required_items_list))
    configuration.validate(required_items=required_items_list)
except KeyError as ke:
    logging.error('The environment variable "config" has not been set and IS required.')
    exit(1)
except FileNotFoundError as fnf:
    logging.error(
        'The file {0} cannot be found and has been set.'.format(fnf)
    )
    exit(1)
logging.debug('Configuration complete.')


@app.route('/', methods=['GET'])
def index_html():
    auth = Authentication(redirect_uri=url_for('authenticated', _external=True))

    try:
        auth.setup(configuration.config_dict.get('client_id', None))
    except KeyError as ke:
        logging.error(
            'The key {0} is not defined as an environment variable and IS required.'.format(ke)
        )
        exit(1)
    except Exception as e:
        raise
        exit(1)

    logging.debug('')
    logging.debug('** WARNING ** WARNING ** WARNING **')
    logging.debug('In production, the log entries in this block should NEVER be written.')
    logging.debug('They present sensitive information which WOULD be bad in the wrong hands!')
    logging.debug('Auth helper  : {0}'.format(auth.dump))
    logging.debug('Sign on at   : {0}'.format(auth.signon_url))
    logging.debug('Redirect URI : {0}'.format(auth.redirect_uri))
    logging.debug('Configuration: {0}'.format(configuration.obfuscated_config))
    logging.debug('** WARNING ** WARNING ** WARNING **')
    logging.debug('')
    logging.debug('In index_html')
    logging.debug('Method: GET')
    return render_template(
        'index.html',
        auth_source=auth.signon_url,
        publication_date='{0}'.format(datetime.now().strftime('%A %d %b %Y')),
        method=request.method
    )


@app.route('/authenticated', methods=['POST'])
def authenticated():
    logging.debug('In authenticated')
    logging.debug('Method: POST')
    return render_template(
        'authindex.html',
        publication_date='{0}'.format(datetime.now().strftime('%A %d %b %Y')),
        method=request.method
    )


@app.route('/cert-key', methods=['GET'])
def cert_key():
    return render_template(
        'cert-key.html'
    )

port = configuration.config_dict.get('port', 8000)
server = configuration.config_dict.get('server', "127.0.0.1")

app.run(host=server, port=port)
