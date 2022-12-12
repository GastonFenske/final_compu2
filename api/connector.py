from iqoptionapi.stable_api import IQ_Option

class Connector:

    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.api = IQ_Option(self.email, self.password)
        self.connect = self.api.connect()

    def get_connect(self) -> bool:
        if self.connect[0]:
            return True
        return False

    def api(self):
        return IQ_Option(self.email, self.password)

    def connect(self):
        return self.api().connect()
