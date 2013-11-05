from configobj import ConfigObj
from configobj import ParseError
import sys
import os


def parse_config(configfile):
    """Parse a configuration file and create a Configuration
    object which will store all configuration"""

    if os.path.isfile(configfile):
        try:
            config = ConfigObj(configfile)
            return config
        except ParseError, e:
            print "Cannot parse configuration file: {}".format(e)
            sys.exit(0)
    else:
        print "Configuration file {} does not exist".format(configfile)
