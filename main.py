import time
from iqoptionapi.stable_api import IQ_Option
from env import *

password = PASSWORD
# print(password)

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
# balance_type="PRACTICE"
# Iq.change_balance(balance_type)
# print(Iq.reset_practice_balance())

print(Iq.get_balance())
ALL_Asset=Iq.get_all_open_time()
print('hola')
print(ALL_Asset["binary"]["EURGBP-OTC"]["open"])
# print(ALL_Asset["binary"])

check,id = Iq.buy(100, "EURGBP-OTC", "call", 1)
time.sleep(5)
d=Iq.get_binary_option_detail()
# print(d["EURGBP-OTC"]["binary"])
if check:
    print('Checking')
    result, amount = Iq.check_win_v4(id)
    if result == 'win':
        print('Has ganado la operación por la cantidad de: ', amount)
    elif result == 'loose':
        print('Has perdido la operación por la cantidad de: ', amount)
else:
    print('Something went wrong')


# while True:
#     option = int(input("Ingrese 1 para comprar o 2 para vender: "))
#     if option == 1:
#         print("Comprar")
#         buy, id = Iq.buy(MONEY, GOAL, ACTION, EXPIRATION_MODE)
#         # buy = Iq.buy_digital_spot(GOAL, MONEY, ACTION, EXPIRATION_MODE)
#         print('Empezando a comprobar la operacion')
#         # check, status = Iq.check_win_v3(id)
#         # print(check, status)
#         print(id)
#         # print(Iq.check_win_v3(id))
#         print(Iq.check_win(id))

        # if buy:
        #     print("Compra exitosa")
        # else:
        #     print("Compra fallida")
    # elif option == 2:
    #     print("Vender")
    #     buy, id = Iq.buy(MONEY, GOAL, "put", EXPIRATION_MODE)
    #     if buy:
    #         print("Venta exitosa")
    #         # print(Iq.check_win_v2(id, 3))
    #     else:
    #         print("Venta fallida")
    # elif option == 3:
    #     print("Saldo reiniciado")
    #     Iq.reset_practice_balance()