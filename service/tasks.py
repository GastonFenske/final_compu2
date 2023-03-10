try:
    from celery_app import celery
except:
    from .celery_app import celery

import sys
sys.path.append('.')
from tarde_strategies import *

strategy = SuperPatronStrategy()

# @celery.task
# def hola():
#     print('hola que hace')

# @celery.task
# def writing(type, result, amount):
#     with open('operations.csv', 'a') as f:
#         f.write(f'{type}, {result}, {amount}\n')

@celery.task
def analize_last_candles(candles):
    return strategy.analize(candles)