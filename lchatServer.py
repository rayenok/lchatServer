#!/usr/bin/python

import SocketServer
import json
import logging
import os


logger = logging.getLogger("jsonSocket")
logger.setLevel(logging.DEBUG)
FORMAT = '[%(asctime)-15s][%(levelname)s][%(funcName)s] %(message)s'
logging.basicConfig(format=FORMAT)
# logging.basicConfig(format=FORMAT,filename='log/server.log',filemode='w')

class MyTCPHandler(SocketServer.BaseRequestHandler):
    """
    The RequestHandler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """
    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        if json.loads(self.data)[0]['login']:
           logger.debug("\tUser trying to log in") 
           nick = json.loads(self.data)[0]['nick']
           password = json.loads(self.data)[0]['password']
           logger.info("\tUser: %s, Password: %s ",nick,password) 
        # just send back the same data, but upper-cased
        self.request.sendall(self.data.upper())

if __name__ == "__main__":
    os.system('clear')
    logger.info("\tStarting Server application")
    HOST, PORT = "localhost", 9995

    # Create the server, binding to localhost on port 9999
    server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
