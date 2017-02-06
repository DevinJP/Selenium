from __future__ import print_function
import atexit
from socket import *

host = '' #host name for server
port = 83 #server port open for listening

serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind((host, port))

log = open('log.txt', 'a')

def exit_handler():
        log.close()

atexit.register(exit_handler)

while True:
        message, address = serverSocket.recvfrom(1024)
        print(message, file=log)                                  
