from api.connector import Connector
from api.getOpenMarkets import OpenMarkets
from service.trader import Trader
from constants import *
import json
import asyncio
# from app import connector
from db.repository import Repository

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

active_market = []
@route('/api/open-markets', 'GET')
def get_open_markets():
    global active_market
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
            # open_markets = asyncio.gather(open_markets.get_open_markets())
            open_markets = open_markets.get_open_markets()
            # return every market with true or false if it's active
            markets = []
            print('active markets', active_market)
            for market in open_markets:
                if market in active_market:
                    data = {
                        'market': market,
                        'operating': True
                    }
                    # markets[market] = True
                    markets.append(data)
                else:
                    # markets[market] = False
                    data = {
                        'market': market,
                        'operating': False
                    }
                    markets.append(data)
            return {
                'open_markets': markets
            }
        else:
            return {
                'error': 'Please connect to IQ'
            }
    except Exception as e:
        return {'error': e}

semaphore = False
@route('/api/trade', 'POST')
def trade(body):

    global semaphore
    global active_market

    # create a switch case for every new request
    if not semaphore:
        semaphore = True
    else:
        semaphore = False


    body = json.loads(body)

    # MONEY = 10
    money = body['money']
    goal = body['market']
    # GOAL = 'EURUSD-OTC'
    size = 60
    maxditc = 1
    expiration_mode = 4

    # print(GOAL, 'este es el mercado que llega')

    try:
        if connector != None:
            # trader = Trader(MONEY, GOAL, size, maxditc, expiration_mode)
            trader = Trader()
            trader.money = money
            trader.goal = goal
            trader.size = size
            trader.maxditc = maxditc
            trader.expiration_mode = expiration_mode
            if semaphore:
                active_market.append(goal)
                print('Empezamos con el trade')
                # trader.start_trade(connector)
                asyncio.gather(trader.start_trade(connector))
                # trader.start_trade(connector)
                return {
                    'trade': 'trade started'
                }
            else:
                active_market.remove(goal)
                print('Paramos el trade')
                asyncio.gather(trader.stop_trade())
                return {
                    'trade': 'trade stopped'
                }
        else:
            return {
                'error': 'Please connect to IQ'
            }
    except Exception as e:
        print('Esta entrando aca', e)
        return {'error': e}

# @route('/api/home', 'GET')
# def get_home():
#     # open the home.html and return it
#     with open('home.html', 'rb') as f: # TODO: desacoplar esta funcion para renderizar html
#         return f.read()

connector = None
@route('/api/login', 'POST')
def post_login(payload):
    global connector
    payload = json.loads(payload)
    try:
        connector = Connector(payload['email'], payload['password'])
        if connector.get_connect():
            return {
                'status': 'ok',
                'message': f'Welcome {payload["email"]}'
            }
        else:
            return {
                'status': 'error',
                'error': 'Wrong credentials'
            }
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

@route('/api/operations', "GET")
def get_operations():
    repository = Repository()
    operations = repository.select('operations', '*')
    print(operations, 'operations desde el GET')
    return {
        'operations': operations
    }

@route('/api/operations-pending', "GET")
def get_operations_pending():
    repository = Repository()
    operations = repository.select_pending_operations('operations', '*')
    print(operations, 'operations desde el GET')
    return {
        'operations': operations
    }
