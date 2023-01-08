import datetime, json, asyncio

class Buyer:

    def __init__(self, connector):
        self.connector = connector

    def buy_operation(self, signal: str, money: float, goal: str, expiration_mode: int = 1) -> tuple:
        """This will return the socket info to sent to front, for terminal and for cards"""

        check, id = self.connector.api.buy(money, goal, signal, expiration_mode)
        if self.verify_operation_buy(check):

            # This is the data that will be sent to the socket promt (terminal front)
            operation_data_promt = {
                    'date': f'{datetime.datetime.now()}',
                    'market': f'{goal}',
                    'id': id,
                    'ammount_use': money,
                    'duration_in_min': expiration_mode,
                    'type': 'new_veil',
                    'state': 'pending',
                    'message': f'El bot encontro una concidencia en el patron y ha abierto una nueva operacion de tipo: {signal}'
                }

            # operation_data_promt = json.dumps(operation_data)

            operation_data = {
                    'date': f'{datetime.datetime.now()}',
                    'market': f'{goal}',
                    'id': id,
                    'ammount_use': money,
                    'duration_in_min': expiration_mode,
                    'type': 'operation',  
                    'state': 'pending',
                    'message': f'{signal} option placed'
                }

            return operation_data_promt, operation_data, id

    def verify_operation_buy(self, check) -> bool:
        return True if check else False

    # async def verify_operation_result(self, id) -> tuple:
    #     """Return the result of the operation and the amount of money earned or lost"""
    #     result, amount = await self.connector.api.check_win_v4(id)
    #     return result, amount

    def verify_operation_result(self, id) -> tuple:
        """Return the result of the operation and the amount of money earned or lost"""
        result, amount = self.connector.api.check_win_v4(id)
        return result, amount

    def package_operation_result(self, signal, id, win, amount, money, expiration_mode, goal) -> str:
        """Return the data to be sent to the socket"""

        # esto solo cuando probamos despues hay que quitarlo
        if signal == 'new_veil':
            signal = 'put'

        result_data = {
            'date': f'{datetime.datetime.now()}',
            'market': f'{goal}',
            'id': id,
            'result': win,
            'ammount_use': money,
            'profit': amount,
            'duration_in_min': expiration_mode,
            'type': f'{signal}',
            'state': 'finished',
            'message': 'No benefits'
        }

        return result_data