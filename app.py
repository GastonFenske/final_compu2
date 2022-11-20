from api.connector import Connector
from constants import *
from server.server import server
from server.router import route, get_fun_by_route, get_routes

# connector = Connector(EMAIL, PASSWORD)
# if connector.get_connect():
#     print('Connected')
# else:
#     print('Not connected')
# # get all open
# open_markets = OpenMarkets(connector)
# print(open_markets.get_open_markets())

# print(get_routes)
server()






