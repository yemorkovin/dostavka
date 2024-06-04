from dadata import Dadata


class gDadata:
    token = "36e9f8f94c709c4c0c2d72d4950d6ac50d3f1c82"

    def __init__(self):
        self.dadata = Dadata(self.token)

    def getAddress(self, query):
        return self.dadata.suggest('address', query)