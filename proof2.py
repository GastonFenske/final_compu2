from iqoptionapi.stable_api import IQ_Option
import time as t
from datetime import datetime
import datetime as dt
from q import writing

user = 's.fenske@alumno.um.edu.ar'
password = ''

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
expiration_mode = 1

print('Empezar stream...')
Iq.start_candles_stream(GOAL, size, maxditc)

print('Hacer algo...')
now = datetime.now()
current_time = now.strftime("%H:%M:%S")
print("Current Time =", current_time)

end_time = now.replace(hour=23, minute=59, second=0, microsecond=0)

# Get real candles
cc = Iq.get_realtime_candles(GOAL, size)

# Place an option
remaining_time = Iq.get_remaning(expiration_mode)
purchase_time = remaining_time

for i in range(purchase_time, 0, -1):
    print(f'{i}', end='\r', flush=True)
    t.sleep(1)

# Place orders
while now < end_time:
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Current Time =", current_time)

    for k in list(cc.keys()):
        open = cc[k]['open']
        close = cc[k]['close']
        print('open', open, '|| Close: ', close)

        if close>open:
            print('Green')
            check, id = Iq.buy(MONEY, GOAL, 'call', expiration_mode)

            if check:
                print('CALL option placed')
                result, amount = Iq.check_win_v4(id)
                print(result)
                writing('call', result, amount)
                # with open('operations.csv', 'a') as file:
                #     file.write(f'PUT option placed, result: {result}\n')
            else:
                print('CALL option failed')
        
        else:
            print('Red')
            check, id = Iq.buy(MONEY, GOAL, 'put', expiration_mode)

            if check:
                print('PUT option placed')
                result, amount = Iq.check_win_v4(id)
                print(result)
                writing('put', result, amount)
                # with open('operations.csv', 'a') as file:
                #     file.write(f'PUT option placed, result: {result}\n')
            else:
                print('PUT option failed')
