#!/usr/bin/python

import thread
import hashlib
import socket
import json
import logging
import os
import MySQLdb
import coloredlogs
import uuid

logger = logging.getLogger("jsonSocket")
coloredlogs.install(level=logging.DEBUG)
logger.setLevel(logging.DEBUG)
FORMAT = '[%(asctime)-15s][%(levelname)s][%(funcName)s] %(message)s'
logging.basicConfig(format=FORMAT)
# logging.basicConfig(format=FORMAT,filename='log/server.log',filemode='w')


def encryptPassword(raw_password):
    import random
    algo = 'sha1'
    salt = uuid.uuid4().hex
    return hashlib.sha1(raw_password + salt).hexdigest()+"$"+str(salt)

def checkPassword(password, password_db):
    encrypted_password = password_db.split("$")[0]
    salt = password_db.split("$")[1]
    return True if hashlib.sha1(password + salt).hexdigest() == encrypted_password else False

def handler(clientsocket):
    data = clientsocket.recv(1024).strip()
    db = Database()
    if json.loads(data)[0]['login']:
        logger.debug("\tUser trying to log in") 
        authDict = {}
        authDict['nick'] = json.loads(data)[0]['nick']
        authDict['password'] = json.loads(data)[0]['password']
        logger.info("\tUser: %s, Password: %s ",authDict['nick'],authDict['password']) 
        bAuth = db.login(authDict)
        if bAuth:
            logger.info("\tUser logged in")
            clientsocket.sendall("OK")
        else:
            logger.error("\tUser and/or password invalid")
            clientsocket.sendall("ERROR: 1")
    else:
        logger.debug("\tUser trying sign in") 
        SignDict = {}
        SignDict['nick'] = json.loads(data)[0]['nick']
        SignDict['password'] = encryptPassword(json.loads(data)[0]['password'])
        SignDict['email'] = json.loads(data)[0]['email']
        SignDict['description'] = json.loads(data)[0]['description']
        SignDict['photo'] = json.loads(data)[0]['photo']
        bSign = db.signUp(SignDict)
        if bSign:
            logger.info("\tUser signed in")
            clientsocket.sendall("OK")
        else:
            logger.error("\tThere was some problem signing in")
            clientsocket.sendall("ERROR: 2")
    db.close()


class Database(object):
    """docstring for MySQLHandler"""
    db = None
    cur = None
    def __init__(self):
        super(Database, self).__init__()
        try:
            logger.info("\tConnecting to the database")
            self.db = MySQLdb.connect(read_default_file="~/.my.cnf",host="192.168.1.4",port=3306,db="lchat")
            self.cur = self.db.cursor()
        except MySQLdb.Error as  e:
            raise e

    def login(self,data):
        try:
            nRows = self.cur.execute("""SELECT nick,password FROM users WHERE nick=%s LIMIT 1;""",(data['nick']))
            if nRows == 1:
                return checkPassword(data['password'], self.cur.fetchone()[1])
            else:
                return False
        except MySQLdb as e:
            raise e

    def signUp(self,data):
        try:
            nRows = self.cur.execute("""INSERT INTO users SET nick=%s, password=%s, email=%s, description=%s, photo=%s;""",(data['nick'],data['password'],data['email'],data['description'],data['photo']))
            return True if nRows == 1 else False
        except MySQLdb.IntegrityError:
            logger.error("\tThe user already exist")
            #TODO: Here i need to notify to the user that the nick already exist
        except MySQLdb as e:
            raise e

    def close(self):
        self.cur.close()

if __name__ == "__main__":
    os.system('clear')
    logger.info("\tStarting Server application")
    host, port= "localhost", 9973

    addr = (host, port)
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Create the server, binding to localhost on port 9999
    serversocket.bind(addr)
    serversocket.listen(5)

    while True:
        logger.debug("\tServer is listening for connections")
        clientsocket, clientaddr = serversocket.accept()
        thread.start_new_thread(handler,(clientsocket,))

    serversocket.close()


