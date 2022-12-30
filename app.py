import sys
sys.path.append('.')
sys.path.append('service')

from constants import *
from server import Server

server = Server(HOST, PORT)
server.start()










