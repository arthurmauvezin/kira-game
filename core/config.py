from configparser import SafeConfigParser
import os

config = SafeConfigParser(os.environ)
config.read('config.ini')

