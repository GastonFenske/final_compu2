import sys, json
sys.path.append('.')

from tasks import analize_last_candles

from api.getCandles import Candles
import time as t
from datetime import datetime
import asyncio
from utils.singleton import SingletonPattern
from celery.result import AsyncResult
from db.repository import Repository
import datetime
from buyer import Buyer

singleton = SingletonPattern()

@singleton.singleton
class Trader:


    def __init__(self, money: float = None, goal: str = None, size: int = None, maxditc: int = None, expiration_mode: int = None):
        self.money = money
        self.goal = goal
        self.size = size
        self.maxditc = maxditc
        self.expiration_mode = expiration_mode
        self.light = True
        self.repository = Repository()

    async def start_trade(self, connector):

        self.light = True

        buyer = Buyer(connector)

        while self.light:

            candles = Candles(connector)

            candles = candles.get_candles(self.goal, self.size, self.maxditc, self.expiration_mode)

            data = analize_last_candles.delay(candles)

            data = AsyncResult(data.id).get()
            signal = data['signal']
            close = data['close']
            id = data['id']
            print(signal, 'signal')

            if signal == 'call':
                print('call', datetime.datetime.now())

                operation_data_promt, operation_data, id = buyer.buy_operation(signal, self.money, self.goal, self.expiration_mode)

                operation_data_promt = json.dumps(operation_data_promt)
                await self.send_to_socket(self.writer, operation_data_promt)

                self.repository.insert('operations', operation_data)
                operation_data = json.dumps(operation_data)
                await self.send_to_socket(self.writer, operation_data)

                # TODO: mientras esperamos el result de la operacion podriamos liberar el hilo, para que no se quede esperando y pueda seguir haciendo otras cosas
                # result, amount = await buyer.verify_operation_result(id)
                result, amount = buyer.verify_operation_result(id)

                win = 0
                if result != 'loose':
                    win = 1

                result_data = buyer.package_operation_result(signal, id, win, amount, self.money, self.expiration_mode, self.goal)

                self.repository.update('operations', result_data, {'id': id})

                await self.send_to_socket(self.writer, result_data)

                print(result)

                # =================================================


            elif signal == 'put':
                print('put', datetime.datetime.now())

                operation_data_promt, operation_data, id = buyer.buy_operation(signal, self.money, self.goal, self.expiration_mode)

                operation_data_promt = json.dumps(operation_data_promt)
                await self.send_to_socket(self.writer, operation_data_promt)

                self.repository.insert('operations', operation_data)
                operation_data = json.dumps(operation_data)
                await self.send_to_socket(self.writer, operation_data)

                # result, amount = await buyer.verify_operation_result(id)
                result, amount = await buyer.verify_operation_result(id)

                win = 0
                if result != 'loose':
                    win = 1

                result_data = buyer.package_operation_result(signal, id, win, amount, self.money, self.expiration_mode, self.goal)

                self.repository.update('operations', result_data, {'id': id})

                await self.send_to_socket(self.writer, result_data)
            
            elif signal == 'new_veil':

                print(f'Se abrio una nueva vela maquinola y la anterior cerro en {close}')

                # =====
                operation_data_promt, operation_data, id = buyer.buy_operation('put', self.money, self.goal, 1)

                operation_data_promt = json.dumps(operation_data_promt)
                await self.send_to_socket(self.writer, operation_data_promt)

                self.repository.insert('operations', operation_data)
                print('se guardo en la db la compra')

                operation_data = json.dumps(operation_data)
                await self.send_to_socket(self.writer, operation_data)
                print('Mando la card de la compra')

                # result, amount = await buyer.verify_operation_result(id)
                # gather o algo asi
                result, amount = buyer.verify_operation_result(id)
                print('Calculo el resultado de la compra y paso de largo por await')

                win = 0
                if result != 'loose':
                    win = 1

                result_data = buyer.package_operation_result(signal, id, win, amount, self.money, self.expiration_mode, self.goal)


                self.repository.update('operations', result_data, {'id': id})
                print('se actualizo la db la compra')

                result_data = json.dumps(result_data)
                await self.send_to_socket(self.writer, result_data)
                print('Mando la card del resultado de la operation/compra')
                # ======

            await asyncio.sleep(0.5)


    async def send_to_socket(self, writer, data):
        writer.write(str(data).encode())
        await writer.drain()

    async def stop_trade(self):
        self.light = False

    
