from abc import ABC, abstractmethod

class TradeStrategy(ABC):

    @abstractmethod
    def analize(self, candles):
        """This method must return a string with the signal to execute"""


light = True
candle_analyzing = 0
close = 0
lower_band = 0
upper_band = 0

class SuperPatronStrategy(TradeStrategy):

    def analize(self, candles):

            global light
            global candle_analyzing
            global close
            global lower_band
            global upper_band

            import pandas as pd

            df = pd.DataFrame(candles)
            df.to_csv('candles.csv', index=False)
            df = pd.read_csv('candles.csv')
            # df['Date'] = pd.to_datetime(df['from'], unit='s')
            # df = df.set_index('Date')
            df['Open'] = df.pop('open')
            df['High'] = df.pop('max')
            df['Low'] = df.pop('min')
            df['Close'] = df.pop('close')
            df['Volume'] = df.pop('volume')

            # Esta sma y sd son para las bandas de bollinger por lo tanto el periodo lo dejamos en 6
            #Calculate simple moving average
            df['sma'] = df['Close'].rolling(6).mean()
            #Calculate standard deviation
            # df['sd'] = df['Close'].rolling(6).std()

            df['TP'] = (df['High'] + df['Low'] + df['Close']) / 3
            df['MA'] = df['TP'].rolling(6).mean()

            # Calculate standard deviation
            df['sd'] = df['Close'].rolling(6).std(ddof=0)

            df['ub'] = df['MA'] + (df['sd']*2)
            df['lb'] = df['MA'] - (df['sd']*2)


            #Calcula ema (media movil exponencial)
            df['ema'] = df['Close'].ewm(span=100.0,adjust=False).mean()

            # Calculate ema growing
            df['ema_growing'] = df['ema'].diff() > 0

            # Calculate stochastic oscillator
            #Calculate %K with period 13

            df['%K'] = 100*((df['Close'] - df['Low'].rolling(13).min())/(df['High'].rolling(13).max() - df['Low'].rolling(13).min()))
            #Calculate %D with period 3
            df['%D'] = df['%K'].rolling(3).mean()

            # Calculate CCI
            df['CCI'] = (df['Close'] - df['Close'].rolling(14).mean())/(0.015*df['Close'].rolling(14).std())

            # aca hasta aca voy

            def find_signal(close, lower_band, upper_band, current_candle, candle_analyzing, K, D, CCI, ema_growing):

                global light

                if current_candle != candle_analyzing:
                    print('========================')
                    print('Se abrio una vela nueva')
                    print(f'La vela cerró en: {close}')
                    print(f'La banda superior es: {upper_band}')
                    print(f'La banda inferior es: {lower_band}')
                    print(f'El K es: {K}')
                    print(f'El D es: {D}')
                    print(f'El CCI es: {CCI}')
                    print(f'La ema creciendo es: {ema_growing}')
                    print('========================')

                    light = True

                    data = {
                        'close': close,
                        'signal': '',
                        'message': '',
                        'id': ''
                    }


                    if close < lower_band:
                        print('Close menor a lower band <=============')
                        if K <= 20 and D <= 20:
                            print('K y D menor a 20 <=============')
                            if CCI <= -100:
                                print('CCI menor a -100 <=============')
                                if ema_growing == True:
                                    print('Ema creciendo <=============')
                                    print('Cumplio, CALL <=============')
                                    data['signal'] = 'call'
                                    data['message'] = 'Perforo la banda inferior y cerro. El bot compro a la alza'
                                    data['id'] = str(current_candle)
                                    return data

                    elif close > upper_band:
                        print('Close mayor a upper band <=============')
                        if K >= 80 and D >= 80:
                            print('K y D mayor a 80 <=============')
                            if CCI >= 100:
                                print('CCI mayor a 100 <=============')
                                if ema_growing == False:
                                    print('Ema decreciendo <=============')
                                    print('Cumplio, PUT <=============')
                                    data['signal'] = 'put'
                                    data['message'] = 'Perforo la banda superior y cerro. El bot compro a la baja'
                                    data['id'] = str(current_candle)
                                    return data

                    
                    # if close < lower_band and K <= 20 and D <= 20 and CCI <= -100 and ema_growing == True:
                    #     # TODO: podemos ver si cambia el id de la vela entonces perforo y cerro
                    #     data['signal'] = 'call'
                    #     data['message'] = 'Perforo la banda inferior y cerro. El bot compro a la alza'
                    #     data['id'] = str(current_candle)
                    #     return data
                    #     # return 'call'
                    # elif close > upper_band and K >= 80 and D >= 80 and CCI >= 100 and ema_growing == False:
                    #     data['signal'] = 'put'
                    #     data['message'] = 'Perforo la banda superior y cerro. El bot compro a la baja'
                    #     data['id'] = str(current_candle)
                    #     return data
                    else:
                        print('Entra al hold')
                        data['signal'] = 'new_veil'
                        data['message'] = 'No perforo la banda superior ni inferior. El bot se mantiene a la espera',
                        data['id'] = str(current_candle)
                        return data

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
            K = df['%K'].iloc[-1]
            D = df['%D'].iloc[-1]
            CCI = df['CCI'].iloc[-1]
            ema_growing = df['ema_growing'].iloc[-1]

            if light:
                candle_analyzing = current_candle
                light = False

            signal = find_signal(close, lower_band, upper_band, current_candle, candle_analyzing=candle_analyzing, K=K, D=D, CCI=CCI, ema_growing=ema_growing)

            return signal
