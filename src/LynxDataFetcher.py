from BorsDataClient import BorsDataClient
from FireBaseClient import FireBaseClient

class LynxDataFetcher:

    def __init__(self):
        self._borsdata_client = BorsDataClient()
        self._firebase_client = FireBaseClient()

    def run(self):
        print('---- Gathering Data from BorsDataAPI ----')
        self._instruments = self._borsdata_client.get_instruments_as_json()
        self.get_meta_data()
        #self.set_meta_data()
        #self.set_reports()
        self.set_stock_prices()
        #self.set_kpi_data()

    def get_meta_data(self):
        print('Gathering metadata')
        self._instruments = self._borsdata_client.get_instruments_as_json()
        self._countries = self._borsdata_client.get_countries_as_json()
        self._branches = self._borsdata_client.get_branches_as_json()
        self._sectors = self._borsdata_client.get_sectors_as_json()
        self._markets = self._borsdata_client.get_markets_as_json()
        self._kpi_metadata = self._borsdata_client.get_kpi_metadata_as_json()
        self._reports_metadata = self._borsdata_client.get_reports_metadata_as_json()
        self._translation_metadata = self._borsdata_client.get_translation_meta_data_as_json()

    def set_meta_data(self):
        print('Uploading metadata to firebase')
        self._firebase_client.set_metadata_instruments(self._instruments)
        self._firebase_client.set_metadata_countries(self._countries)
        self._firebase_client.set_metadata_branches(self._branches)
        self._firebase_client.set_metadata_sectors(self._sectors)
        self._firebase_client.set_metadata_markets(self._markets)
        self._firebase_client.set_metadata_kpi(self._kpi_metadata)
        self._firebase_client.set_metadata_reports(self._reports_metadata)
        self._firebase_client.set_metadata_translation(self._translation_metadata)
        
    def set_reports(self):
        for instrument in self._instruments['instruments']:
            instrument_id = instrument['insId']
            name = instrument['name']
            print('Uploading report for {} with instrument ID {} to firebase'.format(name, instrument_id))
            reports = self._borsdata_client.get_instrument_reports_as_json(instrument_id)
            self._firebase_client.set_report(instrument_id, reports)

    def set_stock_prices(self):
        for instrument in self._instruments['instruments']:
            instrument_id = instrument['insId']
            name = instrument['name']
            print('Uploading stock prices for {} with instrument ID {} to firebase'.format(name, instrument_id))
            stock_prices = self._borsdata_client.get_instrument_stock_prices_as_json(instrument_id)
            self._firebase_client.set_stock_prices(instrument_id, stock_prices)

    def set_kpi_data(self):
        """WIP"""
        for instrument in self._instruments['instruments']:
            instrument_id = instrument['insId']
            name = instrument['name']
            for kpi in self._kpi_metadata['kpiHistoryMetadatas']:
                kpi_id = kpi['kpiId']
                calc_group = '1year'
                calc = 'high'
                print('Uploading kpi_id {} for {} with instrument ID {} to firebase'.format(kpi_id, name, instrument_id))
                kpi_data = self._borsdata_client.get_kpi_data_instrument_as_json(instrument_id, kpi_id, calc_group, calc)
                print(kpi_data)
            return

    def add_quality_instruments(self):
        with open('kvalitetsbolag.txt') as file:
            for line in file:
                for instrument in self._instruments['instruments']:
                    if instrument['name'] in line:
                        #print('MATCH FOUND {} in {} {}'.format(line, instrument['name'], instrument['insId']))
                        match_found = True
                        instrument_id = instrument['insId']
                        data = { 
                            'insId' : instrument['insId'],
                            'name' : instrument['name'],
                        }
                        self._firebase_client.set_quality_instrument(instrument_id, data)

                if not match_found:
                    print('NO MATCH for {}'.format(line))