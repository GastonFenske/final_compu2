from api.connector import Connector
from api.getOpenMarkets import OpenMarkets
from service.trader import Trader
from constants import *
import json
import asyncio
# from app import connector

get_routes: dict = {}
post_routes: dict = {}
put_routes: dict = {}
delete_routes: dict = {}

# TODO: if I move the routes that are below to another file, the route's mapping doesn't work
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

def get_fun_by_route(path, method='GET'):
    # return get_routes[path]
    return set_routes(method)[path]

@route('/api/proof', 'GET')
def get_proof():
    return {'proof': 'some proof'}

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

        # TODO: esto hay que desacploparlo no podemos estar conectandonos cada vez que necesitemos hacer algo
        # connector = Connector(EMAIL, PASSWORD)
        # connector = object()
        if connector != None:
            open_markets = OpenMarkets(connector)
            return {
                'open_markets': open_markets.get_open_markets()
            }
        else:
            return {
                'error': 'Please connect to IQ'
            }
    except Exception as e:
        return {'error': e}

@route('/api/trade', 'GET')
def trade():

    MONEY = 10
    GOAL = 'EURUSD-OTC'
    size = 60
    maxditc = 1
    expiration_mode = 4
    try:
        if connector != None:
            trader = Trader(MONEY, GOAL, size, maxditc, expiration_mode)
            print('Empezamos con el trade')
            # trader.start_trade(connector)
            asyncio.gather(trader.start_trade(connector))
            # trader.start_trade(connector)
            return {
                'trade': 'trade started'
            }
        else:
            return {
                'error': 'Please connect to IQ'
            }
    except Exception as e:
        return {'error': e}

@route('/api/home', 'GET')
def get_home():
    # open the home.html and return it
    with open('home.html', 'rb') as f: # TODO: desacoplar esta funcion para renderizar html
        return f.read()

connector = None
@route('/api/login', 'POST')
def post_login(payload):
    global connector
    payload = json.loads(payload)
    try:
        connector = Connector(payload['email'], payload['password'])
        return {
            'status': 'ok',
            'message': f'Welcome {payload["email"]}'
        }
    except Exception as e:
        return {
            'status': 'error',
            'error': e
        }

@route('/api/connect', 'POST')
def connect(body):
    print(body, 'body en connect')
    email = json.loads(body)['email']
    print(email, 'email')
    # print(body['email'], 'email en connect')
    return {
        'connect': json.loads(body)
    }
    # try:
    #     connector = Connector(EMAIL, PASSWORD)
    #     if connector.get_connect():
    #         return {'connect': True}
    #     else:
    #         return {'connect': False}
    # except Exception as e:
    #     return {'error': e}
