# -*- coding: utf-8 -*-
'''
Created on Nov 1, 2014
@author: daniel
'''
import unittest
from docopt import docopt
from client import __doc__ as doc


class TestClient(unittest.TestCase):
    def testArgs(self):
        cmd = '--server 127.0.0.1 --user bob --password 1234 --exec cat'
        args = docopt(doc, cmd.split(' '))
        self.assertEqual(args['<ip>'], '127.0.0.1')
        self.assertEqual(args['<username>'], 'bob')
        self.assertEqual(args['<password>'], '1234')
        self.assertEqual(args['<program>'], 'cat')

if __name__ == "__main__":
    unittest.main()
