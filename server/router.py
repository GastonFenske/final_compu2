from api.connector import Connector
from api.getOpenMarkets import OpenMarkets
from constants import *

get_routes: dict = {}
post_routes: dict = {}
put_routes: dict = {}
delete_routes: dict = {}

def route(path=None, method='GET'):
    def decorator(func):
        route = set_routes(method)
        route[path] = func
    return decorator

def set_routes(route_type: str):
    type_of_routes = {
        'GET': get_routes,
        'POST': post_routes,
        'PUT': put_routes,
        'DELETE': delete_routes
    }
    return type_of_routes[route_type]

def get_fun_by_route(path):
    return get_routes[path]

@route('/api/open-markets', 'GET')
def get_open_markets():
    # try:
    #     connector = Connector(EMAIL, PASSWORD)
    #     open_markets = OpenMarkets(connector)
    #     print(open_markets.get_open_markets())
    # except:
    #     pass
    # return {'open_markets': 'some open markets'}
    try:
        connector = Connector(EMAIL, PASSWORD)
        open_markets = OpenMarkets(connector)
        return {'open_markets': open_markets.get_open_markets()}
    except Exception as e:
        return {'error': e}

@route('/api/connect', 'POST')
def connect():
    try:
        connector = Connector(EMAIL, PASSWORD)
        if connector.get_connect():
            return {'connect': True}
        else:
            return {'connect': False}
    except Exception as e:
        return {'error': e}
