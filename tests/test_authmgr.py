'''
Created on Nov 2, 2014

@author: daniel
'''
from configparser import ConfigParser
import unittest
from trex import TrexAuthMgr, TrexConfig


class TestAuthMgr(unittest.TestCase):
    def setUp(self):
        unittest.TestCase.setUp(self)
        example = """
[users]
username=password, prog1, prog3
[programs]
prog1=/tmp/prog1
prog2=/tmp/prog2
""" 
        cfgparser = ConfigParser()
        cfgparser.read_string(example)
        self.config = TrexConfig(cfgparser)

    def testAuthenticateNoSuchUser(self):
        authmgr = TrexAuthMgr(self.config)
        self.assertFalse(authmgr.authenticated('nosuchuser', 'password'))
        
    def testAuthenticateWrongPassword(self):
        authmgr = TrexAuthMgr(self.config)
        self.assertFalse(authmgr.authenticated('username', 'passWORD'))
        
    def testAuthorizeNoPermissionForProg(self):
        authmgr = TrexAuthMgr(self.config)
        self.assertFalse(authmgr.authorized('username', 'prog2'))
        
    def testAuthorizeNoSuchUser(self):
        authmgr = TrexAuthMgr(self.config)
        self.assertFalse(authmgr.authorized('nosuchuser', 'prog1'))
    
    def testAuthorizeNoSuchProg(self):
        authmgr = TrexAuthMgr(self.config)
        self.assertFalse(authmgr.authorized('username', 'prog3'))
            
    def testAuthenticated(self):
        authmgr = TrexAuthMgr(self.config)
        self.assertTrue(authmgr.authenticated('username', 'password'))
    
    def testAuthorized(self):
        authmgr = TrexAuthMgr(self.config)
        self.assertTrue(authmgr.authorized('username', 'prog1'))
            
if __name__ == "__main__":
    unittest.main()