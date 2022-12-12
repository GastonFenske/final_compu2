import sys, json
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
# repository = Repository()


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
            # print(candles[-1], 'LAST CANDLE EN EL TRADEEER')
            # print('Llegaron las velas al start trade')
            # print(candles)
            # t.sleep(10)

            data = analize_last_candles.delay(candles)
            # print('Llego el signal')
            # print(signal)
            # t.sleep(10)

            # TODO: example de la data
            # data = {
            #     'close': close,
            #     'signal': '',
            #     'message': ''
            # }

            data = AsyncResult(data.id).get()
            signal = data['signal']
            close = data['close']
            print(signal, 'signal')


            # await self.send_to_socket(self.writer, data)

            if signal == 'call':

                check, id = connector.api.buy(self.money, self.goal, 'call', self.expiration_mode)
                print('call', datetime.datetime.now())

                if check:
                    await self.send_to_socket_new_veil(self.writer, data)
                    print('CALL option placed')

                    operation_data = {
                        'type': 'operation',
                        'date': f'{datetime.datetime.now()}',
                        'market': f'{self.goal}',
                        'ammount_use': self.money,
                        'duration_in_min': self.expiration_mode,
                        'message': 'Call option placed',
                    }
                    await self.send_to_socket(self.writer, operation_data)

                    result, amount = connector.api.check_win_v4(id)

                    win = 0
                    if result != 'loose':
                        win = 1

                    datos = {
                        'date': f'{datetime.datetime.now()}',
                        'market': f'{self.goal}',
                        'result': win,
                        'ammount_use': self.money,
                        'profit': amount,
                        'duration_in_min': self.expiration_mode,
                        'type': 'call'
                    }
                    self.repository.insert('operations', datos)

                    # result_data = {
                    #     'result': win,
                    #     'type': 'call',
                    #     'profit': amount,
                    #     'date': f'{datetime.datetime.now()}'
                    #     'market': f'{self.goal}
                    # }
                    # repository.insert('operations', datos)

                    print(result)
                    # writing.delay('call', result, amount)
                    # with open('operations.csv', 'a') as file:
                    #     file.write(f'PUT option placed, result: {result}\n')
                else:
                    print('CALL option failed')

            elif signal == 'put':
                print('put', datetime.datetime.now())
                check, id = connector.api.buy(self.money, self.goal, 'put', self.expiration_mode)


                if check:
                    await self.send_to_socket_new_veil(self.writer, data)
                    print('PUT option placed')
                    result, amount = connector.api.check_win_v4(id)

                    win = 0
                    if result != 'loose':
                        win = 1

                    datos = {
                        'date': f'{datetime.datetime.now()}',
                        'market': f'{self.goal}',
                        'result': win,
                        'ammount_use': self.money,
                        'profit': amount,
                        'duration_in_min': self.expiration_mode,
                        'type': 'put'
                    }
                    self.repository.insert('operations', datos)
                    # repository.insert('operations', datos)

                    print(result)
                    # writing.delay('put', result, amount)
                    # with open('operations.csv', 'a') as file:
                    #     file.write(f'PUT option placed, result: {result}\n')
                else:
                    print('PUT option failed')

            # elif signal == 'hold':

            #     try:
            #         await self.send_to_socket(self.writer, data)
            #     except Exception as e:
            #         print(e, 'error en el send to socket')
            #         pass
            
            elif signal == 'new_veil':
                print(f'Se abrio una nueva vela maquinola y la anterior cerro en {close}')
                try:
                    print('y se envio por socket')
                    # TODO: esta enviando la informacion mediante sockets al front
                    # datos = {
                    #     'date': f'{datetime.datetime.now()}',
                    #     'market': 'EURUSD',
                    #     'result': 1,
                    #     'ammount_use': 10.0,
                    #     'profit': 9.0,
                    #     'duration_in_min': 60,
                    #     'type': 'put'
                    # }
                    # self.repository.insert('operations', datos)

                    operation_data = {
                        'id': 'JD5454NHB434',
                        'type': 'operation',  
                        'date': f'{datetime.datetime.now()}',
                        'market': f'{self.goal}',
                        'ammount_use': self.money,
                        'duration_in_min': self.expiration_mode,
                        'message': 'Call option placed',
                        'state': 'pending'
                    }
                    operation_data = json.dumps(operation_data)
                    await self.send_to_socket(self.writer, operation_data)

                    # await self.send_to_socket_new_veil(self.writer, data)
                except Exception as e:
                    print(e, 'error en el send to socket')
                    pass

            # else:
            #     print('hold')

            # t.sleep(0.5)
            await asyncio.sleep(0.5)

    async def send_to_socket_new_veil(self, writer, data):
        print('Entra aca')
        # message = f'Se abrio una nueva vela maquinola y la anterior cerro en {data["close"]}'
        if data["close"] != '':
            message = f'{datetime.datetime.now()} {data["message"]}. La vela cerro en: {data["close"]}'
        else:
            message = f'{datetime.datetime.now()} {data["message"]}'
        writer.write(message.encode())
        await writer.drain()
        print('Se envio la nueva vela por socket')

    async def send_to_socket(self, writer, data):
        writer.write(str(data).encode())
        await writer.drain()

    async def stop_trade(self):
        # await asyncio.sleep(0.5)
        print('Entra aca')
        self.light = False
        print(self.light, 'light en el stop trade')

    
# Trader.start_trade(None)

