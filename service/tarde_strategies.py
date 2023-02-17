from abc import ABC, abstractmethod
import datetime

class TradeStrategy(ABC):

    @abstractmethod
    def analize(self, candles):
        """This method must return a string with the signal to execute"""


# TODO: estas variables se las podemos poner a la clase no hace falta dejarlas aca afuera
light = True
candle_analyzing = 0
close = 0
lower_band = 0
upper_band = 0
K = 0
D = 0
CCI = 0
ema_growing = False

class SuperPatronStrategy(TradeStrategy):

    def analize(self, candles):

        global light
        global candle_analyzing
        global close
        global lower_band
        global upper_band
        global K
        global D
        global CCI
        global ema_growing


        import pandas as pd
        df = pd.DataFrame(candles)
        df.to_csv('candles.csv', index=False)
        df = pd.read_csv('candles.csv')
        df['Open'] = df.pop('open')
        df['High'] = df.pop('max')
        df['Low'] = df.pop('min')
        df['Close'] = df.pop('close')
        df['Volume'] = df.pop('volume')

        # Esta sma y sd son para las bandas de bollinger por lo tanto el periodo lo dejamos en 6
        #Calculate simple moving average
        # df['sma'] = df['Close'].rolling(6).mean()
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

        current_candle = df['id'].iloc[-1]

        if light:
            candle_analyzing = current_candle
            light = False

        if current_candle != candle_analyzing:

            print('Se abrio una vela nueva')
            print(f'La vela ({candle_analyzing}) cerró en: {close} upper en: {upper_band} lower en: {lower_band} => DATE: {datetime.datetime.now()}')
            # candle_analyzing = current_candle
            light = True

            data = {
                'close': close,
                'signal': '',
                'message': '',
                'id': ''
            }

            if close > upper_band:
                print('La vela esta por arriba del upper band')
                if K >= 80 and D >= 80:
                    print('Se cumplio tambien OCILADOR STOCHASTICO sobreventa')
                    if CCI >= 100:
                        print('Se cumplio tambien CCI mayor a 100')
                        if ema_growing == False:
                            print('Se cumplio tambien EMA que esta decreciendo')
                            data['signal'] = 'put'
                            data['message'] = 'Perforo la banda superior y cerro. El bot compro a la baja'
                            data['id'] = str(current_candle)
                            return data


            elif close < lower_band:
                print('La vela esta por debajo del lower band')
                if K <= 20 and D <= 20:
                    print('Se cumplio tambien OCILADOR STOCHASTICO sobrecompra')
                    if CCI <= -100:
                        print('Se cumplio tambien CCI menor a -100')
                        if ema_growing == True:
                            print('Se cumplio tambien EMA que esta creciendo')
                            data['signal'] = 'call'
                            data['message'] = 'Perforo la banda inferior y cerro. El bot compro a la alza'
                            data['id'] = str(current_candle)
                            return data
            else:
                print('Entra al new veil')
                data['signal'] = 'new_veil'
                data['message'] = 'No perforo la banda superior ni inferior. El bot se mantiene a la espera',
                data['id'] = str(current_candle)
                return data
        
        close = df['Close'].iloc[-1]
        lower_band = df['lb'].iloc[-1]
        upper_band = df['ub'].iloc[-1]
        K = df['%K'].iloc[-1]
        D = df['%D'].iloc[-1]
        CCI = df['CCI'].iloc[-1]
        ema_growing = df['ema_growing'].iloc[-1]


        return {
            'close': '',
            'signal': 'hold',
            'message': 'Aun no se dan los parametros establecidos',
            'id': ''
        }

        # aca hasta aca voy

