import time
from iqoptionapi.stable_api import IQ_Option
from env import *

password = PASSWORD
print(password)

Iq=IQ_Option("s.fenske@alumno.um.edu.ar", password)
Iq.connect()#connect to iqoption
GOAL="EURUSD"
MONEY=100
ACTION="call"
EXPIRATION_MODE=1
print("get candles")
candles = Iq.get_candles(GOAL, 60, 2,time.time()) #lista de velas, en forma de cola la ultima es la mas reciente
print(Iq.get_candles(GOAL, 60, 2,time.time())) 
print(Iq.check_connect())
balance_type="PRACTICE"
Iq.change_balance(balance_type)
# print(Iq.reset_practice_balance())

print(Iq.get_balance())

while True:
    option = int(input("Ingrese 1 para comprar o 2 para vender: "))
    if option == 1:
        print("Comprar")
        buy = Iq.buy(MONEY, GOAL, ACTION, EXPIRATION_MODE)
        # buy = Iq.buy_digital_spot(GOAL, MONEY, ACTION, EXPIRATION_MODE)
        if buy:
            print("Compra exitosa")
        else:
            print("Compra fallida")
    elif option == 2:
        print("Vender")
        buy = Iq.buy(MONEY, GOAL, "put", EXPIRATION_MODE)
        if buy:
            print("Venta exitosa")
        else:
            print("Venta fallida")
    elif option == 3:
        print("Saldo reiniciado")
        Iq.reset_practice_balance()