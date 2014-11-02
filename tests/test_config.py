'''
Created on Nov 2, 2014

@author: daniel
'''
from configparser import ConfigParser
import unittest

from trex import TrexConfig


class TestConfig(unittest.TestCase):
    def testCreate(self):
        example = """
[users]
# username = password, program, ...
username1=salted_password, name1, name2

[programs]
# program = path
name1=path
name2=path
""" 
        cfgparser = ConfigParser()
        cfgparser.read_string(example)
        cfgparser = TrexConfig(cfgparser)
        self.assertTrue('username1' in cfgparser.users)
        self.assertEqual(cfgparser.users['username1']['password'], 'salted_password')
        self.assertTrue('name1' in cfgparser.users['username1']['programs'])
        self.assertTrue('name2' in cfgparser.users['username1']['programs'])
        self.assertTrue('name1' in cfgparser.programs)
        self.assertTrue('name2' in cfgparser.programs)

if __name__ == "__main__":
    unittest.main()