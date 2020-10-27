from BorsDataClient import BorsDataClient
from FireBaseClient import FireBaseClient

class LynxDataFetcher:

    def __init__(self):
        self._borsdata_client = BorsDataClient()
        self._firebase_client = FireBaseClient()

    def get_meta_data(self):
        self._instruments = self._borsdata_client.get_instruments()
        self._countries = self._borsdata_client.get_countries()
        self._branches = self._borsdata_client.get_branches()
        self._sectors = self._borsdata_client.get_sectors()
        self._markets = self._borsdata_client.get_markets()
        self._kpi_metadata = self._borsdata_client.get_kpi_metadata()
        self._reports_metadata = self._borsdata_client.get_reports_metadata()

    def set_meta_data(self):
        self._firebase_client.set_instruments(self._instruments)
        self._firebase_client.set_countries(self._countries)
        self._firebase_client.set_branches(self._branches)
        self._firebase_client.set_sectors(self._sectors)
        self._firebase_client.set_markets(self._markets)
        self._firebase_client.set_kpi_metadata(self._kpi_metadata)
        self._firebase_client.set_reports_metadata(self._reports_metadata)
        
    def update_stock_prizes(self):
        # TODO
        for instrument in self._instruments['instruments']:
            insId = instrument['insId']
            name = instrument['name']
            print('{} {}'.format(name, insId))
            return

    def get_reports(self):
        for instrument in self._instruments['instruments']:
            instrument_id = instrument['insId']
            name = instrument['name']
            print('Fetching report for {} with instrument ID {}'.format(name, instrument_id))
            reports = self._borsdata_client.get_instrument_reports(instrument_id)
            print(reports)
            return

    def slask(self):
        # TODO
        print('hasse')