"""Build the nv_wc_configurator novelibre plugin package.
        
Note: VERSION must be updated manually before starting this script.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/nv_wc_configurator
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import os
import sys

sys.path.insert(0, f'{os.getcwd()}/../../novelibre/tools')
from package_builder import PackageBuilder

VERSION = '0.2.0'


class PluginBuilder(PackageBuilder):

    PRJ_NAME = 'nv_wc_configurator'
    LOCAL_LIB = 'nvwcconf'
    GERMAN_TRANSLATION = False


def main():
    pb = PluginBuilder(VERSION)
    pb.run()


if __name__ == '__main__':
    main()
