# -*- coding: utf-8 -*-
"""
Created on Nov 1, 2014
@author: daniel

Usage:
    server <config_file>
"""
from docopt import docopt
from trex import TrexServer
import logging

DEFAULT_LOGFILE = 'server.log'
DEFAULT_LOGLEVEL = logging.INFO

logging.basicConfig(filename=DEFAULT_LOGFILE, level=DEFAULT_LOGLEVEL)

if __name__ == '__main__':  
    args = docopt(__doc__)
    logging.info("Starting server with args: {}".format(args))
    s = TrexServer()
    s.serve_forever()
