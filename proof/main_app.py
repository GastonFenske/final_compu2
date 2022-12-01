from iqoptionapi.stable_api import IQ_Option
import time as t
from datetime import datetime
import datetime as dt
# from q import writing
import json, time, datetime, sys, os
from tasks import writing, analize_last_candles

user = 's.fenske@alumno.um.edu.ar'
password = 'perrito2'

Iq = IQ_Option(user, password)
connect = Iq.connect()
if connect:
    print('Conectado')
else:
    print('Error al conectarse')

Iq.change_balance('PRACTICE') # PRACTICE / REAL
balance = Iq.get_balance()
print(balance, 'Es su balance')

MONEY = 10
GOAL = 'EURUSD'
size = 60
maxditc = 1
expiration_mode = 4

print('Empezar stream...')

light = True
candle_analyzing = 0

# def analize_last_candles():
#     global light
#     global candle_analyzing

#     candles = Iq.get_candles(GOAL, size, 100, time.time())
#     import pandas as pd
#     df = pd.DataFrame(candles)
#     df.to_csv('candles.csv', index=False)
#     df = pd.read_csv('candles.csv')
#     df['Date'] = pd.to_datetime(df['from'], unit='s')
#     df = df.set_index('Date')
#     df['Open'] = df.pop('open')
#     df['High'] = df.pop('max')
#     df['Low'] = df.pop('min')
#     df['Close'] = df.pop('close')
#     df['Volume'] = df.pop('volume')
#     #Calculate simple moving average
#     df['sma'] = df['Close'].rolling(20).mean()
#     #Calculate standard deviation
#     df['sd'] = df['Close'].rolling(20).std()
#     #Calculate upper band
#     df['ub'] = df['sma'] + (df['sd']*2)
#     #Calculate lower band
#     df['lb'] = df['sma'] - (df['sd']*2)
#     #Calcula ema
#     df['ema'] = df['Close'].ewm(span=100.0,adjust=False).mean()
#     import numpy as np

#     # df.dropna(inplace=True)

#     def find_signal(close, lower_band, upper_band, current_candle, candle_analyzing):
#         global light
#         # clear terminal
#         # os.system('cls' if os.name == 'nt' else 'clear')
#         # print(f'Punto: {close}, Lower: {lower_band}, Upper: {upper_band}')
#         # print(close > upper_band)
#         # print(close < lower_band)
#         # verify if the candle is a new candle
#         # print(current_candle)
#         # print(candle_analyzing)
#         if current_candle != candle_analyzing:
#             print('Se abrio una vela nueva')
#             print('La vela cerró en: ', close)
#             # print(current_candle, 'Current candle cuando cambia')
#             # candle_analyzing = current_candle
#             light = True

#             if close < lower_band:
#                 # print('Entro al call')
#                 # TODO: podemos ver si cambia el id de la vela entonces perforo y cerro
#                 return 'call'
#             elif close > upper_band:
#                 # print('Entro al put')
#                 return 'put'
#             else:
#                 return 'hold'

#         return 'hold'


#     close = df['Close'].iloc[-1]
#     lower_band = df['lb'].iloc[-1]
#     upper_band = df['ub'].iloc[-1]
#     current_candle = df['id'].iloc[-1]

#     if light:
#         candle_analyzing = current_candle
#         light = False

#     signal = find_signal(close, lower_band, upper_band, current_candle, candle_analyzing=candle_analyzing)

#     return signal


if __name__ == '__main__':
    while True:

        candles = Iq.get_candles(GOAL, size, 100, time.time())
        signal = analize_last_candles.delay(candles)
        # print(signal, end='\r', flush=True)

        if signal == 'call':
            check, id = Iq.buy(MONEY, GOAL, 'call', expiration_mode)
            print('call', datetime.datetime.now())
            if check:
                print('CALL option placed')
                result, amount = Iq.check_win_v4(id)
                print(result)
                writing.delay('call', result, amount)
                # with open('operations.csv', 'a') as file:
                #     file.write(f'PUT option placed, result: {result}\n')
            else:
                print('CALL option failed')

        elif signal == 'put':
            print('put', datetime.datetime.now())
            check, id = Iq.buy(MONEY, GOAL, 'put', expiration_mode)

            if check:
                print('PUT option placed')
                result, amount = Iq.check_win_v4(id)
                print(result)
                writing.delay('put', result, amount)
                # with open('operations.csv', 'a') as file:
                #     file.write(f'PUT option placed, result: {result}\n')
            else:
                print('PUT option failed')

        # else:
        #     print('hold')

        t.sleep(0.5)