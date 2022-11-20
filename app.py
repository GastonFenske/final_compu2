from api import Connector, OpenMarkets
from constants import *
from server import route, server, get_routes

# connector = Connector(EMAIL, PASSWORD)
# if connector.get_connect():
#     print('Connected')
# else:
#     print('Not connected')
# # get all open
# open_markets = OpenMarkets(connector)
# print(open_markets.get_open_markets())

route()
print(get_routes)
server()






