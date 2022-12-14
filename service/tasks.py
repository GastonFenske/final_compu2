try:
    from celery_app import celery
except:
    from .celery_app import celery
import time

import sys
sys.path.append('.')

@celery.task
def hola():
    print('hola que hace')

@celery.task
def writing(type, result, amount):
    with open('operations.csv', 'a') as f:
        f.write(f'{type}, {result}, {amount}\n')

light = True
candle_analyzing = 0

@celery.task
def analize_last_candles(candles):

    # print('Llegan las candles a la task de celery')
    # print(candles)
    # time.sleep(10)

    global light
    global candle_analyzing

    # candles = Iq.get_candles(GOAL, size, 100, time.time())
    import pandas as pd
    df = pd.DataFrame(candles)
    # print(df['id'].iloc[-1], 'LAAAAST CANDLE')
    df.to_csv('candles.csv', index=False)
    df = pd.read_csv('candles.csv')
    df['Date'] = pd.to_datetime(df['from'], unit='s')
    df = df.set_index('Date')
    df['Open'] = df.pop('open')
    df['High'] = df.pop('max')
    df['Low'] = df.pop('min')
    df['Close'] = df.pop('close')
    df['Volume'] = df.pop('volume')
    #Calculate simple moving average
    df['sma'] = df['Close'].rolling(20).mean()
    #Calculate standard deviation
    df['sd'] = df['Close'].rolling(20).std()
    #Calculate upper band
    df['ub'] = df['sma'] + (df['sd']*2)
    #Calculate lower band
    df['lb'] = df['sma'] - (df['sd']*2)
    #Calcula ema
    df['ema'] = df['Close'].ewm(span=100.0,adjust=False).mean()
    import numpy as np

    # df.dropna(inplace=True)

    def find_signal(close, lower_band, upper_band, current_candle, candle_analyzing):

        global light

        # print(current_candle, 'Current candle')
        # print(candle_analyzing, 'Candle analyzing')
        if current_candle != candle_analyzing:
            print('Se abrio una vela nueva')
            print('La vela cerró en: ', close)
            # print(current_candle, 'Current candle cuando cambia')
            # candle_analyzing = current_candle
            light = True
            # print('se cambio la vela', light)

            data = {
                'close': close,
                'signal': '',
                'message': '',
                'id': ''
            }

            if close < lower_band:
                # print('Entro al call')
                # TODO: podemos ver si cambia el id de la vela entonces perforo y cerro
                data['signal'] = 'call'
                data['message'] = 'Perforo la banda inferior y cerro. El bot compro a la alza'
                data['id'] = str(current_candle)
                return data
                # return 'call'
            elif close > upper_band:
                # print('Entro al put')
                data['signal'] = 'put'
                data['message'] = 'Perforo la banda superior y cerro. El bot compro a la baja'
                data['id'] = str(current_candle)
                return data
                # return 'put'
            else:
                print('Entra al hold2')
                data['signal'] = 'new_veil'
                data['message'] = 'No perforo la banda superior ni inferior. El bot se mantiene a la espera',
                data['id'] = str(current_candle)
                return data
                # return 'hold2', close

        # return 'hold'
        return {
            'close': '',
            'signal': 'hold',
            'message': 'Aun no se dan los parametros establecidos',
            'id': ''
        }


    close = df['Close'].iloc[-1]
    lower_band = df['lb'].iloc[-1]
    upper_band = df['ub'].iloc[-1]
    current_candle = df['id'].iloc[-1]

    if light:
        candle_analyzing = current_candle
        light = False
        # print('se cambio la vela', light)

    signal = find_signal(close, lower_band, upper_band, current_candle, candle_analyzing=candle_analyzing)

    return signal