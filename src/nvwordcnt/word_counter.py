"""Provide a strategy class for counting words.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import re


class WordCounter:

    IGNORE_PATTERNS = [
        r'\<note\>.*?\<\/note\>',
        r'\<comment\>.*?\<\/comment\>',
        r'\<.+?\>',
    ]

    SEPARATOR_PATTERNS = [
        r'\<\/p\>',
    ]

    def __init__(self):
        self.set_ignore_regex('')
        self.set_separator_regex('—–')

    def set_ignore_regex(self, additionalCharacters):
        self._ignoreRegex = self._get_regex(
            self.IGNORE_PATTERNS[:], additionalCharacters
        )

    def set_separator_regex(self, additionalCharacters):
        self._separatorRegex = self._get_regex(
            self.SEPARATOR_PATTERNS[:], additionalCharacters
        )

    def get_word_count(self, text):
        """Return the total word count of text as an integer."""
        text = text.replace('\n', '')
        text = self._separatorRegex.sub(' ', text)
        text = self._ignoreRegex.sub('', text)
        return len(text.split())

    def _get_regex(self, patterns, additionalCharacters):
        for s in additionalCharacters:
            patterns.append(re.escape(s))
        return re.compile('|'.join(patterns))

