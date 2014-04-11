import socket
import sys
import json
import logging


logger = logging.getLogger("jsonSocket")
logger.setLevel(logging.DEBUG)
FORMAT = '[%(asctime)-15s][%(levelname)s][%(funcName)s] %(message)s'
logging.basicConfig(format=FORMAT)

HOST, PORT = "localhost", 9999
# data = " ".join(sys.argv[1:])
dataTest = [{'nick':'test','password':'bla','email':'bla@bla.com','description':'idk','photo':'/go/to/foo.png'}]

# Create a socket (SOCK_STREAM means a TCP socket)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Connect to server and send data
    sock.connect((HOST, PORT))
    sock.sendall(json.dumps(dataTest))

    # Receive data from the server and shut down
    received = sock.recv(1024)
finally:
    sock.close()

print "Sent:     {}".format(data)
print "Received: {}".format(received)
