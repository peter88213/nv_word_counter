"""Provide a Configuration class for reading and writing JSON files.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/nv_word_counter
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import json


class ConfigurationJson:
    """Application configuration, representing a JSON file.

    Public instance variables:    
        settings: dict
    """

    def __init__(self, settings={}, options={}):
        """Initalize attribute variables.

        Optional arguments:
            settings -- default settings (dictionary)
            options -- default options (dictionary of boolean values)
        """
        self.settings = None
        self.options = None
        self._sLabel = 'SETTINGS'
        self._oLabel = 'OPTIONS'
        self.set(settings, options)

    def read(self, iniFile):
        """Read a configuration file.
        
        Positional arguments:
            iniFile: str -- path configuration file path.
            
        Settings and options that can not be read in, remain unchanged.
        """
        try:
            with open(iniFile, 'r', encoding='utf-8') as f:
                config = json.load(f)
        except FileNotFoundError:
            config = {}

        if self._sLabel in config:
            section = config[self._sLabel]
            for setting in self.settings:
                fallback = self.settings[setting]
                self.settings[setting] = section.get(setting, fallback)

        if self._oLabel in config:
            section = config[self._oLabel]
            for option in self.options:
                fallback = self.options[option]
                self.options[option] = section.get(option, fallback)

    def set(self, settings=None, options=None):
        """Set the entire configuration without writing the JSON file.

        Optional arguments:
            settings: dict -- new settings
            options -- default options (dictionary of boolean values)
        """
        if settings is not None:
            self.settings = settings.copy()
        if options is not None:
            self.options = options.copy()

    def write(self, iniFile):
        """Save the configuration to iniFile.

        Positional arguments:
            iniFile: str -- path configuration file path.
        """
        with open(iniFile, 'w', encoding='utf-8') as f:
            json.dump(
                {
                  self._sLabel: self.settings,
                  self._oLabel: self.options,
                },
                f,
                ensure_ascii=False,
                indent=4,
            )
