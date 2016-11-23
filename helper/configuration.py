import json
import logging


class Configuration(object):
    _config_file = None
    _config = None

    def __init__(self):
        logging.debug('In Configuration object instantiation method.')

    def __str__(self):
        return '** OBFUSCATED **' if self._config is not None else 'Not Set.'

    def configure_from_file(self, filename, append=False):
        logging.debug('Configuration object: configure from file --> {0}.'.format(filename))
        f = None

        try:
            self._config_file = filename
            f = open(filename, 'r')
            if not append:
                self._config = json.load(f)
            else:
                self._update_config(json.load(f))
        except Exception as e:
            logging.error('Configuration object: Exception --> {0}.'.format(repr(e)))
            raise
        finally:
            if f is not None:
                f.close()

    def configure_from_dict(self, config_dictionary={}, append=False):
        if not isinstance(config_dictionary, dict):
            raise TypeError('Configuration dictionary must be a Python dict')
        elif config_dictionary == {}:
            raise ValueError('Configuration dictionary cannot be empty if configure_from_dict called.')
        if not append:
            self._config = config_dictionary
        else:
            self._update_config(config_dictionary=config_dictionary)

    def _update_config(self, config_dictionary={}):
        if not isinstance(config_dictionary, dict):
            raise TypeError('Configuration dictionary must be a Python dict')
        if config_dictionary == {}:
            return
        if self._config is None:
            self._config = {}
        for key, value in config_dictionary.items():
            self._config[key] = value

    def validate(self, required_items=[]):
        if required_items == []:
            return True
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
    def config_dict(self):
        return self._config

    @config_dict.setter
    def config_dict(self, value):
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
