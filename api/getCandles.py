MONEY = 10
# GOAL = 'EURUSD'
size = 60
maxditc = 1
expiration_mode = 4
import time

class Candles:

    def __init__(self, connector):
        self.connector = connector

    def get_candles(self, goal: str, size: int, maxditc: int, expiration_mode: int) -> list:
        # print('Entra a la funcion get candles para extraer y enviar las velas')
        # candles = self.connector.api.get_candles(goal, size, maxditc, expiration_mode)
        candles = self.connector.api.get_candles(goal, size, 100, time.time())

        # print(candles[-1], 'CANDLEEEE EN EL GET CANDLES API')
        # print('Llegaron las velas, si es que llegan')
        # print(candles)
        # time.sleep(10)
        return candles