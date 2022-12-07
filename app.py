import sys
sys.path.append('.')
sys.path.append('service')

from api.connector import Connector
from api.getOpenMarkets import OpenMarkets
from service.trader import Trader
from constants import *
# from server.server import server
from server import Server
# from server.router import route, get_fun_by_route, get_routes

# connector = Connector(EMAIL, PASSWORD
# if connector.get_connect():
#     print('Connected')
# else:
#     print('Not connected')
# # get all open
# open_markets = OpenMarkets(connector)
# print(open_markets.get_open_markets())


# print(get_routes)

# print('Conectando con IQ...')
# connector = Connector(EMAIL, PASSWORD)
# print('!OK! -> Conectado con IQ')

# print('No llega nunca aca?')

# connector = Connector('s.fenske@alumno.um.edu.ar', 'perrito2')
# # if connector.get_connect():
# #     print('Connected')

# MONEY = 10
# GOAL = 'EURUSD-OTC'
# size = 60
# maxditc = 1
# expiration_mode = 4

# trader = Trader(MONEY, GOAL, size, maxditc, expiration_mode)

# print('Mercados abiertos')
# if connector != None:
#     open_markets = OpenMarkets(connector)
#     print(open_markets.get_open_markets())

# print('Empezamos con el trade')
# trader.start_trade(connector)

server = Server(HOST, PORT)
server.start()










