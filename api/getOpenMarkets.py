
class OpenMarkets:

    def __init__(self, connector):
        self.connector = connector

    def get_open_markets(self) -> list:
        # conexion = self.connector.api().connect()
        # print(conexion)
        # print(conexion.get_all_open_time())
        all_open_markets = self.connector.api.get_all_open_time()
        binary = all_open_markets['binary']
        open_markets = []
        for x in binary:
            if binary[x]['open']:
                open_markets.append(x)
        return open_markets

