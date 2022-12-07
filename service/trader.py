import sys
sys.path.append('.')

from tasks import writing, analize_last_candles, hola

# try:
#     from .celery_app import celery
# except:
#     from celery_app import celery


from api.getCandles import Candles
import time as t
from datetime import datetime
import asyncio
from utils.singleton import SingletonPattern
# from api.connector import Connector

# MONEY = 10
# GOAL = 'EURUSD'
# size = 60
# maxditc = 1
# expiration_mode = 4

singleton = SingletonPattern()


@singleton.singleton
class Trader:

    # global hola

    def __init__(self, money: float, goal: str, size: int, maxditc: int, expiration_mode: int):
        self.money = money
        self.goal = goal
        self.size = size
        self.maxditc = maxditc
        self.expiration_mode = expiration_mode
        self.light = True


    # @staticmethod
    # semaphore = True
    async def start_trade(self, connector):

        # global semaphore

        # create a switch case for every new request
        # if not self.semaphore:
        #     self.semaphore = True
        # else:
        #     print('Lo cambio a false')
        #     self.semaphore = False

        # print(self.semaphore, 'light en el start trade')
        # return

        # self.light = True

        # TODO: esto me sirve para probar que cuando termina la tarea se libera el hilo, pero hasta que la tarea no termina no se pueden escuchar mas peticiones, y en este caso la terea de analizar el mercado es practicamente indefinida
        # for i in range(3):
        #     print(hola.delay())
        #     t.sleep(5)
        # return

        while self.light:

            print(self.light, 'light en el while')

            candles = Candles(connector)

            # print('Traemos las velas')
            candles = candles.get_candles(self.goal, self.size, self.maxditc, self.expiration_mode)
            # print('Llegaron las velas al start trade')
            # print(candles)
            # t.sleep(10)

            signal = analize_last_candles.delay(candles)
            # print('Llego el signal')
            # print(signal)
            # t.sleep(10)

            if signal == 'call':
                check, id = connector.api.buy(self.money, self.goal, 'call', self.expiration_mode)
                print('call', datetime.datetime.now())
                if check:
                    print('CALL option placed')
                    result, amount = connector.api.check_win_v4(id)
                    print(result)
                    writing.delay('call', result, amount)
                    # with open('operations.csv', 'a') as file:
                    #     file.write(f'PUT option placed, result: {result}\n')
                else:
                    print('CALL option failed')

            elif signal == 'put':
                print('put', datetime.datetime.now())
                check, id = connector.api.buy(self.money, self.goal, 'put', self.expiration_mode)

                if check:
                    print('PUT option placed')
                    result, amount = connector.api.check_win_v4(id)
                    print(result)
                    writing.delay('put', result, amount)
                    # with open('operations.csv', 'a') as file:
                    #     file.write(f'PUT option placed, result: {result}\n')
                else:
                    print('PUT option failed')

            # else:
            #     print('hold')

            # t.sleep(0.5)
            await asyncio.sleep(0.5)

    async def stop_trade(self):
        # await asyncio.sleep(0.5)
        print('Entra aca')
        self.light = False
        print(self.light, 'light en el stop trade')

    
# Trader.start_trade(None)

