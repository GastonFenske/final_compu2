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
from celery.result import AsyncResult
from db.repository import Repository
import datetime
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

    def __init__(self, money: float = None, goal: str = None, size: int = None, maxditc: int = None, expiration_mode: int = None):
        self.money = money
        self.goal = goal
        self.size = size
        self.maxditc = maxditc
        self.expiration_mode = expiration_mode
        self.light = True
        self.repository = Repository()


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

        self.light = True

        # TODO: esto me sirve para probar que cuando termina la tarea se libera el hilo, pero hasta que la tarea no termina no se pueden escuchar mas peticiones, y en este caso la terea de analizar el mercado es practicamente indefinida
        # for i in range(3):
        #     print(hola.delay())
        #     t.sleep(5)
        # return

        while self.light:

            # print(self.light, 'light en el while')

            candles = Candles(connector)

            # print('Traemos las velas')
            candles = candles.get_candles(self.goal, self.size, self.maxditc, self.expiration_mode)
            # print('Llegaron las velas al start trade')
            # print(candles)
            # t.sleep(10)

            data = analize_last_candles.delay(candles)
            # print('Llego el signal')
            # print(signal)
            # t.sleep(10)

            data = AsyncResult(data.id).get()
            signal = data['signal']
            close = data['close']
            print(signal, 'signal')

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
            
            elif signal == 'hold2':
                print(f'Se abrio una nueva vela maquinola y la anterior cerro en {close}')
                try:
                    print('y se envio por socket')
                    # TODO: esta enviando la informacion mediante sockets al front
                    datos = {
                        'date': f'{datetime.datetime.now()}',
                        'market': 'EURUSD',
                        'result': 1,
                        'ammount_use': 10.0,
                        'profit': 9.0,
                        'duration_in_sec': 60
                    }
                    self.repository.insert('operations', datos)

                    await self.send_to_socket(self.writer, data)
                except Exception as e:
                    print(e, 'error en el send to socket')
                    pass

            # else:
            #     print('hold')

            # t.sleep(0.5)
            await asyncio.sleep(0.5)

    async def send_to_socket(self, writer, data):
        print('Entra aca')
        message = f'Se abrio una nueva vela maquinola y la anterior cerro en {data["close"]}'
        writer.write(message.encode())
        await writer.drain()
        print('Se envio el hold')

    async def stop_trade(self):
        # await asyncio.sleep(0.5)
        print('Entra aca')
        self.light = False
        print(self.light, 'light en el stop trade')

    
# Trader.start_trade(None)

