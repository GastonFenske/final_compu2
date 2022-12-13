import sys
sys.path.append('.')
sys.path.append('service')

from api.connector import Connector
from api.getOpenMarkets import OpenMarkets
from service.trader import Trader
from constants import *
from server import Server


server = Server(HOST, PORT)
server.start()










