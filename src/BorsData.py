import os

BORSDATA_API_KEY = os.environ.get("BORSDATA_API_KEY")

class BorsData:

    def __init__(self):
        self.data = 'hasse'

    def print_api_key(self):
        print(BORSDATA_API_KEY)

    def print_data(self):
        print(self.data)
