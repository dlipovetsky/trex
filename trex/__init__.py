# -*- coding: utf-8 -*-
'''
Created on Nov 1, 2014
@author: daniel
'''
from configparser import ConfigParser
import logging
import pickle
import socket
import subprocess
from threading import Thread


class TrexServer(object):
    """
    Document...
    """       
    DEFAULT_HOST = '0.0.0.0'
    DEFAULT_PORT = 9999

    def __init__(self, config, authmgr, host=DEFAULT_HOST, port=DEFAULT_PORT):
        self.server_addr = ((host, port))
        self.config = config
        self.authmgr = authmgr
      
    def serve_forever(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(self.server_addr)
        sock.listen(5)
        while True:
            conn, client_addr = sock.accept()
            data = conn.recv(4096)
            msg = pickle.loads(data)
            logging.info("{} - {}".format(client_addr, msg))
            execHandler = TrexExecHandler(self.config, self.authmgr, msg)
            execHandler.start()

class TrexExecHandler(Thread):
    """
    Handles a remote execution request.
    """
    def __init__(self, config, authmgr, msg):
        self.config = config
        self.authmgr = authmgr
        self.msg = msg
        Thread.__init__(self)
                
    def run(self):
        if self.authmgr.authenticated(self.msg.username, self.msg.password) \
        and self.authmgr.authorized(self.msg.username, self.msg.program):
            logging.info("executing {}".format(self.msg.program))
            call_args = [self.msg.program]
            try:
                subprocess.call(call_args, stdout=subprocess.DEVNULL,
                                stderr=subprocess.DEVNULL)
            except OSError as exc:
                logging.error("error executing {} - {}".format(self.msg.program,
                                                               exc))

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


class TrexMsg(object):
    """
    The message exchanged between client and server.
    """ 
    def __init__(self, username, password, program):
        self.username = username
        self.password = password
        self.program = program
        
    def __repr__(self, *args, **kwargs):
        return 'username={}, password={}, program={}'.format(self.username,
                                                             self.password,
                                                             self.program)


class TrexConfig(object):
    """
    Convenience wrapper around the configuration parser.
    """
    USERS_SECTION = 'users'
    PROGRAMS_SECTION = 'programs'
    
    def __init__(self, config):
        self.users = {}
        for username in config[TrexConfig.USERS_SECTION]:
            values = config[TrexConfig.USERS_SECTION].get(username)
            password, rest = values.split(',', 1)
            programs = rest.replace(' ','').split(',')
            self.users[username] = {}
            self.users[username]['password'] = password
            self.users[username][TrexConfig.PROGRAMS_SECTION] = programs
        self.programs = dict(config[TrexConfig.PROGRAMS_SECTION])


class TrexAuthMgr(object):
    """
    Authenticates users against stored passwords, authorizes user
    to execute programs.
    """
    
    def __init__(self, config):
        self.config = config
        
    def authenticated(self, username, password):
        if not username in self.config.users:
            return False
        if not self.config.users[username]['password'] == password:
            return False
        return True

    def authorized(self, username, program):
        if not program in self.config.programs:
            return False
        if not program in self.config.users[username]['programs']:
            return False
        return True
