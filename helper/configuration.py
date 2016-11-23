import json
import logging


class Configuration(object):
    _config_file = None
    _config = None

    def __init__(self):
        logging.debug('Configuration object instantiated.')

    def __str__(self):
        return '** OBFUSCATED **' if self._config is not None else 'Not Set.'

    def configure_from_file(self, filename):
        logging.debug('Configuration object: configure from file --> {0}.'.format(filename))
        f = None

        try:
            self._config_file = filename
            f = open(filename, 'r')
            self._config = json.load(f)
        except Exception as e:
            logging.error('Configuration object: Exception --> {0}.'.format(repr(e)))
            raise
        finally:
            if f is not None:
                f.close()

    def validate(self, required_items=[]):
        if required_items == []:
            return True;
        if not isinstance(required_items, list):
            raise TypeError('The required items must be passed as a list of strings')

        for key in required_items:
            if key not in self._config:
                raise ValueError('{0} was not found in the configuration.'.format(key))
            _value = self._config.get(key, None)
            if _value is None or _value == "":
                raise ValueError('{0} is empty in the configuration.'.format(key))
        return True

    @property
    def config(self):
        logging.debug(
            'Configuration object: Returning configuration --> {0}'.format(self)
        )
        return self._config

    @config.setter
    def config(self, value):
        if isinstance(value, dict):
            self._config = value
        else:
            raise TypeError('Configuration incorrect. Must be a dictionary.')

    @property
    def obfuscated_config(self):
        logging.debug(
            'Configuration object: Returning configuration --> {0}'.format(self)
        )
        return_dict = {}
        for key in self._config:
            return_dict[key] = 'obfuscated'
        return return_dict
