"""Alternative word count plugin class for novelibre.

Requires Python 3.7+
Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/nv_word_counter
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
"""
from pathlib import Path
import webbrowser

from nvwordcnt.nvwordcnt_locale import _
from nvlib.configuration.configuration_json import ConfigurationJson
from nvlib.controller.plugin.plugin_base import PluginBase
from nvwordcnt.word_counter import WordCounter


class Plugin(PluginBase):
    """Alternative word count plugin class."""
    VERSION = '@release'
    API_VERSION = '5.30'
    DESCRIPTION = 'Customizable word counter'
    URL = 'https://github.com/peter88213/nv_word_counter'

    HELP_URL = 'https://github.com/peter88213/nv_word_counter/tree/main/docs/nv_word_counter'

    INI_FILENAME = 'wordcounter.json'
    INI_FILEPATH = '.novx/config'
    SETTINGS = dict(
        additional_word_separators=['—', '–'],
        additional_chars_to_ignore=[]
    )

    def install(self, model, view, controller):
        """Install the plugin.
        
        Positional arguments:
            model -- reference to the novelibre main model instance.
            view -- reference to the novelibre main view instance.
            controller -- reference to the novelibre main controller instance.

        Extends the superclass method.
        """
        super().install(model, view, controller)

        #--- Configure the main menu.

        # Add an entry to the Help menu.
        label = _('nv_word_counter Online help')
        self._ui.helpMenu.add_command(
            label=label,
            command=self.open_help,
        )

        #--- Load configuration.
        try:
            homeDir = str(Path.home()).replace('\\', '/')
            configDir = f'{homeDir}/{self.INI_FILEPATH}'
        except:
            configDir = '.'
        self.iniFile = f'{configDir}/{self.INI_FILENAME}'
        self._configuration = ConfigurationJson(self.SETTINGS)
        self._prefs = {}
        self._configuration.read(self.iniFile)
        self._prefs.update(self._configuration.settings)

        #--- Replace the default word counter with the customizable one.
        self._wordCounter = WordCounter()
        self._mdl.nvService.change_word_counter(self._wordCounter)

        #--- Apply the settings read from the configuration file.
        self.configure_word_counter()

    def configure_word_counter(self):
        try:
            self._wordCounter.set_ignore_regex(
                self._prefs['additional_chars_to_ignore']
            )
        except AttributeError:
            pass
        try:
            self._wordCounter.set_separator_regex(
                self._prefs['additional_word_separators']
            )
        except AttributeError:
            pass
        self.update_word_count()

    def update_word_count(self):
        if self._mdl.prjFile is None:
            return

        for scId in self._mdl.novel.sections:
            section = self._mdl.novel.sections[scId]
            if section.sectionContent:
                section.wordCount = self._wordCounter.get_word_count(
                    section.sectionContent
                )
        self._mdl.notify_observers()

    def on_quit(self):
        """Write back the configuration file.
        
        Overrides the superclass method.
        """
        for keyword in self._prefs:
            if keyword in self._configuration.settings:
                self._configuration.settings[keyword] = self._prefs[keyword]
        self._configuration.write(self.iniFile)

    def open_help(self):
        webbrowser.open(self.HELP_URL)

