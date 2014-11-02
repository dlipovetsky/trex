# -*- coding: utf-8 -*-
'''
Created on Nov 1, 2014
@author: daniel
'''
import unittest
from docopt import docopt
from server import __doc__ as doc


class TestServer(unittest.TestCase):
    def testArgs(self):
        cmd = '/etc/trex.conf'
        args = docopt(doc, cmd.split(' '))
        self.assertEqual(args['<config_file>'], '/etc/trex.conf')
        
if __name__ == "__main__":
    unittest.main()
