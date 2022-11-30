
class OpenMarkets:

    def __init__(self, conn):
        self.conn = conn

    def get_open_markets(self) -> list:
        all_open_markets = self.conn.api.get_all_open_time()
        binary = all_open_markets['binary']
        open_markets = []
        for x in binary:
            if binary[x]['open']:
                open_markets.append(x)
        return open_markets

