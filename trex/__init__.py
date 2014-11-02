# -*- coding: utf-8 -*-
'''
Created on Nov 1, 2014
@author: daniel
'''
import logging
import pickle
import socket
from threading import Thread


class TrexMsg(object):

    def __init__(self, username, password, program):
        self.username = username
        self.password = password
        self.program = program
        
    def __repr__(self, *args, **kwargs):
        return 'username={}, password={}, program={}'.format(self.username,
                                                             self.password,
                                                             self.program)


class TrexServer(object):
    """
    Document...
    """       

    DEFAULT_HOST = '0.0.0.0'
    DEFAULT_PORT = 9999

    def __init__(self, host=DEFAULT_HOST, port=DEFAULT_PORT):
        self.server_addr = ((host, port))
      
    def serve_forever(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(self.server_addr)
        sock.listen(5)
        while True:
            conn, client_addr = sock.accept()
            data = conn.recv(4096)
            msg = pickle.loads(data)
            logging.info("{} - {}".format(client_addr, msg))

            
class TrexExecHandler(Thread):
    """
    Document...
    """
    pass       


class TrexServerAuth(object):
    """
    This will
    """
    def __init__(self):
        pass
    def auth(self, username, password, program):
        pass


class TrexClient(object):
    """
    Document...
    """       
    
    DEFAULT_PORT = 9999

    def __init__(self, host, port=DEFAULT_PORT):
        self.server_addr = ((host, port))
    
    def send(self, msg):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(self.server_addr)
        data = pickle.dumps(msg)
        sock.sendall(data)
        sock.close()