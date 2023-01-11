import sys
sys.path.append('.')

from tasks import analize_last_candles
from api.getCandles import Candles
import asyncio
from utils.singleton import SingletonPattern
from celery.result import AsyncResult
from db.repository import Repository
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
        self.repository = Repository()          # Esta linea quiza este al pedo

    async def start_trade(self, connector):

        self.light = True

        buyer = Buyer(connector, self.writer) # hay que pasarle el writer esto no me gusta mucho

        while self.light:

            candles = Candles(connector)

            candles = candles.get_candles(self.goal, self.size, self.maxditc, self.expiration_mode)

            data = analize_last_candles.delay(candles)

            data = AsyncResult(data.id).get()

            signal = data['signal']

            print(signal, 'signal')

            if signal == 'call':
                await buyer.buy_pro('call', self.money, self.goal, 4)

            elif signal == 'put':
                await buyer.buy_pro('put', self.money, self.goal, 4)
            
            elif signal == 'new_veil':
                await buyer.buy_pro('put', self.money, self.goal, 1)

            await asyncio.sleep(0.5)

    async def stop_trade(self):
        self.light = False

    
