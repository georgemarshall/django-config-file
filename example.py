#!/usr/bin/env python
from config_file.parsers import IniConfig


if __name__ == '__main__':
    from pprint import pprint
    pprint(IniConfig('example.ini'))
